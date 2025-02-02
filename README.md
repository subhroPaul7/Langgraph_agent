# Agent Workflow Executor

## Overview
Agent Workflow Executor is an AI-powered research workflow tool that automates the process of gathering, analyzing, and structuring information using LangChain, LangGraph, and Streamlit. The system orchestrates multiple AI agents to research a given topic, extract relevant information, and generate structured outputs.

## Features
- **Automated Research Workflow:** Uses multiple AI agents for planning, selecting sources, reporting, reviewing, and generating a final structured response.
- **Google Search & Web Scraping:** Integrates Serper API for Google search and a web scraper to extract relevant information.
- **Modular Agent Design:** Agents include Planner, Selector, Reporter, Reviewer, Router, and Final Report Generator.
- **State Persistence:** Stores agent interactions using SQLite for checkpointing and continuity.
- **User-Friendly Interface:** Built with Streamlit to allow easy input and execution.

## Architecture
The system is built using:
- **LangChain & LangGraph:** For managing AI agents and workflow execution.
- **Streamlit:** For providing a simple user interface.
- **OpenAI / Groq API:** For LLM-powered processing.
- **SQLite Storage:** To persist state checkpoints.

### Agent Workflow
1. **PlannerAgent:** Analyzes the research question and generates a research plan.
2. **SelectorAgent:** Selects relevant sources from Serper API results.
3. **ReporterAgent:** Extracts insights from selected sources.
4. **ReviewerAgent:** Ensures the quality of extracted insights.
5. **RouterAgent:** Determines the next agent to process the information.
6. **FinalReportAgent:** Compiles a structured final response.
7. **EndNodeAgent:** Marks the completion of the workflow.

## Installation
### Prerequisites
- Python 3.9+
- Virtual environment (recommended)
- OpenAI / Groq API key
- Serper API key

### Setup
```bash
# Clone the repository
git clone https://github.com/your-username/agent-workflow-executor.git
cd agent-workflow-executor

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use 'venv\Scripts\activate'

# Install dependencies
pip install -r requirements.txt
```

## Configuration
Store API keys in Streamlit secrets:
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-openai-api-key"
GROQ_API_KEY = "your-groq-api-key"
SERPER_API_KEY = "your-serper-api-key"
```

## Running the App
```bash
streamlit run app.py
```

## Usage
1. Enter a research question in the input field.
2. Click **Run Workflow** to execute the research agents.
3. The structured output will be displayed as JSON.

## File Structure
```
agent-workflow-executor/
│── agent_graph/
│   ├── graph_module.py  # Defines the agent workflow
│── agents/
│   ├── agents.py  # Agent implementations
│── models/
│   ├── openai_models.py  # OpenAI/Groq API integration
│── prompts/
│   ├── prompts.py  # Agent prompts
│── states/
│   ├── state.py  # State management
│── tools/
│   ├── google_serper.py  # Google Search API wrapper
│   ├── basic_scraper.py  # Web scraping tool
│── app.py  # Streamlit app entry point
│── requirements.txt  # Dependencies
│── README.md  # Project documentation
```

#

