"""
Entity Research Agent: Gathers and summarizes information about the target entity (company, university, etc.)
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains.summarize import load_summarize_chain

class EntityResearchAgent:
    def __init__(self, gemini_api_key):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-2.5-flash"
        )

    def research_and_summarize(self, prompt_or_url):
        # If input looks like a URL, use WebBaseLoader; otherwise, use Gemini LLM for research
        if isinstance(prompt_or_url, str) and prompt_or_url.strip().lower().startswith("http"):
            from langchain.document_loaders import WebBaseLoader
            loader = WebBaseLoader(prompt_or_url)
            docs = loader.load()
            text = "\n".join([doc.page_content for doc in docs])
            summary_prompt = (
                "Summarize the following entity information for application writing. Also, if there is an application submission URL, extract and return it as JSON in the format: {\"summary\": \"...\", \"submission_url\": \"...\"}:\n" + text
            )
            response = self.llm([HumanMessage(content=summary_prompt)])
            try:
                import json
                result = json.loads(response.content if hasattr(response, 'content') else response)
                return result
            except Exception:
                return {"summary": response.content if hasattr(response, 'content') else response, "submission_url": ""}
        else:
            # Use Gemini to research and summarize based on the prompt, and find the submission URL
            research_prompt = (
                "You are an expert research assistant. Given the following prompt, research the entity (such as a university, company, or organization) using your knowledge and the internet, and provide a concise summary of the entity relevant for an application. "
                "Also, find and return the most likely application submission URL (for SOP/job/thesis/etc.) if available. Respond in JSON as: {\"summary\": \"...\", \"submission_url\": \"...\"}.\n\nPrompt:\n" + prompt_or_url
            )
            response = self.llm([HumanMessage(content=research_prompt)])
            try:
                import json
                result = json.loads(response.content if hasattr(response, 'content') else response)
                return result
            except Exception:
                return {"summary": response.content if hasattr(response, 'content') else response, "submission_url": ""}

class ApplicationWorkflow:
    def __init__(self, llm, data_agent, entity_agent, writer_agent, validator_agent, extract_prompt_template):
        self.llm = llm
        self.data_agent = data_agent
        self.entity_agent = entity_agent
        self.writer_agent = writer_agent
        self.validator_agent = validator_agent
        self.extract_prompt_template = extract_prompt_template

    def run(self, profile_sources, user_prompt):
        # Step 1: Extract only application_type from user_prompt
        extract_prompt = self.extract_prompt_template.format(user_prompt=user_prompt)
        import json
        extract_response = self.llm([HumanMessage(content=extract_prompt)])
        try:
            extract_json = json.loads(extract_response.content if hasattr(extract_response, 'content') else extract_response)
            application_type = extract_json.get("application_type", "SOP")
        except Exception:
            application_type = "SOP"

        print(f"[Extracted] application_type: {application_type}")

        print("[1] Summarizing profile data...")
        profile_summary = self.data_agent.load_and_summarize(profile_sources)
        print("[2] Researching entity...")
        # Pass the user prompt to the entity agent for autonomous research
        entity_info = self.entity_agent.research_and_summarize(user_prompt)
        entity_summary = entity_info.get("summary", "")
        submission_url = entity_info.get("submission_url", "")
        print("[3] Drafting application...")
        application = self.writer_agent.draft_application(profile_summary, entity_summary, application_type)
        print("[4] Validating application...")
        review = self.validator_agent.validate_application(application, profile_summary, entity_summary)
        return {
            "profile_summary": profile_summary,
            "entity_summary": entity_summary,
            "submission_url": submission_url,
            "application": application,
            "review": review
        }
