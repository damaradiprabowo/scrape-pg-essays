import os.path
import html2text
import regex as re
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import urllib.request

"""
Download a collection of Paul Graham essays into csv file
"""

h = html2text.HTML2Text()
h.ignore_images = True
h.ignore_tables = True
h.escape_all = True
h.reference_links = True
h.mark_code = True

FILE = "./essays.csv"

if os.path.isfile(FILE):
    os.remove(FILE)


def parse_main_page(base_url: str, articles_url: str):
    assert base_url.endswith(
        "/"), f"Base URL must end with a slash: {base_url}"
    response = requests.get(base_url + articles_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all relevant 'td' elements
    td_cells = soup.select("table > tr > td > table > tr > td")
    chapter_links = []

    print(f"Found {len(td_cells)} td elements")

    for td in td_cells:
        img = td.find("img")
        if img and int(img.get("width", 0)) <= 15 and int(img.get("height", 0)) <= 15:
            a_tag = td.find("font").find("a") if td.find("font") else None
            if a_tag:
                chapter_links.append(
                    {"link": urljoin(
                        base_url, a_tag["href"]), "title": a_tag.text}
                )

    print(f"Total links found: {len(chapter_links)}")
    return chapter_links

def fetch_essay(url: str):
    try:
        with urllib.request.urlopen(url) as website:
            content = website.read().decode("utf-8")
    except UnicodeDecodeError:
        with urllib.request.urlopen(url) as website:
            content = website.read().decode("latin-1")

    parsed = h.handle(content)
    return parsed

def count_words(text: str):
    words = re.findall(r'\w+', text)
    return len(words)

def main():
    base_url = "http://www.paulgraham.com/"
    articles_url = "articles.html"
    essays = parse_main_page(base_url, articles_url)
    print(essays)
    data = []
    
    for essay in essays:
        url = essay['link']
        if "http://www.paulgraham.com/https://" in url:
            url = url.replace("http://www.paulgraham.com/https://", "https://")
        
        text = fetch_essay(url)
        word_count = count_words(text)
        data.append({
            "title": essay['title'],
            "word_counts": word_count, 
            "texts": text
        })

    df = pd.DataFrame(data)
    df.to_csv("essays.csv", index=False)
    print("DataFrame exported to essays.csv")

if __name__ == "__main__":
    main()