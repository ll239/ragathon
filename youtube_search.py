import streamlit as st
from util.scrape_util import fetch_youtube_content
import util.prompt_util as prompt_util
from urllib.parse import urlparse
from googleapiclient.discovery import build
import os


def search_youtube(query, max_results=3):
    api_key = os.environ.get('YOUTUBE_API')
    if api_key is None:
        st.warning('Please enter your Youtube Api Key', icon='⚠')
    else:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=max_results
        )
        response = request.execute()

        video_links = []
        for item in response['items']:
            video_id = item['id']['videoId']
            video_links.append(f'https://www.youtube.com/watch?v={video_id}')

        return video_links


def youtube_search_engine():
    # Add CSS styling for the search bar and button
    st.markdown(
        """
        <style>
        /* Add CSS styling for the search bar */
        .stTextInput>div>div>input {
            background-color: #f0f2f6; /* Background color */
            color: #333; /* Text color */
            border: 1px solid #ccc; /* Border color */
            border-radius: 5px; /* Border radius */
            padding: 8px 12px; /* Padding */
            font-size: 16px; /* Font size */
            transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out; /* Transition effect */
        }
        /* Add CSS styling for the search button */
        .stButton>button {
            background-color: #4CAF50; /* Button background color */
            color: white; /* Button text color */
            border: none; /* Remove button border */
            border-radius: 5px; /* Button border radius */
            padding: 10px 20px; /* Button padding */
            font-size: 16px; /* Button font size */
            cursor: pointer; /* Cursor style */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    search_query = st.text_input("Search", "")

    if search_query:
        search_results = search_youtube(search_query)
        print(search_results)

        # Apply CSS styling to the search results
        if search_results:
            st.markdown(
                """
                <style>
                .search-result {
                    padding: 10px;
                    margin-bottom: 10px;
                }
                .search-result-link {
                    color: #007bff;
                    text-decoration: none;
                    font-weight: bold;
                }
                .search-result-box {
                    border: 2px solid;
                    border-radius: 5px;
                    padding: 10px;
                    margin-bottom: 10px;
                    cursor: pointer;
                }
                .search-result-box-blue {
                    border-color: #007bff;
                    color: #007bff;
                }
                .search-result-box-green {
                    border-color: #28a745;
                    color: #28a745;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            for idx, url in enumerate(search_results, start=1):
                # if st.button(f" URL: {url}"):
                """if count == 1:
                    prompt_util.insert_trigger()
                if count == 3:
                    break"""
                summary, trigger, theme = prompt_util.check_db(url)
                print(summary, trigger)
                print(type(summary))

                if str(summary) == 'None':

                    text_content = fetch_youtube_content(url)
                    print(text_content)
                    if text_content is None:
                        continue
                summary, theme, trigger = prompt_util.insert_db(text_content, idx, url)
                parsed_url = urlparse(url)
                # Get the subdomain
                domain_parts = parsed_url.netloc.split('.')
                domain = domain_parts[-2] if len(domain_parts) > 1 else domain_parts[0]
                # Convert the first letter of the domain to uppercase
                domain = domain.capitalize()
                # Display the domain as a clickable link with custom CSS
                st.markdown(
                    f"<a href='https://{parsed_url.netloc}' style='font-size: 18px; color: red; text-decoration: none; text-transform: capitalize;'>{domain}</a>",
                    unsafe_allow_html=True)
                st.markdown(
                    """<button onclick="alert('Thumbs Up clicked!')">👍</button>&nbsp;<button onclick="alert('Thumbs 
                    Down clicked!')">👎</button>&nbsp;<button onclick="alert('Button clicked!')">❌</button>""",
                    unsafe_allow_html=True)
                st.error("Trigger: " + str(trigger))
                st.success("Theme: " + str(theme))
                st.success("Summary: " + str(summary))
