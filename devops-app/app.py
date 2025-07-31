import uuid
import streamlit as st
import httpx
import json
import logging
from dataclasses import dataclass
from typing import Optional

# Add debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("streamlit_app")

st.set_page_config(page_title="DevOps Copilot", layout="wide")
st.title("🛠️ DevOps Multi‑Agent Copilot")

API_BASE = "http://localhost:8080"

@dataclass
class MessageChunk:
    text: str = ""
    image_url: Optional[str] = None
    is_complete: bool = False

# Session state initialization with debug
if "history" not in st.session_state:
    st.session_state.history = []
    logger.debug("🔄 Initialized empty history")
else:
    logger.debug(f"🔄 Existing history has {len(st.session_state.history)} messages")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    logger.debug(f"🔄 Created new thread_id: {st.session_state.thread_id}")

if "awaiting_approval" not in st.session_state:
    st.session_state.awaiting_approval = False
if "pending_interrupt" not in st.session_state:
    st.session_state.pending_interrupt = None
if "processing" not in st.session_state:
    st.session_state.processing = False
if "submitted_approval" not in st.session_state:
    st.session_state.submitted_approval = False

# Debug info in sidebar
with st.sidebar:
    st.write("**Debug Info**")
    st.write(f"Thread ID: {st.session_state.thread_id}")
    st.write(f"History length: {len(st.session_state.history)}")
    st.write(f"Awaiting approval: {st.session_state.awaiting_approval}")
    st.write(f"Submitted approval: {st.session_state.submitted_approval}")
    st.write(f"Processing: {st.session_state.processing}")
    if st.session_state.pending_interrupt:
        st.write(f"Pending interrupt: {st.session_state.pending_interrupt}")

# Show current history
logger.debug(f"📜 Rendering {len(st.session_state.history)} history items")
for i, (role, kind, content) in enumerate(st.session_state.history):
    logger.debug(f"📜 Item {i}: {role}/{kind}")
    if kind == "text":
        st.chat_message(role, avatar="🤖" if role == "assistant" else "🧑‍💻").write(content)
    elif kind == "image":
        st.chat_message("assistant", avatar="🤖").image(content, caption="Generated Diagram")

# Approval flow
if st.session_state.awaiting_approval and not st.session_state.submitted_approval:
    logger.debug("🤔 Showing approval form")
    interrupt = st.session_state.pending_interrupt
    
    # Show the interrupt message prominently
    st.warning(f"**Action Required:** {interrupt.get('message', 'Unknown interrupt')}")
    
    if interrupt.get("requires_input", False):
        st.info("Please approve or reject to continue:")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve", key="approve_btn", use_container_width=True, type="primary"):
                logger.debug("✅ User approved")
                st.session_state.submitted_approval = True
                st.session_state.approval_decision = True
                st.rerun()
        with col2:
            if st.button("❌ Reject", key="reject_btn", use_container_width=True):
                logger.debug("❌ User rejected")
                st.session_state.submitted_approval = True
                st.session_state.approval_decision = False
                st.rerun()

# Handle submitted approval/clarification
if st.session_state.get("submitted_approval", False):
    if hasattr(st.session_state, "approval_decision"):
        decision = st.session_state.approval_decision
        logger.debug(f"🔄 Processing approval decision: {decision}")
        
        # Add decision to history
        icon = "✅" if decision else "❌"
        status = "Approved" if decision else "Rejected"
        st.session_state.history.append(("user", "text", f"{icon} {status}"))
        logger.debug(f"📜 Added decision to history: {icon} {status}")
        
        # Reset approval state
        st.session_state.awaiting_approval = False
        st.session_state.pending_interrupt = None
        st.session_state.submitted_approval = False
        del st.session_state.approval_decision
        
        # Call resume endpoint and show response in real-time
        logger.debug("🔄 Calling /resume endpoint")
        
        # Create a new chat message container for the streaming response
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            accumulated_text = ""
            
            try:
                with httpx.stream(
                    "POST",
                    f"{API_BASE}/resume",
                    json={"thread_id": st.session_state.thread_id, "approved": decision},
                    timeout=120.0,
                ) as resp:
                    resp.raise_for_status()
                    
                    for line in resp.iter_lines():
                        if line.startswith("data: "):
                            data = json.loads(line[6:])
                            logger.debug(f"📡 Resume received: {data}")
                            
                            if data.get("text"):
                                accumulated_text += data["text"]
                                # Show streaming text with cursor
                                message_placeholder.markdown(accumulated_text + "▌")
                            
                            if data.get("done"):
                                # Remove cursor and finalize
                                message_placeholder.markdown(accumulated_text)
                                # Add to history
                                if accumulated_text:
                                    st.session_state.history.append(("assistant", "text", accumulated_text))
                                    logger.debug(f"📜 Added resume response to history: {len(accumulated_text)} chars")
                                break
                                
            except Exception as e:
                logger.error(f"❌ Resume failed: {e}")
                st.error(f"Resume failed: {e}")
        
        st.rerun()

# Chat input (only if not awaiting approval)
if not st.session_state.awaiting_approval:
    prompt = st.chat_input("What would you like to build?")
    if prompt:
        logger.debug(f"💬 User input: {prompt}")
        st.session_state.history.append(("user", "text", prompt))
        
        # Show user message
        st.chat_message("user", avatar="🧑‍💻").write(prompt)
        
        # Create assistant message container for streaming
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            accumulated_text = ""
            
            try:
                with httpx.stream(
                    "POST",
                    f"{API_BASE}/stream",
                    json={"input": prompt, "thread_id": st.session_state.thread_id},
                    timeout=120.0,
                ) as resp:
                    resp.raise_for_status()
                    
                    for line in resp.iter_lines():
                        if line.startswith("data: "):
                            data = json.loads(line[6:])
                            logger.debug(f"📡 Received: {data}")
                            
                            if "interrupt" in data:
                                logger.debug("🤔 Interrupt received, setting approval state")
                                st.session_state.pending_interrupt = data["interrupt"]
                                st.session_state.awaiting_approval = True
                                st.session_state.submitted_approval = False
                                
                                # Finalize current message before interrupt
                                if accumulated_text:
                                    message_placeholder.markdown(accumulated_text)
                                    st.session_state.history.append(("assistant", "text", accumulated_text))
                                
                                st.rerun()
                                break
                            
                            if data.get("text"):
                                accumulated_text += data["text"]
                                # Show streaming text with cursor
                                message_placeholder.markdown(accumulated_text + "▌")
                            
                            if data.get("done"):
                                # Remove cursor and finalize
                                message_placeholder.markdown(accumulated_text)
                                if accumulated_text:
                                    st.session_state.history.append(("assistant", "text", accumulated_text))
                                    logger.debug(f"📜 Added response to history: {len(accumulated_text)} chars")
                                break
                                
            except Exception as e:
                logger.error(f"❌ Stream failed: {e}")
                st.error(f"Stream failed: {e}")

# New conversation button
if st.button("🆕 Start New Conversation"):
    logger.debug("🔄 Starting new conversation")
    st.session_state.clear()
    st.rerun()
