from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from app.memory.experience import ExperienceBuffer


router = APIRouter()
EXP = ExperienceBuffer()


class ExpLog(BaseModel):
    event: Dict[str, Any]


@router.post("/log")
def log_event(rec: ExpLog) -> Dict[str, Any]:
    EXP.append(rec.event)
    return {"status": "ok"}

