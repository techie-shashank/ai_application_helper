# SubmissionAgent that connects to the MCP server and exposes submit_application

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from langchain_mcp_adapters.tools import load_mcp_tools

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

class SubmissionAgent:
    def __init__(self, gemini_api_key, server_path=None):
        # URL to your running MCP server's streamable-http endpoint
        self.server_url = server_path or "http://127.0.0.1:8000/mcp"
        self.gemini_api_key = gemini_api_key

    async def submit_application_async(self, form_url, submission_data):
        async with streamablehttp_client(self.server_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                tool = None
                for t in tools:
                    if t.name == "submit_application":
                        tool = t
                        break
                if tool is None:
                    raise RuntimeError("submit_application tool not found on MCP server")
                response = await tool.ainvoke({
                    "form_url": form_url,
                    "submission_data": submission_data
                })
                return response

    def submit_application(self, form_url, submission_data):
        return asyncio.run(self.submit_application_async(form_url, submission_data))
