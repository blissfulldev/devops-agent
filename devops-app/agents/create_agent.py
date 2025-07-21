from langgraph.graph import MessagesState
from langchain.schema.runnable import Runnable
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from typing import List
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.agents import initialize_agent, AgentType

def create_agent(llm, tools: List[Tool], prompt: str) -> Runnable:
    # Initialize a ReAct-style agent manually using LangChain
    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )

    def invoke_agent(state: MessagesState) -> MessagesState:
        history = state["messages"]
        input_message = history[-1].content if history else ""

        # Prepend custom system message
        input_with_system_prompt = f"{prompt}\n\n{input_message}"

        response = agent_executor.run(input_with_system_prompt)
        new_messages = history + [{"role": "assistant", "content": response}]
        return {"messages": new_messages}

    return Runnable.from_fn(invoke_agent)

def build_agent_executor(llm, tools, system_prompt):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    prompted_llm = prompt | llm

    return initialize_agent(
        tools,
        prompted_llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True
    )

