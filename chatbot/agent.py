import os
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from chatbot.memory import agent_memory
from chatbot.eopp_tool import match_eopp
from dotenv import load_dotenv
from chatbot.tools.information_rag_tool import query_data

# Load environment variables
load_dotenv()

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.environ.get("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = 'true'

# Load Google search tool
web_search_tool = load_tools(["google-serper"], serper_api_key=SERPER_API_KEY)

# Add course retrieval tool to tools list
tools = web_search_tool + [match_eopp, query_data]


def load_onboarding_questions() -> str:
    """Load onboarding questions from a text file."""
    questions_file = os.path.join("docs", "questions.txt")
    if not os.path.exists(questions_file):
        raise FileNotFoundError(f"{questions_file} not found.")

    with open(questions_file, 'r', encoding='utf-8') as file:
        onboarding_questions = file.read().strip()

    return onboarding_questions


def setup_agent() -> AgentExecutor:
    """Set up the agent for finding educational opportunities and course details."""

    extracted_details_path = "temp/extracted_details.txt"

    if os.path.exists(extracted_details_path):
        with open(extracted_details_path, "r") as file:
            extracted_details = file.read().strip()
    else:
        extracted_details = "No extracted details available."

    # Updated Prompt with Course Retrieval
    prompt = PromptTemplate(
        input_variables=["agent_scratchpad", "chat_history", "input"],
        template=(
            f"""
            You are an AI education consultant helping students find the best **Educational Opportunity and Pathways Program (EOPP)**.

            Your Responsibilities
            Gather Required Information  
            - To find the best EOPP, we need key details from the user.
            - Here are the required details:  
            {load_onboarding_questions()}  
            - We have already analyzed their CV and found:
            {extracted_details}
            - Verify with the user if the extracted details are correct.  
            - Ask only one missing detail at a time to avoid overwhelming the user.

            Retrieve Course-Related Information  
            - If the user asks about course fees, duration, entry requirements, or course information, use the 'course_retrieval' tool to fetch relevant details.  
            - If the requested course information is not found, automatically use the 'web_search_tool' to get the latest data.

            Match the Best EOPP  
            - Once all required details are collected, use the 'match_eopp' tool to suggest the most suitable educational opportunities.

            ---  
            Important Rules for Engagement: 
            Be concise and structured in responses.  
            If any requested information is missing, ask for it one at a time. 
            If the user is unsure, offer guidance based on available options.  
            Always provide the most relevant and up-to-date information. 

            Let's get started!   
            """
            """
            Chat History:
            {chat_history}

            User Input: {input}
            {agent_scratchpad}
            """
        ),
    )

    agent_llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)

    agent = create_tool_calling_agent(agent_llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=agent_memory,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    return agent_executor
