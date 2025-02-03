import os
import gdown
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Google Drive file ID (Extract from the share link)
FILE_ID = "1bsUFKFFIW9YWZRZAyKDyuNn46Vp-CxBP"
DESTINATION_PATH = "chatbot/chroma_db/"

def download_from_gdrive(file_id, destination):
    """Download a file from Google Drive and save it."""
    if not os.path.exists(destination):  # Avoid redownloading
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        gdown.download(f"https://drive.google.com/uc?id={file_id}", destination, quiet=False)
        st.success(f"File downloaded successfully to {destination}")
    else:
        st.info("File already exists, skipping download.")

def main():
    """Main Streamlit App"""
    # Fix SQLite issue with Streamlit
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

    st.set_page_config(page_title="Demo", page_icon=":memo:", layout="wide")

    # Ensure the file is downloaded
    download_from_gdrive(FILE_ID, DESTINATION_PATH)

    pg = st.navigation(
        [
            st.Page("pages/page1.py", title="Introduction"),
            st.Page("pages/page2.py", title="Chatbot")
        ]
    )
    pg.run()


if __name__ == "__main__":
    main()
