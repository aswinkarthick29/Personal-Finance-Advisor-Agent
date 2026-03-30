from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import pandas as pd
import uuid
import os

from fastapi_app.models import FeedbackInput, GraphResponse
from fastapi_app.agent.graph import finance_agent_graph

load_dotenv()

app = FastAPI(title="Personal Finance Advisor API")

# Setup CORS for the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-csv", response_model=GraphResponse)
@app.post("/upload-csv/", response_model=GraphResponse)
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV to start the agentic workflow."""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
        
    try:
        # Read the CSV into pandas
        df = pd.read_csv(file.file)
        # Convert df to list of dicts for safety
        csv_data = df.to_dict(orient='records')
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {str(e)}")
        
    # Generate a unique thread ID for this user session
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial state
    initial_state = {
        "csv_data": csv_data,
        "iteration_count": 0,
        "feedback_history": []
    }
    
    # Run the graph until the first breakpoint (`interrupt_after=["predict_future_savings"]`)
    for event in finance_agent_graph.stream(initial_state, config=config, stream_mode="values"):
        final_state = event
        
    return GraphResponse(
        thread_id=thread_id,
        analysis=final_state.get("analysis_summary"),
        advice=final_state.get("current_advice"),
        predictions=final_state.get("future_predictions")
    )


@app.post("/provide-feedback", response_model=GraphResponse)
async def provide_feedback(feedback_input: FeedbackInput):
    """Resume the agent with new human feedback."""
    config = {"configurable": {"thread_id": feedback_input.thread_id}}
    
    # Get current state to ensure the thread exists
    current_state_wrapper = finance_agent_graph.get_state(config)
    
    if not current_state_wrapper or not current_state_wrapper.values:
        raise HTTPException(status_code=404, detail="Thread not found or expired.")
    
    current_state = current_state_wrapper.values

    # Append the new feedback to the state's feedback_history
    existing_history = current_state.get("feedback_history", [])
    new_history = existing_history + [feedback_input.feedback_text]

    # Update the state with the new feedback
    finance_agent_graph.update_state(
        config,
        {"feedback_history": new_history},
    )

    # Get the freshly updated state
    updated_state = finance_agent_graph.get_state(config).values

    # Directly invoke the revise_advice node logic on the current state
    from fastapi_app.agent.nodes import revise_advice, predict_future_savings
    
    revised = revise_advice(updated_state)
    
    # Merge revised advice into state 
    merged_state = {**updated_state, **revised}
    
    # Directly invoke the predict_future_savings node
    predictions = predict_future_savings(merged_state)
    
    # Persist the updated state back into the graph so thread stays consistent
    finance_agent_graph.update_state(
        config,
        {**revised, **predictions},
    )

    return GraphResponse(
        thread_id=feedback_input.thread_id,
        analysis=merged_state.get("analysis_summary"),
        advice=revised.get("current_advice"),
        predictions=predictions.get("future_predictions")
    )
