import requests
from bs4 import BeautifulSoup

def scrape_metadata(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return None, f"Error: Received status code {response.status_code}"

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "N/A"
        description = soup.find("meta", attrs={"name": "description"})
        keywords = soup.find("meta", attrs={"name": "keywords"})
        og_title = soup.find("meta", property="og:title")

        return {
            "url": url,
            "title": title,
            "description": description["content"] if description else "N/A",
            "keywords": keywords["content"] if keywords else "N/A",
            "og_title": og_title["content"] if og_title else "N/A"
        }, None

    except Exception as e:
        return None, f"Exception: {e}"
