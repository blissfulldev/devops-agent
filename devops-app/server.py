import os, json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from supervisor.graph import create_graph
from langgraph.graph import START
from fastapi.responses import StreamingResponse
import uuid
import logging
from langchain.schema import HumanMessage, BaseMessage

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("server")

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

    # add_fastapi_endpoint(app, sdk, "/copilotkit_remote", max_workers=10)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            # Use astream_events (v2) to get a stream of events from the graph
            async for event in graph.astream_events(graph_input, config=config, version="v2"):
                # We are interested in the tokens streamed from the underlying chat model
                if event["event"] == "on_chat_model_stream":
                    chunk = event["data"].get("chunk")
                    if chunk and hasattr(chunk, 'content') and chunk.content:
                        # The Streamlit client expects a JSON object with a "text" key
                        data_to_send = {"text": chunk.content}
                        # Format as a Server-Sent Event (SSE) and send to the client
                        yield f"data: {json.dumps(data_to_send)}\n\n"
        except Exception as e:
            logger.exception("🔥 graph.astream_events failed")
            error_message = {"error": str(e)}
            yield f"data: {json.dumps(error_message)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", port=8080)
