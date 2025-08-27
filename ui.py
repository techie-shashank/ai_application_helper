"""
Streamlit UI for the AI Application Drafter
"""
import streamlit as st
import os
from dotenv import load_dotenv
from workflows.application_workflow import ApplicationWorkflow

st.set_page_config(page_title="AI Application Drafter", layout="wide")
st.title("Personalized AI SOP/Job/Thesis Application Drafter")

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

with st.form("input_form"):
    st.header("1. Upload Your Profile Data")
    uploaded_files = st.file_uploader("Upload your CV, project reports, etc.", accept_multiple_files=True)
    st.header("2. Enter Your Prompt")
    user_prompt = st.text_area("Describe your target (e.g., 'Draft an SOP for Stanford University Data Science program')")
    submission_url_input = st.text_input("Submission URL (optional, will override detected URL)")
    submitted = st.form_submit_button("Generate Application")

if submitted and (uploaded_files or user_prompt):
    # Save uploaded files to a temp directory
    profile_sources = []
    temp_dir = "data/temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join(temp_dir, file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        profile_sources.append(file_path)

    if not gemini_api_key:
        st.warning("Please provide your GEMINI_API_KEY in the .env file.")
    else:
        workflow = ApplicationWorkflow(gemini_api_key)
        with st.spinner("Processing..."):
            # Pass user_prompt and submission_url_input
            result = workflow.run(profile_sources, user_prompt, submission_url_input)

        st.subheader("Profile Summary")
        st.write(result["profile_summary"])
        st.subheader("Entity Summary")
        st.write(result["entity_summary"])
        if result.get("submission_url"):
            st.subheader("Submission URL")
            st.write(result["submission_url"])
        st.subheader("Drafted Application")
        st.write(result["application"])
        st.subheader("Validation Review")
        st.write(result["review"])
        if result.get("submission_result"):
            st.subheader("Submission Result")
            st.write(result["submission_result"])

elif submitted and not gemini_api_key:
    st.warning("Please provide at least one profile file or entity URL.")
