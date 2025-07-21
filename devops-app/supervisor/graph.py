from langgraph.checkpoint.memory import MemorySaver
from agents.shared_agent import llm
from agents.shared_agent import planning_agent_factory, diagram_agent_factory, terraform_agent_factory
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.system_prompts import SUPERVISIOR_AGENT_SYSTEM_PROMPT
from langgraph_supervisor import create_supervisor 
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """The state for the supervisor graph."""
    messages: Annotated[List[BaseMessage], operator.add]
    is_last_step: bool
    remaining_steps: int

async def create_graph():
    # 1. Fetch MCP tools
    core_tools = await MultiServerMCPClient({"core_mcp": {"transport":"sse","url":"http://localhost:8000/sse"}}).get_tools()
    diag_tools = await MultiServerMCPClient({"diagram_mcp": {"transport":"sse","url":"http://localhost:8001/sse"}}).get_tools()
    tf_tools   = await MultiServerMCPClient({"terraform_mcp": {"transport":"sse","url":"http://localhost:8002/sse"}}).get_tools()

    # 2. Build agent functions
    planning_agent  = planning_agent_factory(core_tools)
    diagram_agent   = diagram_agent_factory(diag_tools)
    terraform_agent = terraform_agent_factory(tf_tools)
    # Supervisor: use prebuilt react too
    supervisor_agent = create_supervisor(
        agents=[planning_agent,diagram_agent,terraform_agent],
        model=llm,
        state_schema = AgentState,
        prompt=SUPERVISIOR_AGENT_SYSTEM_PROMPT,
        add_handoff_back_messages=True,
        output_mode="full_history",
        ).compile(checkpointer=MemorySaver())

    return supervisor_agent

# graph = asyncio.run(create_graph())
