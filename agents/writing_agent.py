"""
Writing Agent: Drafts the application using LLMs and prompt templates
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.prompts import PromptTemplate

class WritingAgent:
    def __init__(self, gemini_api_key):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-2.5-flash"
        )
        self.prompt_template = PromptTemplate(
            input_variables=["profile_summary", "entity_summary", "application_type"],
            template="""
You are an expert application writer. Write a {application_type} application using the following information.\n\nProfile Summary:\n{profile_summary}\n\nEntity Summary:\n{entity_summary}\n\nDraft the application in a professional, relevant, and personalized manner.\n\nApplication:\n"""
        )

    def draft_application(self, profile_summary, entity_summary, application_type="SOP"):
        prompt = self.prompt_template.format(
            profile_summary=profile_summary,
            entity_summary=entity_summary,
            application_type=application_type
        )
        response = self.llm([HumanMessage(content=prompt)])
        return response.content if hasattr(response, 'content') else response

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
