"""
MCP server for SubmissionAgent using FastMCP (MCP protocol).
Exposes the submit_application tool for MCP clients.
"""

from mcp.server.fastmcp import FastMCP
from browser_use import Agent, ChatGoogle, ChatOllama

mcp = FastMCP("SubmissionAgent")

@mcp.tool()
async def submit_application(form_url, submission_data):
    """Submit an application form using the SubmissionAgent."""
    agent = Agent(
        task=f"""
            Using the following data, fill the form at {form_url}. Draft an answer which is less than 300 characters for each question.
            I'm repeating again, do not type answer with more than 300 characters for one question.

            Here is the data - 
            {submission_data}
        """,
        llm=ChatGoogle(model='gemini-2.5-flash')
    )
    result = await agent.run()
    return result


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
