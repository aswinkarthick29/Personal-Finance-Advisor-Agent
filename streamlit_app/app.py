import streamlit as st
import requests
from PIL import Image

API_URL = "http://localhost:9004"

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
_logo = Image.open("streamlit_app/logo.png")
st.set_page_config(
    page_title="FinAdvisor AI",
    page_icon=_logo,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Dark background */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(15, 15, 30, 0.95) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.2);
}
[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 20px 60px rgba(99, 102, 241, 0.3);
}
.hero-banner h1 {
    font-size: 2.4rem;
    font-weight: 700;
    color: white !important;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero-banner p {
    color: rgba(255,255,255,0.85);
    font-size: 1rem;
    margin: 0;
}

/* ── Glass Cards ── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(12px);
    transition: all 0.2s ease;
}
.glass-card:hover {
    border-color: rgba(99,102,241,0.4);
    background: rgba(255,255,255,0.07);
}

/* ── Metric Cards ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(99,102,241,0.6);
    box-shadow: 0 8px 30px rgba(99,102,241,0.2);
}
.metric-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #a5b4fc;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}

/* ── Upload box ── */
[data-testid="stFileUploader"] {
    background: rgba(99,102,241,0.05) !important;
    border: 2px dashed rgba(99,102,241,0.35) !important;
    border-radius: 12px !important;
    transition: all 0.2s ease;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,0.7) !important;
    background: rgba(99,102,241,0.1) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(99,102,241,0.4) !important;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
    margin-bottom: 0.75rem !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* ── Divider ── */
hr {
    border-color: rgba(255,255,255,0.08) !important;
    margin: 1.5rem 0 !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #6366f1 !important;
}

/* ── Thread ID badge ── */
.thread-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #a5b4fc;
    font-family: monospace;
    margin-bottom: 1rem;
}

