import json
from typing import Literal

from langgraph.types import Command
from langgraph.graph import END
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from utils.system_prompts import SUPERVISIOR_AGENT_SYSTEM_PROMPT

def get_supervisor_agent(llm: ChatGoogleGenerativeAI):
    # Build a prompt template that prepends the system message and then injects full history
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SUPERVISIOR_AGENT_SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages")
    ])
    chain = prompt | llm

    async def supervisor_agent(state) -> Command[Literal["planning_agent", "diagram_agent", "terraform_agent", END]]:
        # 1) Call Gemini with the full message history
        response = await chain.ainvoke({"messages": state["messages"]})
        text = response.content

        # 2) Append the supervisor's own message so the next agent sees it
        ai_msg = AIMessage(content=text)
        updated_history = state["messages"] + [ai_msg]

        # 3) Parse which agent to call next
        try:
            payload = json.loads(text)
            next_agent = payload.get("next_agent", "__end__")
        except (json.JSONDecodeError, TypeError):
            lower = text.lower()
            if "planning" in lower:
                next_agent = "planning_agent"
            elif "diagram" in lower:
                next_agent = "diagram_agent"
            elif "terraform" in lower:
                next_agent = "terraform_agent"
            else:
                next_agent = "__end__"

        # 4) If the supervisor decides to end, terminate the graph
        if next_agent == "__end__":
            return Command(goto=END, update={"messages": [ai_msg]})

        # 5) Otherwise route to the chosen agent, carrying along the updated messages
        return Command(goto=next_agent, update={"messages": [ai_msg]})

    return supervisor_agent
