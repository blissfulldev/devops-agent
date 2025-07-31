import os
import json
import uuid
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, JSONResponse

from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from pydantic import BaseModel

from agents.graph import create_graph, GraphState

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("server")

# --- Workspace setup ---
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(SERVER_DIR, "workspace")
os.makedirs(WORKSPACE_DIR, exist_ok=True)

app = FastAPI(
    title="DevOps Agent Server",
    version="1.0",
    description="FastAPI server for the multi-agent DevOps platform with HIL",
)

# CORS & static files
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=WORKSPACE_DIR), name="static")

# Global graph and in‑memory thread store
graph = None
threads: dict[str, GraphState] = {}

@app.on_event("startup")
async def startup_event():
    global graph
    graph = await create_graph()

@app.post("/stream")
async def stream_endpoint(request: Request):
    body = await request.json()
    logger.debug("▶ Incoming raw body: %s", body)

    thread_id = body.get("thread_id") or str(uuid.uuid4())
    user_text = body.get("input", "").strip()
    if not user_text:
        return JSONResponse({"error": "Empty input"}, status_code=400)

    # Only create a new state if thread_id is new
    if thread_id in threads:
        state = threads[thread_id]
        # Append the new user message
        state.messages.append(HumanMessage(content=user_text))
        state.input = user_text
    else:
        state = GraphState(
            input=user_text,
            messages=[HumanMessage(content=user_text)],
            thread_id=thread_id,
        )
        threads[thread_id] = state

    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        try:
            async for ev in graph.astream_events(
                state.dict(),
                config=config,
                version="v2",
            ):
                # Interrupt handling
                if ev["event"] == "interrupt":
                    logger.debug("🤔 Interrupt received: %s", ev["data"])
                    yield f"data: {json.dumps({'interrupt': ev['data']})}\n\n"
                    return  # Stop processing until approval

                # Streaming text
                if ev["event"] == "on_chat_model_stream":
                    chunk = ev["data"]["chunk"]
                    content = chunk.content if hasattr(chunk, "content") else chunk
                    if content:
                        yield f"data: {json.dumps({'text': content})}\n\n"

                # Diagram tool end
                if ev["event"] in ("on_tool_end", "tool_end") and ev.get("name") == "generate_diagram":
                    raw_out = ev["data"]["output"]
                    # parse into dict
                    if hasattr(raw_out, "content") and isinstance(raw_out.content, str):
                        try:
                            out = json.loads(raw_out.content)
                        except Exception:
                            continue
                    elif isinstance(raw_out, dict):
                        out = raw_out
                    elif isinstance(raw_out, str):
                        try:
                            out = json.loads(raw_out)
                        except Exception:
                            continue
                    else:
                        continue

                    status, path = out.get("status"), out.get("path")
                    if status == "success" and path and os.path.exists(path):
                        rel = os.path.relpath(path, WORKSPACE_DIR).replace(os.sep, "/")
                        yield f"data: {json.dumps({'image_url': f'/static/{rel}'})}\n\n"

        except Exception as e:
            logger.exception("🔥 graph.astream_events failed")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


class ResumeRequest(BaseModel):
    thread_id: str
    approved: bool

