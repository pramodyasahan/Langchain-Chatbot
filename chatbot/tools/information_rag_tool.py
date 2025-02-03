from langchain.agents import tool
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings


@tool
def query_data(input_string: str):
    """Use this tool to query the knowledge base to answer questions about courses."""

    chroma_embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    model = ChatOpenAI(model="gpt-4o-mini", streaming=True)

    DB_FOLDER = "../chatbot/chroma_db"


    # Load ChromaDB
    chroma_db = Chroma(
        persist_directory=DB_FOLDER,
        embedding_function=chroma_embeddings,
        collection_name="spec",
    )

    retriever = chroma_db.as_retriever(search_kwargs={'k': 4})

    # Improved prompt for clarity and precision
    template = """You are answering a user query based on retrieved documentation excerpts. 
    Use only the provided context to generate a precise, factual, and well-structured response. 
    Do not include any assumptions or extra information beyond what is given.

    - If the provided context does not contain enough information to answer the question, state: "I do not have enough information to answer this question."
    - Keep the response formal, clear, and concise.
    - Do not include any emojis, personal opinions, or speculative content.

    ==========
    Question: {question}
    ==========
    Context:
    {context}
    ==========
    Provide a factual and precise response:
    """

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | model
            | StrOutputParser()
    )

    answer = chain.invoke(input_string)
    return answer
