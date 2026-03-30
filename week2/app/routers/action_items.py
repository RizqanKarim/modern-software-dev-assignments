from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .. import db
from ..services.extract import extract_action_items, extract_action_items_llm

router = APIRouter(prefix="/action-items", tags=["action-items"])

# Unified request model for both extract endpoints
class ExtractPayload(BaseModel):
    text: str
    save_note: Optional[bool] = False

@router.post("/extract")
def extract(payload: ExtractPayload) -> Dict[str, Any]:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        try:
            note_id = db.insert_note(text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save note: {str(e)}")

    try:
        items = extract_action_items(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")

    try:
        ids = db.insert_action_items(items, note_id=note_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save action items: {str(e)}")

    return {
        "note_id": note_id,
        "items": [{"id": i, "text": t} for i, t in zip(ids, items)]
    }


@router.post("/extract-llm")
def extract_llm(payload: ExtractPayload) -> Dict[str, Any]:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        try:
            note_id = db.insert_note(text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save note: {str(e)}")

    try:
        items = extract_action_items_llm(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM extraction failed: {str(e)}")

    try:
        ids = db.insert_action_items(items, note_id=note_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save action items: {str(e)}")

    return {
        "note_id": note_id,
        "items": [{"id": i, "text": t} for i, t in zip(ids, items)]
    }


@router.get("")
def list_all(note_id: Optional[int] = None) -> List[Dict[str, Any]]:
    rows = db.list_action_items(note_id=note_id)
    return [
        {
            "id": r["id"],
            "note_id": r["note_id"],
            "text": r["text"],
            "done": bool(r["done"]),
            "created_at": r["created_at"],
        }
        for r in rows
    ]


@router.post("/{action_item_id}/done")
def mark_done(action_item_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
    done = bool(payload.get("done", True))
    db.mark_action_item_done(action_item_id, done)
    return {"id": action_item_id, "done": done}