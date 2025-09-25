from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
import os
import json


load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("CROQ_API_KEY")  # Get the API key from environment

class Chain:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
    
        """
        ### SCRAPED TEXT FROM WEBSITE:
        {Page_data}
        ### INSTRUCTIONS
        Do not include any preamble, explanations, or extra text outside the JSON.

        The JSON must have the following top-level keys:

        role → The exact job title or position mentioned.

        description → A concise summary (2–4 sentences) capturing the company context and key responsibilities of the role.

        skills → technical skills → tools, technologies, or domain-specific expertise required, soft_skills → interpersonal, communication, leadership, or problem-solving skills.

        experience → years of experience, industry background, or domain-specific requirements.

        certifications → licenses, degrees, or certifications explicitly mentioned.

        location → city, state, country, or remote work options.

        salary → salary range, pay scale, or compensation details if provided.

        other_requirements → any additional conditions such as language proficiency, travel readiness, or work eligibility.

        Output Requirements:

        Return valid JSON only. A JSON object with scope for multiple jobs if applicable.

        Preserve numerical values, conditions, and qualifications exactly as stated in the job description.

        Do not summarize or generalize—extract details as given.

        Do not include any  '''json or ``` marks in your response.

        Exclude promotional or marketing text that is not directly related to requirements.
            """
        )

        chain_extract = prompt_extract | self.llm
        response = chain_extract.invoke(input={"Page_data": cleaned_text})
        response = json.loads(response.content)

        print(response)
        return response

    def write_email(self, job_details, links):
        # This function will take job details and links to portfolio and generate a cold email
        print("Generating email with job details:", job_details)
        prompt_email = PromptTemplate.from_template("""
        ### JOB DESCRIPTION
        {job_description}
        
        ### INSTRUCTION
        You are Anand Senior consultant at Antartica Inc, Focused on AI solutions to the real world business problems.
        Provided the Job Description for different AI roles, Create a Cold Message indicating the willingness to offer 
        soluctions for the client requirements. You can add the following portfolio's to guide the client to the works we are done.
        link list (a dictionary of links) : {link_list}
        Make a very elaborate and detailed professional mail that should address their needs by giving priority to the business goals,
        cost optimization, efficiency.
        Add no Preamble
        ##EMAIL (NO PREAMBLE)""")
        chain_extract = prompt_email | self.llm
        response = chain_extract.invoke(input={"job_description": job_details, "link_list": links})

        print(response.content)
        return response.content