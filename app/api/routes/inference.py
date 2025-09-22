from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from app.core.orchestrator import Orchestrator


router = APIRouter()
ORCH = Orchestrator()


class InferenceRequest(BaseModel):
    task: str


@router.post("/complete")
def complete(req: InferenceRequest) -> Dict[str, Any]:
    out = ORCH.handle(req.task)
    return out

