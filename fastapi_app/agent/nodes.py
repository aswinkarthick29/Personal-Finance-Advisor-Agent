import pandas as pd
import os
from typing import Dict, Any
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from fastapi_app.agent.state import AgentState

load_dotenv()

# Node 1: Data Processing
def process_csv_data(state: AgentState) -> dict:
    """Parses raw CSV path or data into the state."""
    print("---NODE 1: PROCESSING DATA---")
    return {"csv_data": state.get("csv_data", [])}


# Node 2: Spending Analysis
def analyze_spending(state: AgentState) -> dict:
    """Analyzes the parsed CSV data and generates a financial summary."""
    print("---NODE 2: ANALYZING SPENDING---")
    
    data = state.get("csv_data", [])
    if not data:
        return {"analysis_summary": "No data available to analyze."}
        
    df = pd.DataFrame(data)
    
    if 'Amount' in df.columns and ('Category' in df.columns or 'Description' in df.columns):
        total_spend = df['Amount'].sum()
        category_col = 'Category' if 'Category' in df.columns else 'Description'
        top_spends = df.groupby(category_col)['Amount'].sum().sort_values(ascending=False).head(3)
        
        summary = f"Total spend: ₹{total_spend:,.2f}. Top categories: "
        for cat, amt in top_spends.items():
            summary += f"\n- {cat}: ₹{amt:,.2f}"
    else:
        summary = f"Could not analyze data fully. Here are the raw columns: {df.columns.tolist()}"
        
    return {"analysis_summary": summary}


# Initialize Groq LLM
def _get_llm():
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=os.environ.get("GROQ_API_KEY"),
    )


# Node 3: Advice Generation
def generate_initial_advice(state: AgentState) -> dict:
    """Uses Groq to generate initial savings advice based on the analysis."""
    print("---NODE 3: GENERATING ADVICE---")
    
    llm = _get_llm()
    analysis = state.get("analysis_summary", "")
    
    prompt = f"""
    You are a professional Personal Finance Advisor.
    Below is a summary of the user's recent spending:
    {analysis}
    
    Provide exactly 3 practical, actionable pieces of advice on where the user can cut back to increase their savings.
    Be concise but friendly.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"current_advice": response.content}


# Node 4: Revising Advice (Post-Feedback)
def revise_advice(state: AgentState) -> dict:
    """Revises advice based on user feedback."""
    print("---NODE 5: REVISING ADVICE---")
    
    llm = _get_llm()
    current_advice = state.get("current_advice", "")
    feedbacks = state.get("feedback_history", [])
    latest_feedback = feedbacks[-1] if feedbacks else "No feedback provided."
    iters = state.get("iteration_count", 0) + 1
    
    # --- Guardrail Check ---
    guardrail_prompt = f"""
    You are a guardrail for a Personal Finance Advisor AI.
    Determine if the following user input is related to personal finance, budgeting, savings, investing, seeking financial advice, or providing constraints on previous financial advice.
    
    User Input: "{latest_feedback}"
    
    If it is purely unrelated (e.g., asking for a biryani recipe, writing code, general knowledge, or casual chat unrelated to finance), reply entirely with exactly 'REJECT'. 
    Otherwise, reply with 'ACCEPT'.
    """
    
    guardrail_response = llm.invoke([HumanMessage(content=guardrail_prompt)]).content.strip()
    
    if "REJECT" in guardrail_response.upper():
        print(f"Guardrail Check Failed: Rejecting off-topic query: '{latest_feedback}'")
        return {
            "current_advice": "I am a Personal Finance Advisor AI and can only help with questions related to personal finance, savings, budgeting, and your expenses. Please ask a relevant question.",
            "iteration_count": iters
        }
    # -----------------------
    
    prompt = f"""
    You are a professional Personal Finance Advisor.
    You previously gave this advice:
    {current_advice}
    
    The user provided the following feedback/constraints:
    "{latest_feedback}"
    
    Please REVISE your advice to fully accommodate the user's feedback. 
    Explain how they can still save money while respecting their constraints.
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return {
        "current_advice": response.content,
        "iteration_count": iters
    }

# Node 5: Future Predictions
def predict_future_savings(state: AgentState) -> dict:
    """Calculates speculative future savings."""
    print("---NODE 6: PREDICTING FUTURE SAVINGS---")
    
    analysis = state.get("analysis_summary", "")
    total_spend = 0
    try:
        import re
        match = re.search(r"Total spend:\s*₹([\d,]+\.\d{2})", analysis)
        if match:
             total_spend = float(match.group(1).replace(',', ''))
    except Exception:
        pass
        
    estimated_monthly_savings = total_spend * 0.10 if total_spend > 0 else 150.0
    
    predictions = {
        "1_month": estimated_monthly_savings,
        "6_months": estimated_monthly_savings * 6,
        "1_year": estimated_monthly_savings * 12
    }
    
    return {"future_predictions": predictions}
