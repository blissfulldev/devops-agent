from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

from utils.system_prompts import (
    DIAGRAM_AGENT_SYSTEM_PROMPT,
    PLANNING_AGENT_SYSTEM_PROMPT,
    TERRAFORM_AGENT_SYSTEM_PROMPT,
)
from tools.write_project_to_disk import write_project_to_disk


load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

def planning_agent_factory(tools):
    return create_react_agent(llm, tools=tools, prompt=PLANNING_AGENT_SYSTEM_PROMPT, name="planning_agent")

def diagram_agent_factory(tools, project_root: str):
    formatted_prompt = DIAGRAM_AGENT_SYSTEM_PROMPT.format(project_root=project_root)
    return create_react_agent(llm, tools=tools, prompt=formatted_prompt, name="diagram_agent")

def terraform_agent_factory(tools, project_root: str):
    all_tools = tools + [write_project_to_disk]
    formatted_prompt = TERRAFORM_AGENT_SYSTEM_PROMPT.format(project_root=project_root)
    return create_react_agent(llm, tools=all_tools, prompt=formatted_prompt, name="terraform_agent")
