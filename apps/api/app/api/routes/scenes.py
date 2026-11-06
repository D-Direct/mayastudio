"""Scenes Routes - CRUD operations for scenes"""
from fastapi import APIRouter, HTTPException
from uuid import UUID

router = APIRouter()

@router.post("/{project_id}/scenes")
async def create_scene(project_id: UUID):
    """Create scene in project"""
    raise HTTPException(status_code=501, detail="Not implemented")

@router.get("/{project_id}/scenes")
async def list_scenes(project_id: UUID):
    """List scenes in project"""
    return []

@router.get("/scenes/{scene_id}")
async def get_scene(scene_id: UUID):
    """Get scene by ID"""
    raise HTTPException(status_code=501, detail="Not implemented")
