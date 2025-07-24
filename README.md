# LangGraph Multi-Agent DevOps App

This project implements a multi-agent system using LangGraph to create a "DevOps Copilot." The system is composed of a supervisor agent that delegates tasks to specialized agents for planning, diagramming, and Terraform operations.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10+
- Install GraphViz https://www.graphviz.org/

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone git@github.com:blissfulldev/devops-agent.git
cd DevOps-Platform
```

### 2. Set Up the Python Environment
```bash
# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Navigate to the application directory and install dependencies
cd devops-app
pip install poetry
poetry install
```

### 3. Configure Environment Variables
Create a `.env` file from the example template and add your API keys.
```bash
# Make sure you are in the `devops-app` directory
cp env.example .env
```
Now, open the `.env` file and add the necessary secret keys (e.g., `GOOGLE_API_KEY`).


## ▶️ Running the Application

The application consists of several services that must be run simultaneously. It is highly recommended to **open a new terminal for each step and activate venv in every terminal before running any command**.

### 1. Start the MCP Servers
These servers provide the specialized tools for each agent.

*   **Core MCP Server:**
    ```bash
    cd devops-app/mcp/aws-diagram-mcp-server/
    poetry install
    ```
    ```bash
    python -m mcp.core-mcp-server.server --transport streamable-http --host 0.0.0.0 --port 8000
    ```
*   **Diagraming MCP Server:**
    ```bash
    cd devops-app/mcp/aws-diagram-mcp-server/
    poetry install
    ```
    ```bash
    python -m mcp.aws-diagram-mcp-server.server --transport streamable-http --host 0.0.0.0 --port 8001
    ```
*   **Terraform MCP Server:**
    ```bash
    cd devops-app/mcp/terraform-mcp-server/
    poetry install
    ```

    ```bash
    python -m mcp.terraform-mcp-server.server --transport streamable-http --host 0.0.0.0 --port 8002
    ```

### 2. Start the FastAPI Backend
This server orchestrates the agents and provides the streaming API.
```bash
# From the `devops-app` directory
poetry run uvicorn server:app --host 0.0.0.0 --port 8080 --reload
```

### 3. Start the Streamlit Frontend
This is the user interface for interacting with the copilot.
```bash
# From the `devops-app` directory
streamlit run app.py
```
You can now access the chat interface at `http://localhost:8501`.
