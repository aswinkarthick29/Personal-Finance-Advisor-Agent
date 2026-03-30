from pydantic import BaseModel, Field
from typing import List, Optional

class FeedbackInput(BaseModel):
    thread_id: str = Field(..., description="The LangGraph thread ID to resume the conversation.")
    feedback_text: str = Field(..., description="The feedback provided by the user regarding the savings advice.")

class GraphResponse(BaseModel):
    thread_id: str
    analysis: Optional[str] = None
    advice: Optional[str] = None
    predictions: Optional[dict] = None
