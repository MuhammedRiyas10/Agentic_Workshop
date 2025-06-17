import requests
from bs4 import BeautifulSoup

def load_input(mode, data):
    if mode == "url":
        try:
            response = requests.get(data)
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
        except:
            return "Error loading content from URL."
    return data
