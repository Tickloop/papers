import json
import requests
from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor, as_completed

def parse_all_papers(soup: BeautifulSoup):
    def get_paper_links(soup: BeautifulSoup):
        title = soup.find('a').text
        authors = soup.find('i').text
        link = soup.find('a')['href']
        return {
            'title': title,
            'link': link,
            'authors': authors,
        }
    all_papers = [get_paper_links(paper) for paper in soup.select('.conference')]
    all_benchmarks = [get_paper_links(benchmark) for benchmark in soup.select('.datasets_and_benchmarks_track')]
    return [*all_papers, *all_benchmarks]

def get_paper_details(soup: BeautifulSoup):
    nips_paper_base_url = 'https://papers.nips.cc/{0}'
    title = soup.select('body > div.container-fluid > div > h4:nth-child(1)')[0].text
    link = soup.select('body > div.container-fluid > div > div > a.btn.btn-primary.btn-spacer')[0]['href']
    authors = soup.select('body > div.container-fluid > div > p:nth-child(6)')[0].text
    abstract = soup.select('body > div.container-fluid > div > p:nth-child(8)')[0].text
    abstract_html = str(soup.select('body > div.container-fluid > div > p:nth-child(8)')[0])
    return {
        'title': title,
        'link': nips_paper_base_url.format(link),
        'authors': authors,
        'abstract': abstract,
        'abstract_html': abstract_html
    }

def paper_pipeline(link: str):
    soup = fetch_page(link)
    if soup:
        return {**get_paper_details(soup), "original_link": link}
    return None

def fetch_page(url: str):
    r = requests.get(url)
    if r.status_code == 200:
        return BeautifulSoup(r.content, 'html.parser')
    return None

if __name__ == '__main__':
    # first get all the paper urls
    year = 2023
    nips_anth = 'https://papers.nips.cc/paper_files/paper/{0}'
    nips_paper_base_url = 'https://papers.nips.cc/{0}'
    soup = fetch_page(nips_anth.format(f'{year}'))
    
    # get all paper links
    if soup:
        papers = parse_all_papers(soup)
    
    # threadpoolexecutor
    detailed_papers = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(paper_pipeline, nips_paper_base_url.format(paper['link'])): paper for paper in papers}
        idx = 0
        for future in as_completed(future_to_url):
            paper = future_to_url[future]
            try:
                detailed_papers.append({"id": idx, **future.result()})
            except Exception as e:
                print(f"Error fetching details for {paper['title']}: {e}")
            idx += 1

    with open(f'./data/nips.{year}.json', 'w') as f:
        json.dump(detailed_papers, f, indent=4)
