from typing import List, Optional
from pydantic import BaseModel

class AgentState(BaseModel):
    input_path: str
    input_type: str
    raw_text: Optional[str] = None
    extracted_skills: Optional[List[str]] = []
    enriched_concepts: Optional[List[str]] = []
    profile: Optional[str] = None
    recommendations: Optional[str] = None
