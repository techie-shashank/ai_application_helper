"""
Main entry point for the AI Application Drafter
"""

import os
from dotenv import load_dotenv
from workflows.application_workflow import ApplicationWorkflow


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("Please set the OPENAI_API_KEY variable in your .env file.")

    # Example usage: update these paths/URLs as needed
    profile_sources = [
        "data/my_cv.txt",  # Path to your CV
        # "https://mywebsite.com",  # Your website (optional)
        # "data/project_report.txt",  # Any other file
    ]
    entity_url = "https://www.exampleuniversity.edu/about"  # Target entity URL
    application_type = "SOP"  # or "Job Application", "Thesis Application", etc.

    workflow = ApplicationWorkflow(openai_api_key)
    result = workflow.run(profile_sources, entity_url, application_type)

    print("\n--- Profile Summary ---\n", result["profile_summary"])
    print("\n--- Entity Summary ---\n", result["entity_summary"])
    print("\n--- Drafted Application ---\n", result["application"])
    print("\n--- Validation Review ---\n", result["review"])
