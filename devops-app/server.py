import os, json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from agents.graph import create_graph
from fastapi.responses import StreamingResponse
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
    allow_origins=[os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")],
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
        # Flag to identify when the diagram_agent is producing its final answer (the raw Python code)
        # which should not be streamed to the UI.
        is_diagram_agent_final_answer_pending = False
        try:
            # Use astream_events (v2) to get a stream of events from the graph
            async for event in graph.astream_events(graph_input, config=config, version="v2"):
                # Log every event for debugging purposes
                logger.debug(f"Event: {event['event']}, Name: {event.get('name')}, Data: {event.get('data')}")

                # Stream LLM tokens for the "thinking" effect
                if event["event"] == "on_chat_model_stream":
                    # If this flag is set, we are in the diagram_agent's final answer stream.
                    # We suppress this stream because it's the raw Python code intended for the next agent.
                    if event.get("name") == "diagram_agent" and is_diagram_agent_final_answer_pending:
                        continue  # Skip sending this chunk to the UI

                    chunk = event["data"].get("chunk")
                    if chunk and hasattr(chunk, 'content') and chunk.content:
                        data_to_send = {"text": chunk.content}
                        yield f"data: {json.dumps(data_to_send)}\n\n"
                
                # When the diagram tool finishes, send the image path to the client
                if event["event"] == "on_tool_end" and event["name"] == "generate_diagram":
                    # Set the flag to suppress the agent's next stream, which will be the raw code
                    is_diagram_agent_final_answer_pending = True
                    tool_output_str = event["data"].get("output")
                    tool_output = {}
                    if tool_output_str:
                        try:
                            tool_output = json.loads(tool_output_str)
                        except (json.JSONDecodeError, TypeError):
                            logger.warning(f"Could not parse tool output: {tool_output_str}")

                    if tool_output.get("status") == "success":
                        image_path = tool_output.get("path")
                        if image_path and os.path.exists(image_path):
                            # Convert the absolute filesystem path to a relative URL
                            # that the client can use.
                            # We already have the absolute path to workspace
                            relative_path = os.path.relpath(image_path, WORKSPACE_DIR)
                            image_url = f"/static/{relative_path.replace(os.sep, '/')}"
                            
                            data_to_send = {"image_url": image_url}
                            yield f"data: {json.dumps(data_to_send)}\n\n"

                            # Also send a user-friendly confirmation message to the UI
                            confirmation_message = "\n\nDiagram generated successfully."
                            data_to_send = {"text": confirmation_message}
                            yield f"data: {json.dumps(data_to_send)}\n\n"
        except Exception as e:
            logger.exception("🔥 graph.astream_events failed")
            error_message = {"error": str(e)}
            yield f"data: {json.dumps(error_message)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", port=8080)
