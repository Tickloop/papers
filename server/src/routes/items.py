from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def get_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

@router.post('/')
async def create_item(item: dict):
    return {"id": 3, "name": item["name"]}
