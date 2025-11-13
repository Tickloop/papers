import json

from sqlmodel import select
from src.core.models import Paper, Venue
from src.core.db import Session, get_settings, create_engine

def load_papers_from_json():
    with open('../data/acl-papers-with-venues.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
    return papers

def load_venues_from_json():
    with open('../data/acl-venues.json', 'r', encoding='utf-8') as f:
        venues = json.load(f)
    return venues

def write_to_db(papers: list[dict], venues: list[dict], db_url: str):
    with Session(create_engine(db_url)) as session:
        session.add_all([
            Venue(
                url=venue['url'],
                name=venue['name'],
                acl_id=venue['abbr'],
                volume_cnt=venue['volume_count']
            ) for venue in venues
        ])
        session.commit()
        print('Venues added to DB....')
        db_venues = {venue.acl_id: venue for venue in session.exec(select(Venue)).all()}
        
        session.add_all([
            Paper(
                abstract=paper['abstract'],
                authors=paper['author'],
                title=paper['title'],
                url=paper['url'],
                venue=db_venues.get(paper['venue_id'])
            ) for paper in papers
        ])
        session.commit()

if __name__ == '__main__':
    db_url = get_settings().db_url
    papers = load_papers_from_json()
    venues = load_venues_from_json()
    write_to_db(papers, venues, db_url)