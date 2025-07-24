import os, json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from agents.graph import create_graph
from fastapi.responses import StreamingResponse
from langchain.schema import BaseMessage
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("server")

# Define workspace path robustly
# The server.py file is inside devops-app, and workspace is at the same level.
# So we get the directory of the current file and join it with 'workspace'.
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.join(SERVER_DIR, "workspace")

# Create workspace if it doesn't exist
os.makedirs(WORKSPACE_DIR, exist_ok=True)

app = FastAPI(
    title="DevOps Agent Server",
    version="1.0",
    description="FastAPI server for the multi-agent DevOps platform",
)

graph = None

@app.on_event("startup")
async def startup_event():
    global graph
    graph = await create_graph()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the workspace directory to serve generated files like diagrams
app.mount("/static", StaticFiles(directory=WORKSPACE_DIR), name="static")

@app.post("/stream")
async def stream_endpoint(request: Request):
    body = await request.json()
    logger.debug("▶ Incoming raw body: %s", body)

    user_text = body.get("input", "").strip()
    if not user_text:
        return {"error": "Empty input"}

    # The input to the graph is a list of messages
    graph_input = {"messages": [("user", user_text)]}

    # Get the thread_id from the request, or create a new one
    thread_id = body.get("thread_id") or str(uuid.uuid4())
    logger.debug("▶ Using thread_id: %s", thread_id)

    # Configuration for the graph stream, including the thread_id for state management
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        try:
            async for event in graph.astream_events(graph_input, config=config, version="v2"):
                logger.debug(
                    f"Event: {event['event']}, Name: {event.get('name')}, Data keys: {list(event.get('data',{}).keys())}"
                )

                # 1) Stream LLM tokens as before
                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"].get("chunk")
                    if chunk and getattr(chunk, "content", None):
                        yield f"data: {json.dumps({'text': chunk.content})}\n\n"

                # 2) Capture the generate_diagram tool end
                if event["event"] in ("on_tool_end", "tool_end") and event.get("name") == "generate_diagram":
                    raw_out = event["data"].get("output")

                    # 2a) If it’s a message‐like object with .content, parse that
                    if hasattr(raw_out, "content") and isinstance(raw_out.content, str):
                        try:
                            out = json.loads(raw_out.content)
                        except json.JSONDecodeError:
                            logger.error("Could not parse .content JSON", raw_out.content)
                            continue

                    # 2b) If it’s already a dict, use it directly
                    elif isinstance(raw_out, dict):
                        out = raw_out

                    # 2c) If it’s a plain string, assume it’s JSON
                    elif isinstance(raw_out, str):
                        try:
                            out = json.loads(raw_out)
                        except json.JSONDecodeError:
                            logger.error("Could not parse string output JSON", raw_out)
                            continue

                    else:
                        logger.error("Unexpected generate_diagram output type", type(raw_out))
                        continue

                    status = out.get("status")
                    path   = out.get("path")
                    logger.debug("Parsed generate_diagram output:", out)

                    if status == "success" and path and os.path.exists(path):
                        rel = os.path.relpath(path, WORKSPACE_DIR).replace(os.sep, "/")
                        url = f"/static/{rel}"
                        yield f"data: {json.dumps({'image_url': url})}\n\n"
        except Exception:
            logger.exception("🔥 graph.astream_events failed")
            yield f"data: {json.dumps({'error': 'internal stream error'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", port=8080)
