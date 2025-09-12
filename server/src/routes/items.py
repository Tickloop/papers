from src.core.db import DB

from fastapi import APIRouter

router = APIRouter()


def load_json(file: str):
    import json
    with open('/home/arya/projects/papers/data-scraping/data/' + file, 'r') as f:
        return json.load(f)

def save_json(file: str, data):
    import json
    with open('/home/arya/projects/papers/data-scraping/data/' + file, 'w') as f:
        json.dump(data, f)

# data = load_json('nips2024.json')
data = load_json('acl-entities-cleaned.json')
actions = load_json('actions.json')

from pydantic import BaseModel

class ItemAction(BaseModel):
    id: str
    action: str

@router.get('')
async def get_items(db: DB, limit: int = 25):
    read_ids = [item['id'] for item in actions]
    unread_papers = [item for item in data if item['id'] not in read_ids]
    return unread_papers[:limit]

@router.get('/count/total')
async def get_total_count(db: DB):
    return {'total_count': len(data)}

@router.get('/count/likes')
async def get_likes_count(db: DB):
    return {'likes_count': len([item for item in actions if item['action'] == 'accepted'])}

@router.get('/likes')
async def get_liked_items(db: DB, offset: int = 0, limit: int = 25):
    liked_ids = [item['id'] for item in actions if item['action'] == 'accepted']
    liked_papers = [item for item in data if item['id'] in liked_ids]
    return liked_papers[offset: offset + limit]

@router.post('')
async def action(item_action: ItemAction, db: DB):
    if item_action.action == 'accept':
        actions.append({'id': item_action.id, 'action': 'accepted'})
    elif item_action.action == 'reject':
        actions.append({'id': item_action.id, 'action': 'rejected'})
    save_json('actions.json', actions)
    return {'status': 'success', 'actions': actions}