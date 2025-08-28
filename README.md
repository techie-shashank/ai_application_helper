# AI Application Helper


This project orchestrates multi-agent workflows for automating application drafting and submission using LLMs and browser automation. It features:

## Browser Automation

This project uses [browser-use](https://github.com/browser-use/browser-use) for browser automation. The submission agent leverages browser-use to:
- Open and interact with web forms
- Fill out and submit applications automatically
- Extract content from success pages after submission

Make sure to follow the [browser-use setup instructions](https://github.com/browser-use/browser-use#installation) for your platform. The browser-use package is a core dependency for the submission agent's automation capabilities.

- **Multi-agent workflow** for data ingestion, research, writing, validation, and submission
- **MCP server** exposing the submission agent as a tool
- **LangChain/LangGraph integration** for agent-tool orchestration
- **Streamlit UI** for user interaction

## Features
- Summarize user profile and target entity
- Draft and validate applications (SOP, job, etc.)
- Submit applications via browser automation
- Modular agents for each workflow step
- MCP server for tool interoperability

## Structure
```
main.py                  # Entry point
ui.py                    # Streamlit UI
requirements.txt         # Dependencies
agents/                  # Agent implementations
workflows/               # Workflow orchestration
submission_mcp_server.py # MCP server for submission agent
```

## Usage

### 1. Install dependencies
```sh
pip install -r requirements.txt
```

### 2. Set up environment variables
Create a `.env` file with your API keys (e.g., for Gemini):
```
GEMINI_API_KEY=your_key_here
```

### 3. Run the MCP server (for submission agent)
```sh
python submission_mcp_server.py
```

### 4. Run the Streamlit UI
```sh
streamlit run ui.py
```

### 5. (Optional) Use the SubmissionAgent directly
You can invoke the submission agent as a tool from other agents or scripts using the MCP protocol.

## Notes

## Example Workflow

1. **User provides profile sources and a target entity (e.g., university or company).**
2. **The workflow loads and summarizes the profile data.**
3. **Entity research agent gathers and summarizes information about the target.**
4. **Writing agent drafts an application (e.g., SOP) using the summaries.**
5. **Validation agent reviews the draft for quality and relevance.**
6. **Submission agent (via MCP server) fills and submits the application form using browser automation.**

**Example Python usage:**
```python
from workflows.application_workflow import ApplicationWorkflow

workflow = ApplicationWorkflow(gemini_api_key="your_gemini_key")
profile_sources = ["data/my_cv.pdf"]
user_prompt = "Apply to the MS program at Example University."
submission_url = "https://exampleuniversity.edu/apply"

result = workflow.run(profile_sources, user_prompt, submission_url)
print(result["application"])
print(result["submission_result"])
```

---
- Make sure only one MCP server instance runs on a given port.
- All logs and print statements in the MCP server should go to stderr, not stdout.
- The project supports both direct tool invocation and agent-based orchestration.

