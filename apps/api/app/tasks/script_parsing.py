"""
Script Parsing Tasks
Celery tasks for Gemini AI script parsing
"""

from app.worker import celery_app


@celery_app.task(name="parse_screenplay")
def parse_screenplay(project_id: str, script_text: str):
    """
    Parse screenplay text using Google Gemini

    Steps:
    1. Call Gemini API with parsing prompt
    2. Extract structured dialogue data
    3. Create scenes and dialogue blocks in database
    4. Return parsed structure
    """
    # TODO: Implement Gemini parsing
    print(f"Parsing screenplay for project {project_id}...")

    return {"project_id": project_id, "status": "completed"}
