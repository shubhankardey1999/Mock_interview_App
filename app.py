import streamlit as st
import google.generativeai as genai
import PyPDF2
import base64

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
                linear-gradient(rgba(5,12,22,0.82), rgba(5,12,22,0.82)),
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
    font-size: 2.7rem;
    font-weight: 900;
    color: #5EEAD4;
    margin-bottom: 0.3rem;
}

.sub-title {
    text-align: center;
    font-size: 1.25rem;
    color: #E0F2FE;
    margin-bottom: 1.6rem;
}

/* ---------- SECTION HEADERS ---------- */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #67E8F9;
    margin-bottom: 0.6rem;
}

/* ---------- CARDS ---------- */
.card {
    background: rgba(15,23,42,0.90);
    border: 1px solid rgba(94,234,212,0.45);
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.8rem;
}

/* ---------- INPUTS ---------- */
.stTextInput input,
.stTextArea textarea {
    background-color: #1E293B;
    color: #F8FAFC;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.3);
}

/* ---------- LABELS ---------- */
label,
.stTextInput label,
.stTextArea label,
.stFileUploader label {
    color: #E5F9F6 !important;
    font-weight: 600;
}

/* ---------- PLACEHOLDER ---------- */
::placeholder {
    color: #CBD5E1 !important;
    opacity: 1;
}

/* ---------- FILE UPLOADER ---------- */
.stFileUploader div,
.stFileUploader span {
    color: #E5F9F6 !important;
}

/* ---------- JOB ROLE CENTER ---------- */
.center-input {
    display: flex;
    justify-content: center;
    margin-bottom: 1.6rem;
}

.center-input input {
    width: 38%;
    text-align: center;
    font-size: 1rem;
}

/* ---------- BUTTON ---------- */
.center-btn {
    display: flex;
    justify-content: center;
    margin-top: 1.2rem;
}

.stButton>button {
    background: linear-gradient(90deg, #5EEAD4, #38BDF8);
    color: #020617;
    font-weight: 800;
    border-radius: 12px;
    padding: 0.7em 2em;
    border: none;
    font-size: 1rem;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #38BDF8, #5EEAD4);
}

/* ---------- QUESTION ---------- */
.question-text {
    color: #E0F2FE;
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

/* ---------- ANSWER ---------- */
.answer-label {
    color: #A7F3D0;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

/* ---------- FEEDBACK ---------- */
.feedback-title {
    color: #FACC15;
    font-weight: 800;
    margin-top: 1rem;
    margin-bottom: 0.4rem;
    font-size: 1.1rem;
}

.feedback-text {
    color: #F8FAFC;
    line-height: 1.65;
}

/* ---------- RATING ---------- */
.rating-text {
    color: #4ADE80;
    font-size: 1.35rem;
    font-weight: 900;
    text-align: center;
}

/* ---------- HR ---------- */
hr {
    border: 1px solid rgba(94,234,212,0.45);
}

</style>
""", unsafe_allow_html=True)

# ================= TITLES =================
st.markdown("""
<div class="main-title">AI BASED MOCK INTERVIEW</div>
<div class="sub-title">
🤖 Leveraging Agentic AI for Automated Interview Questioning and Performance Evaluation 🚀
</div>
<hr>
""", unsafe_allow_html=True)

# ================= GEMINI CONFIG =================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.5-flash")

def safe_generate(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception:
        return "⚠️ AI response could not be generated due to API limits."

# ================= PDF EXTRACTION =================
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([p.extract_text() or "" for p in reader.pages])

# ================= SESSION STATE =================
for key, val in {
    "questions": [],
    "answers": {},
    "feedback": {},
    "started": False,
    "summary": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ================= JOB ROLE =================
st.markdown('<div class="section-title">👨‍💼 Job Role</div>', unsafe_allow_html=True)
st.markdown('<div class="center-input">', unsafe_allow_html=True)
job_role = st.text_input(
    "Job Role",
    placeholder="Financial Analyst, Business Analyst",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ================= JD + RESUME =================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area("Paste Job Description", height=90)
    jd_pdf = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
    if jd_pdf:
        jd_text = extract_text(jd_pdf)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📑 Resume (PDF)</div>', unsafe_allow_html=True)
    resume_pdf = st.file_uploader("Upload Resume", type=["pdf"])
    resume_text = extract_text(resume_pdf) if resume_pdf else ""
    st.markdown('</div>', unsafe_allow_html=True)

# ================= START INTERVIEW =================
st.markdown('<div class="center-btn">', unsafe_allow_html=True)
start = st.button("🚀 Start Interview")
st.markdown('</div>', unsafe_allow_html=True)

if start and job_role and jd_text and resume_text:
    st.session_state.summary = safe_generate(
        f"Summarize concisely:\nRole:{job_role}\nJD:{jd_text}\nResume:{resume_text}"
    )
    q_text = safe_generate(
        f"Generate EXACTLY 2 interview questions.\nContext:\n{st.session_state.summary}"
    )
    st.session_state.questions = [q for q in q_text.split("\n") if q.strip()]
    st.session_state.started = True
    st.experimental_rerun()

# ================= INTERVIEW FLOW =================
if st.session_state.started:

    for i, q in enumerate(st.session_state.questions):
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(f"### 🗣 Question {i+1}")
        st.markdown(f'<div class="question-text">{q}</div>', unsafe_allow_html=True)

        st.markdown('<div class="answer-label">Your Answer</div>', unsafe_allow_html=True)
        ans = st.text_area("", key=f"a{i}", height=140)

        if ans and i not in st.session_state.answers:
            st.session_state.answers[i] = ans
            st.session_state.feedback[i] = safe_generate(
                f"""
                Question: {q}
                Answer: {ans}
                Provide:
                - Strengths (2 points)
                - Weaknesses (2 points)
                - Improvement Tips (2 points)
                """
            )

        if i in st.session_state.feedback:
            st.markdown('<div class="feedback-title">🧠 AI Feedback</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="feedback-text">{st.session_state.feedback[i]}</div>',
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    if len(st.session_state.answers) == len(st.session_state.questions):
        rating = safe_generate(
            f"Rate interview out of 10 with one-line reason.\nAnswers:{st.session_state.answers}"
        )
        st.markdown(
            f'<div class="card"><div class="rating-text">⭐ Final Rating<br>{rating}</div></div>',
            unsafe_allow_html=True
        )