/* ── Status pill ── */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.78rem;
    color: #34d399;
    font-weight: 500;
}
.status-dot {
    width: 7px;
    height: 7px;
    background: #34d399;
    border-radius: 50%;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Hide Streamlit branding */
/* Hide only Streamlit footer branding */
footer {visibility: hidden;}

/* Keep sidebar toggle arrow always visible */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    color: #a5b4fc !important;
    background: rgba(99,102,241,0.15) !important;
    border-radius: 50% !important;
}
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ──────────────────────────────────────────────────────────
for k, v in {
    "thread_id": None, "analysis": None, "advice": None,
    "predictions": None, "chat_history": []
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.image("streamlit_app/logo.png", use_container_width=True)
    st.markdown("""
    <div style='text-align:center; padding: 0.5rem 0 1.5rem;'>
        <div style='font-size:1.15rem; font-weight:700; color:#e2e8f0;'>FinAdvisor AI</div>
        <div style='font-size:0.78rem; color:#64748b; margin-top:0.2rem;'>Powered by Groq · LangGraph</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📋 How It Works**")
    st.markdown("""
    <div style='font-size:0.82rem; color:#94a3b8; line-height:1.7;'>
    1️⃣ &nbsp;Upload your expense CSV<br>
    2️⃣ &nbsp;AI analyses your spending<br>
    3️⃣ &nbsp;Get personalised savings advice<br>
    4️⃣ &nbsp;Give feedback to refine suggestions<br>
    5️⃣ &nbsp;View projected savings in ₹
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.thread_id:
        st.markdown("---")
        st.markdown("""<div class='status-pill'><div class='status-dot'></div> Session Active</div>""", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:0.7rem; color:#475569; margin-top:0.5rem; word-break:break-all;'>{st.session_state.thread_id[:20]}...</div>", unsafe_allow_html=True)

        if st.button("🔄 Start New Session"):
            st.session_state.clear()
            st.rerun()

# ─── MAIN CONTENT ───────────────────────────────────────────────────────────
# Hero Banner
st.markdown("""
<div class='hero-banner'>
    <h1>Personal Finance Advisor AI</h1>
    <p>Upload your expenses · Get AI-powered insights · Grow your savings with personalised advice</p>
</div>
""", unsafe_allow_html=True)

# ─── UPLOAD SECTION ─────────────────────────────────────────────────────────
if st.session_state.thread_id is None:
    col1, col2 = st.columns([1.6, 1])

    with col1:
        st.markdown("<div class='section-header'>📤 Upload Your Expense File</div>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drag & drop or browse your CSV file",
            type="csv",
            label_visibility="collapsed"
        )

        if uploaded_file:
            st.markdown(f"""
            <div style='display:flex;align-items:center;gap:10px;background:rgba(99,102,241,0.1);
                border:1px solid rgba(99,102,241,0.3);border-radius:10px;padding:12px 16px;margin:0.75rem 0;'>
                <span style='font-size:1.4rem;'>📄</span>
                <div>
                    <div style='font-weight:600;color:#e2e8f0;'>{uploaded_file.name}</div>
                    <div style='font-size:0.75rem;color:#64748b;'>{uploaded_file.size} bytes</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Analyse My Spending"):
                with st.spinner("🤖 AI Agent processing your data..."):
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                    try:
                        response = requests.post(f"{API_URL}/upload-csv", files=files)
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.thread_id = data.get("thread_id")
                            st.session_state.analysis = data.get("analysis")
                            st.session_state.advice = data.get("advice")
                            st.session_state.predictions = data.get("predictions", {})
                            st.session_state.chat_history.append({"role": "assistant", "content": data.get("advice")})
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Failed to connect to backend: {e}")

    with col2:
        st.markdown("<div class='section-header'>💡 Tips for Best Results</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card'>
            <div style='font-size:0.85rem; color:#94a3b8; line-height:1.9;'>
            ✅ &nbsp;Include a <b style='color:#a5b4fc;'>Category</b> column<br>
            ✅ &nbsp;Include an <b style='color:#a5b4fc;'>Amount</b> column (₹)<br>
            ✅ &nbsp;Add a <b style='color:#a5b4fc;'>Date</b> column for context<br>
            ✅ &nbsp;More rows = better AI insights<br>
            ✅ &nbsp;Use consistent category names
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── RESULTS SECTION ────────────────────────────────────────────────────────
else:
    preds = st.session_state.predictions or {}

    # Thread badge
    st.markdown(f"""<div class='thread-badge'>🔗 Session: {st.session_state.thread_id[:28]}...</div>""", unsafe_allow_html=True)

    # Metric Cards
    st.markdown("<div class='section-header'>📈 Projected Savings (10% monthly reduction)</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='metric-row'>
        <div class='metric-card'>
            <div class='metric-label'>📅 1 Month</div>
            <div class='metric-value'>₹{preds.get('1_month', 0):,.0f}</div>
        </div>
        <div class='metric-card'>
            <div class='metric-label'>🗓️ 6 Months</div>
            <div class='metric-value'>₹{preds.get('6_months', 0):,.0f}</div>
        </div>
        <div class='metric-card'>
            <div class='metric-label'>📆 1 Year</div>
            <div class='metric-value'>₹{preds.get('1_year', 0):,.0f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Analysis expander
    col_a, col_b = st.columns([1.6, 1])

    with col_a:
        with st.expander("📊 View Spending Analysis", expanded=False):
            st.markdown(f"""
            <div style='font-size:0.9rem; color:#cbd5e1; line-height:1.8; padding:0.5rem 0;'>
                {st.session_state.analysis}
            </div>
            """, unsafe_allow_html=True)

        # Chat Interface
        st.markdown("<div class='section-header'>💬 Revise Your Advice</div>", unsafe_allow_html=True)

        # Render messages
        for msg in st.session_state.chat_history:
            icon = "🤖" if msg["role"] == "assistant" else "🧑"
            with st.chat_message(msg["role"], avatar=icon):
                st.markdown(msg["content"])

        user_feedback = st.chat_input("💬 Type feedback, e.g. 'I can't reduce rent, suggest food cuts'")

        if user_feedback:
            st.session_state.chat_history.append({"role": "user", "content": user_feedback})
            with st.chat_message("user", avatar="🧑"):
                st.markdown(user_feedback)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🧠 Revising advice based on your feedback..."):
                    payload = {"thread_id": st.session_state.thread_id, "feedback_text": user_feedback}
                    try:
                        response = requests.post(f"{API_URL}/provide-feedback", json=payload)
                        if response.status_code == 200:
                            data = response.json()
                            new_advice = data.get("advice")
                            new_preds = data.get("predictions", {})
                            st.session_state.advice = new_advice
                            st.session_state.predictions = new_preds
                            st.session_state.chat_history.append({"role": "assistant", "content": new_advice})
                            st.markdown(new_advice)
                            st.rerun()
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Failed to reach API: {e}")

    with col_b:
        st.markdown("<div class='section-header'>🎯 Quick Actions</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='glass-card'>
            <div style='font-size:0.82rem; color:#94a3b8; margin-bottom:1rem;'>
                Try asking the AI to refine advice based on your situation:
            </div>
            <div style='display:flex;flex-direction:column;gap:0.5rem;'>
        """, unsafe_allow_html=True)

        suggestions = [
            "I can't reduce my rent",
            "Suggest food cost alternatives",
            "How do I invest the savings?",
            "Give me a monthly budget plan",
        ]
        for s in suggestions:
            st.markdown(f"""
            <div style='background:rgba(99,102,241,0.08);border:1px solid rgba(99,102,241,0.2);
                border-radius:8px;padding:8px 12px;font-size:0.8rem;color:#a5b4fc;cursor:default;'>
                💡 {s}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)
