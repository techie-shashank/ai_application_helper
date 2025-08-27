"""
LangGraph workflow to orchestrate the multi-agent process
"""
from agents.data_ingestion_agent import DataIngestionAgent
from agents.entity_research_agent import EntityResearchAgent
from agents.writing_agent import WritingAgent
from agents.validation_agent import ValidationAgent
from agents.submission_agent import SubmissionAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage

class ApplicationWorkflow:
    def __init__(self, gemini_api_key):
        self.data_agent = DataIngestionAgent(gemini_api_key)
        self.entity_agent = EntityResearchAgent(gemini_api_key)
        self.writer_agent = WritingAgent(gemini_api_key)
        self.validator_agent = ValidationAgent(gemini_api_key)
        self.submission_agent = SubmissionAgent(headless=True)
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-2.5-flash"
        )

    def run(self, profile_sources, user_prompt, submission_url):
        # Step 1: Extract application_type and submission_url from user_prompt if not provided
        if not submission_url:
            extract_prompt = (
                "Given the following user prompt, extract as JSON: "
                '{"application_type": "...", "submission_url": "..."}. '
                "The 'submission_url' should be the URL where the application is to be submitted. "
                "If no submission URL is found, use an empty string.\n\nPrompt:\n" + user_prompt
            )
            import json
            extract_response = self.llm([HumanMessage(content=extract_prompt)])
            try:
                extract_json = json.loads(extract_response.content if hasattr(extract_response, 'content') else extract_response)
                application_type = extract_json.get("application_type", "SOP")
                submission_url = extract_json.get("submission_url", "")
            except Exception:
                application_type = "SOP"
                submission_url = ""
        else:
            # Only extract application_type from prompt if submission_url is provided by user
            extract_prompt = (
                "Given the following user prompt, extract as JSON: "
                '{"application_type": "..."}. '
                "Prompt:\n" + user_prompt
            )
            import json
            extract_response = self.llm([HumanMessage(content=extract_prompt)])
            try:
                extract_json = json.loads(extract_response.content if hasattr(extract_response, 'content') else extract_response)
                application_type = extract_json.get("application_type", "SOP")
            except Exception:
                application_type = "SOP"

        print(f"[Extracted] application_type: {application_type}, submission_url: {submission_url}")

        print("[1] Summarizing profile data...")
        profile_summary = self.data_agent.load_and_summarize(profile_sources)
        print("[2] Researching entity...")
        # Pass the user prompt to the entity agent for autonomous research
        entity_info = self.entity_agent.research_and_summarize(user_prompt)
        entity_summary = entity_info.get("summary", "")
        # If no submission_url found in prompt or user, use the one from entity agent
        if not submission_url:
            submission_url = entity_info.get("submission_url", "")
        print("[3] Drafting application...")
        application = self.writer_agent.draft_application(profile_summary, entity_summary, application_type)
        print("[4] Validating application...")
        review = self.validator_agent.validate_application(application, profile_summary, entity_summary)
        print("[5] Submitting application via browser-use...")
        submission_result = None
        if submission_url:
            submission_result = self.submission_agent.submit_application(submission_url, application)
        return {
            "profile_summary": profile_summary,
            "entity_summary": entity_summary,
            "submission_url": submission_url,
            "application": application,
            "review": review,
            "submission_result": submission_result
        }
