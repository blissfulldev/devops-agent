import os
from typing import Literal, Optional, List, Union
from pydantic import BaseModel
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage, BaseMessage

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt
from langgraph_supervisor import create_supervisor

from agents.shared_agent import llm, planning_agent_factory, diagram_agent_factory, terraform_agent_factory
from utils.system_prompts import SUPERVISOR_AGENT_SYSTEM_PROMPT

# 1) Typed state
class GraphState(BaseModel):
    input: str
    messages: List[BaseMessage] = []
    next_agent: Optional[str] = None
    approved: Optional[bool] = None
    awaiting_approval: bool = False  # Add this flag
    command: Optional[str] = None

    class Config:
        # we no longer store complex types here
        arbitrary_types_allowed = True

# 2) SupervisorStep schema
class SupervisorStep(BaseModel):
    next_agent: Literal["planning_agent", "diagram_agent", "terraform_agent", "__end__"]

async def create_graph():
    # workspace
    here = os.path.dirname(__file__)
    workspace = os.path.join(here, "..", "workspace")
    os.makedirs(workspace, exist_ok=True)

    # fetch MCP tools
    core_tools = await MultiServerMCPClient({
        "core_mcp": {"transport": "streamable_http", "url": "http://localhost:8000/mcp"}
    }).get_tools()
    diag_tools = await MultiServerMCPClient({
        "diagram_mcp": {"transport": "streamable_http", "url": "http://localhost:8001/mcp"}
    }).get_tools()
    tf_tools = await MultiServerMCPClient({
        "terraform_mcp": {"transport": "streamable_http", "url": "http://localhost:8002/mcp"}
    }).get_tools()

    # build child agents
    planning_agent  = planning_agent_factory(core_tools)
    diagram_agent   = diagram_agent_factory(diag_tools, project_root=workspace)
    terraform_agent = terraform_agent_factory(tf_tools, project_root=workspace)

    # supervisor (selects next_agent)
    supervisor_agent = create_supervisor(
        agents=[planning_agent, diagram_agent, terraform_agent],
        model=llm,
        prompt=SUPERVISOR_AGENT_SYSTEM_PROMPT,
        response_format=SupervisorStep
    ).compile()

    # helper to normalize input->messages
    def input_cleaner(state: GraphState) -> dict:
        cleaned = state.input.strip()
        # Initialize messages with user's input
        messages = [HumanMessage(content=cleaned)]
        return {
            "input": cleaned,
            "messages": messages,
            "next_agent": None,
            "approved": None
        }


    # interrupt for human approval
    def ask_approval(state: GraphState) -> Command:
        return interrupt({
            "message": f"Supervisor wants to run `{state.next_agent}`. Approve?",
            "next_agent": state.next_agent
        })

    # after resume, branch to child or back to supervisor
    def approval_handler(state: GraphState) -> Union[Command, dict]:
        """Handle the approval response after interrupt"""
        # If we haven't asked for approval yet, or are still waiting
        if not hasattr(state, 'approved') or state.approved is None:
            return interrupt({
                "message": f"Supervisor wants to run `{state.next_agent}`. Approve?",
                "next_agent": state.next_agent,
                "requires_input": True
            })
        
        # We have an answer, clear the flags
        state.awaiting_approval = False
        
        if state.approved:
            logger.debug(f"✅ Approved: going to {state.next_agent}")
            return Command(goto=state.next_agent)
        else:
            logger.debug("❌ Rejected: going back to supervisor")
            return Command(goto="supervisor", update={
                "approved": None,
                "awaiting_approval": False
            })

    # post‐processor (after child agent finishes)
    def post_processor(state: GraphState) -> dict:
        return {
            "input": state.input,
            "messages": state.messages or [],
            "awaiting_approval": state.awaiting_approval,
            "approved": state.approved
        }

    # --- assemble the StateGraph ---
    builder = StateGraph(GraphState)

    # nodes
    builder.add_node("input_cleaner", input_cleaner)
    builder.add_node("supervisor",    supervisor_agent)
    builder.add_node("approval_handler", approval_handler)
    builder.add_node("planning_agent",    planning_agent)
    builder.add_node("diagram_agent",     diagram_agent)
    builder.add_node("terraform_agent",   terraform_agent)
    builder.add_node("post_processor", post_processor)

    # edges
    builder.set_entry_point("input_cleaner")
    builder.add_edge("input_cleaner",  "supervisor")
    
    # Add conditional routing after supervisor
    def needs_approval(state: GraphState) -> bool:
        """Check if the next agent requires approval"""
        result = state.next_agent in ["diagram_agent", "terraform_agent"]
        logger.debug(f"🔍 needs_approval check: next_agent='{state.next_agent}', needs_approval={result}")
        return result

    builder.add_conditional_edges(
        "supervisor",
        needs_approval,
        {
            True: "approval_handler",
            False: "planning_agent"
        }
    )

    # Add edges from approval handler to agents
    builder.add_edge("approval_handler", "planning_agent")
    builder.add_edge("approval_handler", "diagram_agent")
    builder.add_edge("approval_handler", "terraform_agent")
    builder.add_edge("approval_handler", "supervisor")  # For rejection case

    # Add edges to post_processor
    builder.add_edge("planning_agent",  "post_processor")
    builder.add_edge("diagram_agent",   "post_processor")
    builder.add_edge("terraform_agent", "post_processor")
    builder.add_edge("post_processor",  END)

    return builder.compile(checkpointer=MemorySaver())
