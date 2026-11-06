"""Voice Routes - Voice profile management"""
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/design")
async def design_voice():
    """Create voice from text description"""
    raise HTTPException(status_code=501, detail="Not implemented")

@router.post("/clone")
async def clone_voice():
    """Clone voice from audio sample"""
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/")
async def list_voices():
    """List user's voice profiles"""
    return []
