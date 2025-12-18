import streamlit as st
import google.generativeai as genai
import PyPDF2
import base64
import re

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="AI Based Mock Interview",
    layout="wide"
)

# ================= BACKGROUND =================
def set_background(image_path):
    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(6,10,18,0.88), rgba(6,10,18,0.88)),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background.png")

# ================= STYLING =================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
body {
    font-family: "Segoe UI", sans-serif;
    color: #F8FAFC;
}

/* ---------- TITLES ---------- */
.main-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 800;
    color: #4FE6D8;
    margin-top: 4.5rem;
}

.sub-title {
    text-align: center;
    font-size: 1.25rem;
    color: #E6FFFA;
    margin-bottom: 2rem;
}

/* ---------- SECTION HEADERS ---------- */
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #4FE6D8;
}

/* ---------- CARDS ---------- */
.card {
    background: rgba(15,23,42,0.92);
    border: 1px solid rgba(79,230,216,0.35);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1.6rem;
}

/* ---------- INPUTS ---------- */
.stTextInput input,
.stTextArea textarea {
    background-color: #1E293B;
    color: #F8FAFC;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.25);
}

/* ---------- LABELS ---------- */
label {
    color: #E6FFFA !important;
    font-weight: 500;
}

/* ---------- PLACEHOLDER ---------- */
::placeholder {
    color: #CBD5E1 !important;
}

/* ---------- CENTER JOB ROLE ---------- */
.center-input {
    display: flex;
    justify-content: center;
    margin-bottom: 1.5rem;
}

.center-input input {
    width: 40%;
    text-align: center;
}

/* ---------- BUTTON ---------- */
.stButton > button {
    background: linear-gradient(90deg, #4FE6D8, #38BDF8);
    color: #020617;
    font-weight: 700;
    border-radius: 10px;
    padding: 0.6em 1.4em;
    border: none;
    margin: auto;
    display: block;
}

/* ---------- QUESTION ---------- */
.question-title {
    color: #38BDF8;
    font-size: 1.4rem;
    font-weight: 700;
}

.question-text {
    color: #E6FFFA;
}

/* ---------- FEEDBACK ---------- */
.strengths-title { color: #4ADE80; font-weight: 700; }
.weaknesses-title { color: #F87171; font-weight: 700; }
.improvement-title { color: #FACC15; font-weight: 700; }

.feedback-content {
    color: #CBD5E1;
}

/* ---------- RATING ---------- */
.rating-text {
    color: #4ADE80;
    font-size: 1.3rem;
    font-weight: 800;
    text-align: center;
}

/* ---------- HIDE EMPTY CONTAINERS ---------- */
div[data-testid="column"] > div:empty {
    display: none !important;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLES =================
st.markdown("""
<div class="main-title">AI BASED MOCK INTERVIEW APP</div>
<div class="sub-title">
🤖 Leveraging Agentic AI for Automated Interview Questioning and Performance Evaluation 🚀
</div>
<hr>
""", unsafe_allow_html=True)

# ================= GEMINI =================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.5-flash-lite")

def safe_generate(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception:
        return ""

# ================= PDF =================
def extract_text(file):
    if not file:
        return ""
    reader = PyPDF2.PdfReader(file)
    return " ".join(p.extract_text() or "" for p in reader.pages)

# ================= SESSION =================
st.session_state.setdefault("questions", [])
st.session_state.setdefault("answers", {})
st.session_state.setdefault("feedback", {})
st.session_state.setdefault("started", False)

# ================= JOB ROLE =================
st.markdown('<div class="section-title">👨‍💼 Job Role</div>', unsafe_allow_html=True)
st.markdown('<div class="center-input">', unsafe_allow_html=True)
job_role = st.text_input(
    "",
    placeholder="Software Engineer, Business Analyst, HRBP",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ================= JD + RESUME =================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area("", height=90, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📑 Resume</div>', unsafe_allow_html=True)
    resume_pdf = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    resume_text = extract_text(resume_pdf)
    st.markdown('</div>', unsafe_allow_html=True)

# ================= START =================
if st.button("🚀 Start Interview"):
    if job_role and jd_text and resume_text:
        summary = safe_generate(f"Summarize Role:{job_role} JD:{jd_text} Resume:{resume_text}")
        q_text = safe_generate(f"Generate exactly 2 interview questions from: {summary}")
        st.session_state.questions = [q for q in q_text.split("\n") if q.strip()]
        st.session_state.started = True
        st.rerun()

# ================= INTERVIEW =================
if st.session_state.started:
    for i, q in enumerate(st.session_state.questions):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="question-title">🗣 Question {i+1}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="question-text">{q}</div>', unsafe_allow_html=True)
        ans = st.text_area("Your Answer", key=f"a{i}")
        st.markdown('</div>', unsafe_allow_html=True)