@app.post("/resume")
async def resume_endpoint(body: ResumeRequest):
    if body.thread_id not in threads:
        raise HTTPException(404, "Unknown thread_id")

    state = threads[body.thread_id]
    state.approved = body.approved

    config = {"configurable": {"thread_id": body.thread_id}}

    async def resume_generator():
        try:
            async for ev in graph.astream_events(
                state.dict(),
                config=config,
                version="v2",
                resume=body.approved,
            ):
                logger.debug(f"Resume Event: {ev['event']}, name={ev.get('name')}")

                if ev["event"] == "on_chat_model_stream":
                    chunk = ev["data"]["chunk"]
                    if hasattr(chunk, "content") and chunk.content:
                        yield f"data: {json.dumps({'text': chunk.content})}\n\n"

                if ev["event"] in ("on_tool_end", "tool_end") and ev.get("name") == "generate_diagram":
                    out = ev["data"]["output"]
                    if isinstance(out, dict) and out.get("status") == "success":
                        path = out.get("path")
                        rel  = os.path.relpath(path, WORKSPACE_DIR).replace(os.sep, "/")
                        yield f"data: {json.dumps({'image_url': f'/static/{rel}'})}\n\n"

            # signal completion
            yield f"data: {json.dumps({'done': True})}\n\n"

        except Exception:
            logger.exception("🔥 graph.astream_events (resume) failed")
            yield f"data: {json.dumps({'error':'internal resume error'})}\n\n"

    return StreamingResponse(resume_generator(), media_type="text/event-stream")


# (Optional) Clarification endpoint for answering agent questions
class ClarifyRequest(BaseModel):
    thread_id: str
    answers: list

@app.post("/clarify")
async def clarify_endpoint(body: ClarifyRequest):
    if body.thread_id not in threads:
        raise HTTPException(404, "Unknown thread_id")
    state = threads[body.thread_id]
    # You may want to store the answers in state, or pass them to the graph as needed
    state.answers = body.answers

    config = {"configurable": {"thread_id": body.thread_id}}

    async def clarify_generator():
        try:
            async for ev in graph.astream_events(
                state.dict(),
                config=config,
                version="v2",
                resume=True,
            ):
                logger.debug(f"Clarify Event: {ev['event']}, name={ev.get('name')}")
                if ev["event"] == "on_chat_model_stream":
                    chunk = ev["data"]["chunk"]
                    if hasattr(chunk, "content") and chunk.content:
                        yield f"data: {json.dumps({'text': chunk.content})}\n\n"
                if ev["event"] in ("on_tool_end", "tool_end") and ev.get("name") == "generate_diagram":
                    out = ev["data"]["output"]
                    if isinstance(out, dict) and out.get("status") == "success":
                        path = out.get("path")
                        rel  = os.path.relpath(path, WORKSPACE_DIR).replace(os.sep, "/")
                        yield f"data: {json.dumps({'image_url': f'/static/{rel}'})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception:
            logger.exception("🔥 graph.astream_events (clarify) failed")
            yield f"data: {json.dumps({'error':'internal clarify error'})}\n\n"

    return StreamingResponse(clarify_generator(), media_type="text/event-stream")


@app.post("/interrupt")
async def interrupt_endpoint(request: Request):
    body = await request.json()
    logger.debug("▶ Interrupt request: %s", body)

    thread_id = body.get("thread_id")
    if not thread_id or thread_id not in threads:
        raise HTTPException(404, "Unknown thread_id")

    state = threads[thread_id]

    # Approve the interrupt
    state.approved = True

    config = {"configurable": {"thread_id": thread_id}}

    async def stream_generator():
        try:
            async for ev in graph.astream_events(
                state.dict(),
                config=config,
                version="v2"
            ):
                if ev["event"] == "interrupt":
                    # Store the interrupt state
                    st.session_state.awaiting_approval = True
                    st.session_state.pending_interrupt = ev["data"]
                    yield f"data: {json.dumps({'interrupt': ev['data']})}\n\n"
                    break

        except Exception:
            logger.exception("🔥 graph.astream_events (interrupt) failed")
            yield f"data: {json.dumps({'error':'internal interrupt error'})}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")


@app.get("/debug/{thread_id}")
async def debug_thread(thread_id: str):
    if thread_id not in threads:
        return {"error": "Thread not found"}
    
    state = threads[thread_id]
    return {
        "thread_id": thread_id,
        "input": state.input,
        "messages_count": len(state.messages) if state.messages else 0,
        "awaiting_approval": getattr(state, 'awaiting_approval', None),
        "approved": getattr(state, 'approved', None),
        "next_agent": getattr(state, 'next_agent', None),
    }
