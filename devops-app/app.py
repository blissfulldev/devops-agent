import uuid
import streamlit as st
import httpx
import json
import os

# 1) Page config
st.set_page_config(page_title="DevOps Copilot", layout="wide")
st.title("🛠️ DevOps Multi‑Agent Copilot")

# Base URL of your FastAPI server
API_BASE = "http://localhost:8080"

# 2) Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "checkpoint_ns" not in st.session_state:
    st.session_state.checkpoint_ns = "devops_platform"
if "checkpoint_id" not in st.session_state:
    st.session_state.checkpoint_id = "main"

# Render chat history
for role, msg in st.session_state.history:
    if role == "assistant_image":
        st.chat_message("assistant").image(msg, caption="Generated Diagram")
    else:
        st.chat_message(role).write(msg)

# 3) User input
if prompt := st.chat_input("What would you like to build?"):
    # Display user message
    st.session_state.history.append(("user", prompt))
    st.chat_message("user").write(prompt)

    # Build payload
    payload = {
        "input": prompt,
        "thread_id": st.session_state.thread_id,
        "checkpoint_ns": st.session_state.checkpoint_ns,
        "checkpoint_id": st.session_state.checkpoint_id,
    }

    # 4) Stream assistant response
    with st.chat_message("assistant"):
        text_pl = st.empty()
        img_pl  = st.empty()
        assistant_response_text = ""
        final_image_url = None

        try:
            with httpx.stream(
                "POST",
                f"{API_BASE}/stream",
                json=payload,
                timeout=120.0,
            ) as response:
                response.raise_for_status()

                for line in response.iter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    data = json.loads(line.removeprefix("data: "))

                    # Streamed text
                    if text_chunk := data.get("text"):
                        assistant_response_text += text_chunk
                        text_pl.markdown(assistant_response_text + "▌")

                    # Diagram image URL
                    if rel_url := data.get("image_url"):
                        # Build full URL (serve path from FastAPI /static)
                        full_url = f"{API_BASE}{rel_url}"
                        final_image_url = full_url
                        img_pl.image(full_url, caption="Generated Diagram")

            # Final render without cursor
            text_pl.markdown(assistant_response_text)

            # Save to history
            if assistant_response_text:
                st.session_state.history.append(("assistant", assistant_response_text))
            if final_image_url:
                st.session_state.history.append(("assistant_image", final_image_url))

        except httpx.ReadTimeout:
            st.error("The request timed out. The agent system is taking too long to respond.")
        except httpx.HTTPStatusError as e:
            st.error(f"An HTTP error occurred: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
