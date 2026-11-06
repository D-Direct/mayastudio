"""Script Parsing Routes - Gemini AI integration"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ScriptParseRequest(BaseModel):
    """Script parsing request"""
    script_text: str
    language: str = "sinhala"

@router.post("/parse-script")
async def parse_script(request: ScriptParseRequest):
    """Parse screenplay into structured JSON using Gemini"""
    # TODO: Integrate Google Gemini API
    raise HTTPException(status_code=501, detail="Not implemented")
