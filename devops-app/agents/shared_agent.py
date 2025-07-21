from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from utils.system_prompts import PLANNING_AGENT_SYSTEM_PROMPT, DIAGRAM_AGENT_SYSTEM_PROMPT, TERRAFORM_AGENT_SYSTEM_PROMPT
from dotenv import load_dotenv
from tools import write_project_to_disk


load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def planning_agent_factory(tools):
    return create_react_agent(llm, tools=tools, prompt=PLANNING_AGENT_SYSTEM_PROMPT, name="planning_agent")

def diagram_agent_factory(tools):
    return create_react_agent(llm, tools=tools, prompt=DIAGRAM_AGENT_SYSTEM_PROMPT, name="diagram_agent")

def terraform_agent_factory(tools):
    all_tools=tools+[write_project_to_disk]
    return create_react_agent(llm, tools=tools, prompt=TERRAFORM_AGENT_SYSTEM_PROMPT, name="terraform_agent")
