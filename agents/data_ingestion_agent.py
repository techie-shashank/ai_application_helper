"""
Data Ingestion Agent: Loads and summarizes user profile data (CV, website, reports, etc.)
"""
from langchain.document_loaders import TextLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader
import os

class DataIngestionAgent:
    def __init__(self, gemini_api_key):
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=gemini_api_key,
            model="gemini-2.5-flash"
        )

    def load_and_summarize(self, sources):
        docs = []
        for src in sources:
            if src.startswith('http'):
                loader = WebBaseLoader(src)
            elif src.lower().endswith('.pdf'):
                loader = PyPDFLoader(src)
            else:
                loader = TextLoader(src)
            docs.extend(loader.load())
        # Split and summarize
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
        split_docs = text_splitter.split_documents(docs)
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        summary = chain.run(split_docs)
        return summary
