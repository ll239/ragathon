import streamlit as st
from googlesearch import search
import webbrowser
from util.scrape_util import fetch_content
import util.prompt_util as prompt_util
import requests
from urllib.parse import urlparse


def google_custom_search( cx, query, num=20):
    api_key = os.environ.get('GOOGLE_API')
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}&num={num}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('items', [])
    else:
        print(f"Error: {response.status_code}")
        return []

def search_engine():
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



    cx = "7231a8d5afbf1470f"
    # Create a text input for search
    search_query = st.text_input("Search", "")

    # Perform a search using the Custom Search API
    results = google_custom_search( cx, search_query)
    search_results = [result["link"] for result in results]


    if search_query:
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
                summary, trigger, theme = prompt_util.check_db(url)
                print(summary, trigger)
                print(type(summary))

                if str(summary) == 'None':

                    text_content = fetch_content(url)
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
                    st.markdown(
                        """<button onclick="alert('Thumbs Up clicked!')">👍</button>&nbsp;<button onclick="alert('Thumbs Down clicked!')">👎</button>&nbsp;<button onclick="alert('Button clicked!')">❌</button>""",
                        unsafe_allow_html=True)
                    # Display the domain as a clickable link with custom CSS
                    st.markdown(
                        f"<a href='https://{parsed_url.netloc}' style='font-size: 18px; color: red; text-decoration: none; text-transform: capitalize;'>{domain}</a>",
                        unsafe_allow_html=True)

                    st.success(summary)
                    st.success(theme)
                    st.error(trigger)
                else:
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
                        """<button onclick="alert('Thumbs Up clicked!')">👍</button>&nbsp;<button onclick="alert('Thumbs Down clicked!')">👎</button>&nbsp;<button onclick="alert('Button clicked!')">❌</button>""",
                        unsafe_allow_html=True)

                    st.success(summary)
                    st.success(theme)
                    st.error(trigger)
