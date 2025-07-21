from typing import Literal
from langgraph.types import Command
from langchain.schema import AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from utils.system_prompts import TERRAFORM_AGENT_SYSTEM_PROMPT
from utils.executor_builder import build_function_calling_executor

async def get_terraform_agent(llm):
    client = MultiServerMCPClient({
        "terraform_mcp": {
            "transport": "sse",
            "url": "http://localhost:8002/sse"   # terraform MCP HTTP endpoint
        }
    })
    tools = await client.get_tools()

    executor = build_function_calling_executor(llm, tools)

    async def terraform_agent(state) -> Command[Literal["supervisor_agent"]]:
        query = state["messages"][-1].content.strip() if state["messages"] else ""

        if not query:
            return Command(
                goto="supervisor_agent",
                update={"messages": [AIMessage(content="No input provided to diagram agent.")]}
            )
        prompt_query = f"{TERRAFORM_AGENT_SYSTEM_PROMPT}\n\n{query}"
        result = await executor.arun(input=prompt_query)
        return Command(
            goto="supervisor_agent",
            update={"messages": [AIMessage(content=str(result))]}
        )

    return terraform_agent
