from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    # The raw parsed CSV data (e.g., list of dictionaries representing rows)
    csv_data: List[Dict[str, Any]]
    
    # Financial analysis generated from data processing
    analysis_summary: str
    
    # The current generated advice from the LLM
    current_advice: str
    
    # History of user feedback for context
    feedback_history: Annotated[List[str], operator.add]
    
    # Projected future savings based on the accepted advice
    future_predictions: Dict[str, float]
    
    # Track iterations to prevent infinite loops (cycle breaker)
    iteration_count: int
    
    # Standard LangGraph messages
    messages: Annotated[List[BaseMessage], operator.add]
