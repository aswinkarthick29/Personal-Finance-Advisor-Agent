from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver

from fastapi_app.agent.state import AgentState
from fastapi_app.agent.nodes import (
    process_csv_data,
    analyze_spending,
    generate_initial_advice,
    revise_advice,
    predict_future_savings
)

def should_end_or_continue(state: AgentState) -> str:
    """Conditional routing based on iteration count and feedback."""
    # Prevent infinite loops
    iters = state.get("iteration_count", 0)
    if iters >= 3:
        return "predict_future_savings"

    # If new feedback was just added via Human-in-the-loop, go to revision
    return "revise_advice"


def compile_graph():
    """Builds and compiles the LangGraph workflow with a Memory Checkpointer."""
    builder = StateGraph(AgentState)
    
    # 1. Add all nodes
    builder.add_node("process_csv", process_csv_data)
    builder.add_node("analyze_spending", analyze_spending)
    builder.add_node("generate_initial_advice", generate_initial_advice)
    
    # Notice we don't have a specific "feedback_node". To get feedback, 
    # we use a breakpoint just *before* revising advice.
    builder.add_node("revise_advice", revise_advice)
    builder.add_node("predict_future_savings", predict_future_savings)
    
    # 2. Add normal edges
    builder.add_edge(START, "process_csv")
    builder.add_edge("process_csv", "analyze_spending")
    builder.add_edge("analyze_spending", "generate_initial_advice")
    
    # From initial advice, we jump straight to predicting futures as the baseline
    builder.add_edge("generate_initial_advice", "predict_future_savings")
    
    # 3. Add cyclic routing from predicting futures. 
    # The LangGraph will pause *after* 'predict_future_savings' waiting for human intervention on the frontend.
    
    # After revision, we always re-predict
    builder.add_edge("revise_advice", "predict_future_savings")
    
    # Let's cleanly exit if the human is satisfied. 
    # If the user is satisfied, they won't resume the graph with new feedback.
    
    # 4. Compile with checkpointer
    # MemorySaver tracks the thread state so we can interrupt and resume
    memory = MemorySaver()
    graph = builder.compile(
        checkpointer=memory,
        interrupt_after=["predict_future_savings"]  # THE BREAKPOINT - Wait for frontend here
    )
    
    return graph

# Expose a singleton graph instance for the FastAPI app
finance_agent_graph = compile_graph()
