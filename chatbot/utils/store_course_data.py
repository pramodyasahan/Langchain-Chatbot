import os
import logging
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
load_dotenv()


def create_chroma_vectorstore_from_folder(folder_path, collection_name):
    """
    Create a Chroma vector store from text files in a specified folder.

    Args:
        folder_path (str): Path to the folder containing text files.
        collection_name (str): Name of the Chroma collection.

    Returns:
        Chroma: A Chroma vector store with embedded documents.
    """
    if not os.path.exists(folder_path):
        logging.error(f"Folder path '{folder_path}' does not exist.")
        return None

    logging.info(f"📂 Processing files from: {folder_path}")

    embeddings = OpenAIEmbeddings()
    documents = []
    file_count = 0

    # Read and load documents
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            try:
                loader = TextLoader(file_path, encoding="utf-8")
                doc = loader.load()
                documents.extend(doc)
                file_count += 1
            except Exception as e:
                logging.error(f"❌ Error loading '{filename}': {e}")

    if not documents:
        logging.warning(f"⚠️ No text documents found in {folder_path}. Skipping collection.")
        return None

    logging.info(f"Total files processed: {file_count}")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = text_splitter.split_documents(documents)
    logging.info(f"Total document chunks created: {len(splits)}")

    # Create Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory="../chroma_db"
    )

    logging.info(f"✅ Chroma vectorstore '{collection_name}' created successfully at '../chroma_db'.")

    return vectorstore


def process_all_universities(dataset_base_path):
    """
    Process all university folders inside the dataset base path and create a Chroma vector store for each.

    Args:
        dataset_base_path (str): Path to the dataset containing multiple university folders.
    """
    logging.info("🚀 Starting vector store creation for all universities...")

    if not os.path.exists(dataset_base_path):
        logging.error(f"Dataset base path '{dataset_base_path}' does not exist.")
        return

    for university_folder in os.listdir(dataset_base_path):
        university_path = os.path.join(dataset_base_path, university_folder)

        if os.path.isdir(university_path):  # Ensure it's a folder
            collection_name = university_folder.lower().replace(" ", "_")  # Normalize collection name
            logging.info(f"🔍 Processing university: {university_folder} -> Collection: {collection_name}")
            create_chroma_vectorstore_from_folder(university_path, collection_name)

    logging.info("🎉 Vector store creation for all universities completed!")


def main():
    dataset_base_path = "../../dataset"  # Base path containing multiple university folders
    process_all_universities(dataset_base_path)


if __name__ == "__main__":
    main()
