import requests
from bs4 import BeautifulSoup
from llama_hub.youtube_transcript import YoutubeTranscriptReader


# Function to fetch and parse content from a specific URL
def fetch_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract text content from the webpage
        text_content = soup.get_text()
        return text_content
    else:
        print(f"Failed to fetch content from {url}")
        return None


def fetch_youtube_content(url):
    loader = YoutubeTranscriptReader()
    documents = loader.load_data(ytlinks=[url])
    return documents[0].text
