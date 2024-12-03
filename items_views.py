from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/")
def list_items():
    return {"items": [{"id": "1", "label": "Item 1"}, ]}


@router.get("/latest")
def get_latest():
    return {"items": {"item_id": 1, "name": "Item 1"}}


@router.get("/{item_id}")
def get_item(item_id: Annotated[int, Path(ge=1)]):
    return {"item_id": item_id}
