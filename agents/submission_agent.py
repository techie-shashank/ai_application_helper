import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, ChatOpenAI

class SubmissionAgent:
    def __init__(self, gemini_api_key):
        self.headless = headless
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-2.5-flash"
        )

    def submit_application(self, submission_url: str, drafted_application: str):
        async def _run():
            agent = Agent(
                task=f"Go to {submission_url}, fill out the submission form using the following application text, and submit it. Return the content of the success page. Application: {drafted_application}",
                llm=ChatOpenAI(model=self.llm_model),
                headless=self.headless
            )
            result = await agent.run()
            return result
        return asyncio.run(_run())
