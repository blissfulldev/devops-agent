import uuid
import streamlit as st
import httpx
import json

# 1) Page config
st.set_page_config(page_title="DevOps Copilot", layout="wide")
st.title("🛠️ DevOps Multi‑Agent Copilot")

# 2) Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
# Generate a thread_id once per user session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
# You can also set a fixed namespace if you like
if "checkpoint_ns" not in st.session_state:
    st.session_state.checkpoint_ns = "devops_platform"
# And a checkpoint_id if needed
if "checkpoint_id" not in st.session_state:
    st.session_state.checkpoint_id = "main"

# Render chat history from session state
for role, msg in st.session_state.history:
    st.chat_message(role).write(msg)


def stream_generator(response):
    """Generator to yield text chunks from the SSE response and build the full message."""
    assistant_response = ""
    for line in response.iter_lines():
        if not line or not line.startswith("data:"):
            continue
        try:
            chunk = json.loads(line.removeprefix("data: "))
            text_chunk = chunk.get("text", "")
            assistant_response += text_chunk
            yield text_chunk
        except json.JSONDecodeError:
            continue  # Ignore invalid JSON chunks
    # Once streaming is complete, add the final message to history
    st.session_state.history.append(("assistant", assistant_response))


# 3) Use st.chat_input for a better user experience
if prompt := st.chat_input("What would you like to build?"):
    # Add user message to history and display it
    st.session_state.history.append(("user", prompt))
    st.chat_message("user").write(prompt)

    # Build payload
    payload = {
        "input": prompt,
        "thread_id": st.session_state.thread_id,
        "checkpoint_ns": st.session_state.checkpoint_ns,
        "checkpoint_id": st.session_state.checkpoint_id,
    }

    # Display assistant response in a streaming fashion
    with st.chat_message("assistant"):
        try:
            # 4) Call FastAPI SSE endpoint with an increased timeout
            with httpx.stream(
                "POST",
                "http://localhost:8080/stream",
                json=payload,
                timeout=120.0,  # Set a 120-second timeout
            ) as response:
                response.raise_for_status()  # Raise an exception for bad status codes
                # Use st.write_stream to render the response as it comes in
                st.write_stream(stream_generator(response))
        except httpx.ReadTimeout:
            st.error("The request timed out. The agent system is taking too long to respond.")
        except httpx.HTTPStatusError as e:
            st.error(f"An HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
