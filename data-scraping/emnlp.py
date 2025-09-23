import json
from nips import fetch_page
import requests
from bs4 import BeautifulSoup

def get_emnlp_paper_details(soup: BeautifulSoup):
    title = soup.select('')

def parse_emnlp_papers(soup: BeautifulSoup):
    papers = soup.select('p')
    ...

if __name__ == '__main__':
    year = 2024
    base_url = 'https://aclanthology.org/events/emnlp-{0}/'

    soup = fetch_page(base_url.format(year))
    if soup:
        papers = parse_emnlp_papers(soup)

    with open(f'./data/emnlp.{year}.json', 'w') as f:
        json.dump(papers, f, indent=2)

