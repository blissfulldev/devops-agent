from typing import Literal
from langgraph.types import Command
from langchain.schema import AIMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.system_prompts import DIAGRAM_AGENT_SYSTEM_PROMPT
from utils.executor_builder import build_function_calling_executor

async def get_diagram_agent(llm):
    client = MultiServerMCPClient({
        "diagram_mcp": {
            "transport": "sse",
            "url": "http://localhost:8001/sse"   # diagram MCP HTTP endpoint
        }
    })
    tools = await client.get_tools()

    executor = build_function_calling_executor(llm, tools)

    async def diagram_agent(state) -> Command[Literal["supervisor_agent"]]:
        last_message = state.get("messages", [])[-1] if state.get("messages") else None
        query = last_message.content.strip() if last_message and last_message.content else ""

        print(f"[DEBUG] diagram_agent query: '{query}'")  # <--- Log the actual input

        if not query:
            return Command(
                goto="supervisor_agent",
                update={"messages": [AIMessage(content="Empty input. Nothing to process.")]}
            )

        prompt_query = f"{DIAGRAM_AGENT_SYSTEM_PROMPT.strip()}\n\n{query}"

        # Ensure we wrap input into a proper HumanMessage
        result = await executor.ainvoke([HumanMessage(content=prompt_query)])

        return Command(
            goto="supervisor_agent",
            update={"messages": [AIMessage(content=str(result))]}
        )

    return diagram_agent
