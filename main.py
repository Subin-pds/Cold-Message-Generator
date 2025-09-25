#Importing Libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import json

def create_streamlit_app(llm, portfolio, clean_text):
    # --- UI Header ---
    st.title("📧 Cold Message Generator")
    st.write("Turn job postings into personalized cold emails to reach out to companies.")

    # --- Input Section ---
    job_url = st.text_input("🔗 Enter the Job Description URL", placeholder="Paste job description link here...")

    if st.button("Generate Cold Email"):
        if job_url.strip():
            try:
                pf = Portfolio()
                loader = WebBaseLoader([job_url])
                data = clean_text(loader.load().pop().page_content)
                print(data)
                pf.add_to_vector_store()
                ch = Chain()
                jobs = ch.extract_jobs(data)
                print(jobs)
                skills = jobs['skills']['technical_skills']
                job_description = jobs['description']
                skills = " ".join(skills)
                print("Skills String", skills)
                links = pf.query_portfolio(skills)
                link_list = [link['links'] for link in links if 'links' in link]
                print(type(link_list))
                print("Link List", link_list)
                link_list = " , ".join(link_list)
                print("Link List String", link_list)
                email = ch.write_email(job_description, link_list)
                print("Generated Email", email)
                st.code(email, language='markdown')


            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ =="__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Message Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)