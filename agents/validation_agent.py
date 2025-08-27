"""
Validation Agent: Checks the draft for relevance, correctness, and quality
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.prompts import PromptTemplate

class ValidationAgent:
    def __init__(self, gemini_api_key):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-2.5-flash"
        )
        self.prompt_template = PromptTemplate(
            input_variables=["application_text", "profile_summary", "entity_summary"],
            template="""
You are an expert application reviewer. Review the following application for relevance, correctness, and completeness.\n\nApplication:\n{application_text}\n\nProfile Summary:\n{profile_summary}\n\nEntity Summary:\n{entity_summary}\n\nProvide feedback and highlight any mistakes or missing information.\n\nReview:\n"""
        )

    def validate_application(self, application_text, profile_summary, entity_summary):
        prompt = self.prompt_template.format(
            application_text=application_text,
            profile_summary=profile_summary,
            entity_summary=entity_summary
        )
        response = self.llm([HumanMessage(content=prompt)])
        return response.content if hasattr(response, 'content') else response
