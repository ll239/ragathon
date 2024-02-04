import streamlit as st
from home_page import home
from search_page import search_engine
from youtube_search import youtube_search_engine
import os


def home_page():
    home()


def search_page():
    search_engine()


def youtube_search():
    youtube_search_engine()


def main():
    page = st.sidebar.radio('', ["\U0001F3E0  Home", "Tingle Search Engine", "Youtube Search"])

    if page == "\U0001F3E0  Home":
        home_page()
    elif page == "Tingle Search Engine":
        search_page()
    elif page == "Youtube Search":
        youtube_search()

    st.markdown(
        """
        <style>
        /* Add CSS styling for the text input field */
        .stTextInput>div>div>input {
            background-color: white;
            color: darkgreen;
            border: 2px solid darkgreen;
            border-radius: 5px;
            padding: 8px 12px;
            font-size: 18px;
            transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
            caret-color: black;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    openai_api_key = st.sidebar.text_input(
        "Enter OpenAI API Key", key="openai_api_key", type="password"
    )
    os.environ["OPENAI_API_KEY"] = openai_api_key
    st.sidebar.markdown(
        "[Get an OpenAI API Key](https://platform.openai.com/account/api-keys)"
    )
    astra_db_token = st.sidebar.text_input(
        "Enter ASTRADB APPLICATION TOKEN", key="astra_db_token", type="password"
    )

    os.environ["ASTRA_DB_APPLICATION_TOKEN"] = astra_db_token
    st.sidebar.markdown(
        "[Get an ASTRADB APPLICATION TOKEN  ](https://docs.datastax.com/en/astra-serverless/docs/manage/org/manage"
        "-tokens.html) "
    )

    astra_db_api = st.sidebar.text_input(
        "Enter ASTRADB API ENDPOINT", key="astra_db_api", type="password"
    )
    os.environ["ASTRA_DB_API_ENDPOINT"] = astra_db_api
    st.sidebar.markdown(
        "[Create Astradb ](https://docs.datastax.com/en/astra/astra-db-vector/databases/create-database.html)"
    )

    youtube_api = st.sidebar.text_input("Enter Youtube API ENDPOINT", key="youtube_api", type="password")
    os.environ["YOUTUBE_API"] =youtube_api

    google_api = st.sidebar.text_input(
        "Enter Google API KEY", key="google_api", type="password"
    )
    os.environ["GOOGLE_API"] = google_api

    st.sidebar.divider()


if __name__ == "__main__":
    main()
