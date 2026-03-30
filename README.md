# 💰 Personal Finance Advisor Agent

An AI-powered Personal Finance Advisor built with **LangGraph**, **FastAPI**, and **Streamlit**. Upload your expense CSV, get personalized savings advice powered by **Groq (LLaMA 3.3 70B)**, provide feedback to refine the advice, and see future savings predictions — all through an interactive agent workflow.

---

## 🚀 Features

- 📊 **Expense Analysis** — Automatically parses and summarizes your spending by category
- 🤖 **AI-Powered Advice** — Generates 3 actionable savings tips using Groq's LLaMA 3.3 70B model
- 🔄 **Human-in-the-Loop Feedback** — Revises advice based on your constraints and preferences
- 📈 **Future Savings Predictions** — Estimates savings at 1 month, 6 months, and 1 year
- 🖥️ **Streamlit Frontend** — Clean, interactive UI for the full workflow

---

## 🧠 Architecture

```
CSV Upload → Process CSV → Analyze Spending → Generate Advice → Predict Savings
                                                                      ↕  (breakpoint)
                                                   Revise Advice ← User Feedback
```

The agent is built as a **LangGraph stateful graph** with a `MemorySaver` checkpointer, allowing the workflow to pause at the `predict_future_savings` node and resume after human feedback via the `/provide-feedback` API.

### LangGraph Nodes

| Node | Responsibility |
|------|---------------|
| `process_csv` | Loads and passes CSV data into the agent state |
| `analyze_spending` | Uses Pandas to compute total spend and top categories |
| `generate_initial_advice` | Calls Groq LLM to generate initial savings tips |
| `predict_future_savings` | Estimates future savings (1M / 6M / 1Y) |
| `revise_advice` | Revises advice based on latest user feedback |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | [Groq — LLaMA 3.3 70B](https://console.groq.com) |
| Backend API | [FastAPI](https://fastapi.tiangolo.com) |
| Frontend | [Streamlit](https://streamlit.io) |
| Data Processing | [Pandas](https://pandas.pydata.org) |
| State Validation | [Pydantic](https://docs.pydantic.dev) |

---

## 📁 Project Structure

```
Personal Finance Advisor/
├── fastapi_app/
│   ├── main.py              # FastAPI routes (/upload-csv, /provide-feedback)
│   ├── models.py            # Pydantic request/response models
│   └── agent/
│       ├── graph.py         # LangGraph workflow definition
│       ├── nodes.py         # Individual agent node functions
│       └── state.py         # AgentState TypedDict
├── streamlit_app/
│   └── app.py               # Streamlit frontend UI
├── sample_expenses.csv      # Sample dataset for testing
├── test_api.py              # API integration tests
├── test_feedback.py         # Feedback loop tests
├── test_routes.py           # Route-level tests
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/aswinkarthick29/Personal-Finance-Advisor-Agent.git
cd Personal-Finance-Advisor-Agent
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate  # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn streamlit langgraph langchain-groq pandas pydantic python-dotenv
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your free API key at [console.groq.com](https://console.groq.com)

---

## ▶️ Running the Application

### Start the FastAPI Backend

```bash
uvicorn fastapi_app.main:app --reload
```

API will be available at `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

### Start the Streamlit Frontend

```bash
streamlit run streamlit_app/app.py
```

Frontend will open at `http://localhost:8501`

---

## 📡 API Endpoints

### `POST /upload-csv`
Upload a CSV file to start the agent workflow.

- **Input:** Multipart CSV file with `Amount` and `Category` columns
- **Returns:** `thread_id`, spending analysis, initial advice, and savings predictions

### `POST /provide-feedback`
Resume the agent with user feedback to revise the advice.

- **Input:** `{ "thread_id": "...", "feedback_text": "I can't cut food expenses" }`
- **Returns:** Updated advice and revised savings predictions

---

## 📄 Sample CSV Format

```csv
Date,Category,Amount,Description
2024-01-01,Food,1500,Groceries
2024-01-02,Transport,500,Uber
2024-01-03,Entertainment,2000,Netflix & Movies
2024-01-04,Utilities,800,Electricity Bill
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

<p align="center">Built with ❤️ by <a href="https://github.com/aswinkarthick29">aswinkarthick29</a></p>
