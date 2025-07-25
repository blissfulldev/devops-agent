from langgraph.checkpoint.memory import MemorySaver
from agents.shared_agent import llm
from agents.shared_agent import planning_agent_factory, diagram_agent_factory, terraform_agent_factory
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.system_prompts import SUPERVISOR_AGENT_SYSTEM_PROMPT
from langgraph_supervisor import create_supervisor 
from typing import Any, Dict, Literal, Optional, TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableLambda
import os
import operator
from pydantic import BaseModel
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    """The state for the supervisor graph."""
    messages: Annotated[List[BaseMessage], operator.add]
    is_last_step: bool
    remaining_steps: int

class GraphState(BaseModel):
    input: str
    thread_id: Optional[str] = None
    checkpoint_ns: Optional[str] = None
    checkpoint_id: Optional[str] = None
    planning_output: Optional[Dict] = {}
# --- Dummy Input Cleaner Node ---
def input_cleaner_node(state: dict) -> dict:
    print("🔹 [input_cleaner] Received input:", state.input)
    cleaned_input = state.input
    return {"input": cleaned_input}


# --- Dummy Post-Processor Node ---
def post_processor_node(state: dict) -> dict:
    print("🔹 [post_processor] Final output:", state.get("messages", []))
    return state  # In real use case, trigger webhook, CI/CD, etc.
class SupervisorStep(BaseModel):
    next_agent: Literal["planning_agent","diagram_agent","terraform_agent","__end__"]
async def create_graph():
    # Define and create the workspace directory relative to this file's location
    # This ensures a consistent path regardless of where the script is run from.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.join(current_dir, '..', 'workspace')
    os.makedirs(workspace_dir, exist_ok=True)

    # 1. Fetch MCP tools
    core_tools = await MultiServerMCPClient({"core_mcp": {"transport":"streamable_http","url":"http://localhost:8000/mcp"}}).get_tools()
    diag_tools = await MultiServerMCPClient({"diagram_mcp": {"transport":"streamable_http","url":"http://localhost:8001/mcp"}}).get_tools()
    tf_tools   = await MultiServerMCPClient({"terraform_mcp": {"transport":"streamable_http","url":"http://localhost:8002/mcp"}}).get_tools()

    # 2. Build agent functions
    planning_agent  = planning_agent_factory(core_tools)
    diagram_agent   = diagram_agent_factory(diag_tools, project_root=workspace_dir)
    terraform_agent = terraform_agent_factory(tf_tools, project_root=workspace_dir)
    # Supervisor: use prebuilt react too
    supervisor_agent = create_supervisor(
        agents=[planning_agent,diagram_agent,terraform_agent],
        model=llm,
        prompt=SUPERVISOR_AGENT_SYSTEM_PROMPT,
        response_format = SupervisorStep
        ).compile()
    builder = StateGraph(GraphState)

    builder.add_node("input_cleaner", RunnableLambda(input_cleaner_node))
    builder.add_node("supervisor", supervisor_agent)
    builder.add_node("post_processor", RunnableLambda(post_processor_node))

    builder.set_entry_point("input_cleaner")
    builder.add_edge("input_cleaner", "supervisor")
    builder.add_edge("supervisor", "post_processor")
    builder.add_edge("post_processor", END)
    graph = builder.compile(checkpointer=MemorySaver())
    return graph

# graph = asyncio.run(create_graph())
