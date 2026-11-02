import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            docs = loader.load()
            if not docs:
                st.error("No content could be loaded from the provided URL.")
                return
            data = clean_text(docs.pop().page_content)

            # Ensure portfolio vectors exist
            portfolio.add_to_vector_store()

            jobs = llm.extract_jobs(data)
            # Normalize response to a list if needed
            if not isinstance(jobs, list):
                jobs = [jobs]

            for job in jobs:
                skills = job.get('skills', []) if isinstance(job, dict) else []
                links = portfolio.query_portfolio(skills)
                email = llm.write_email(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

