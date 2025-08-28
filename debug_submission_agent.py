"""
Debug script for SubmissionAgent
"""

from agents.submission_agent import SubmissionAgent

if __name__ == "__main__":
    # Example arguments, update as needed for your use case
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdhHm9dtGxDj8Rrv8Zpr8qGDPpWfGtAVTADnPC0z7USP8C48w/viewform?usp=dialog"
    submission_data = "Hello world"
    try:
        agent = SubmissionAgent()
        result = agent.submit_application(form_url, submission_data)
        print("Submission Result:", result)
    except Exception as e:
        print("Error during submission:", e)
