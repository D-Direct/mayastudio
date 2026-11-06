"""Dialogue Routes - Manage dialogue blocks"""
from fastapi import APIRouter, HTTPException
from uuid import UUID

router = APIRouter()

@router.post("/scenes/{scene_id}/dialogue")
async def create_dialogue_block(scene_id: UUID):
    """Create dialogue block"""
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/scenes/{scene_id}/dialogue")
async def list_dialogue_blocks(scene_id: UUID):
    """List dialogue blocks in scene"""
    return []

@router.post("/dialogue/{block_id}/generate-audio")
async def generate_audio(block_id: UUID):
    """Generate TTS audio for dialogue block"""
    raise HTTPException(status_code=501, detail="Not implemented")
