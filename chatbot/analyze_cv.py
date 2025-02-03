import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import Any


def extract_cv_details(file_path: str) -> Any:
    """
    Extract details from a CV in PDF format.

    Args:
        file_path (str): The path to the PDF file containing the CV.

    Returns:
        Any: The extracted details formatted according to the defined output structure.
    """

    loader = PyPDFLoader(file_path)
    cv = loader.load()

    prompt = ChatPromptTemplate.from_template(
        """
        Extract the following details from the CV. If not provided, indicate that the information is not given:

        1. Name (as per passport)
        2. Date of birth
        3. Address (with the country)
        4. Contact number (with country code) - available via WhatsApp
        5. Email ID
        6. Latest qualification (month-year)

        If the qualification is GCSE or O-levels, following resultsm
        - English
        - Maths
        - Science

        If the qualification is A-Level, full results

        If the qualification is a Bachelor's degree, extract the following:
        1. Stream of study
        2. GPA

        If the qualification is a Master's degree, extract the following:
        1. Stream of study
        2. GPA

        7. English language qualifications - IELTS / PTE

        Candidate CV:
        {cv}
        """
    )

    model = ChatOpenAI()

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser
    output = chain.invoke({"cv": cv})
    os.makedirs("tmp", exist_ok=True)

    with open("temp/extracted_details.txt", "w") as file:
        file.write(output)

    return output
