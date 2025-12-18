import streamlit as st
import google.generativeai as genai
import PyPDF2
import base64

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Mock AI",
    layout="wide"
)

# ================= BACKGROUND IMAGE =================
def set_bg(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(
                    rgba(10, 15, 25, 0.88),
                    rgba(10, 15, 25, 0.88)
                ),
                url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("background.png")

# ================= PREMIUM UI =================
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
body {
    font-family: "Segoe UI", sans-serif;
    color: #e6f1f1;
}

/* ---------- TITLE ---------- */
.app-title {
    text-align: center;
    margin-bottom: 2rem;
}
.title-main {
    font-size: 2.6rem;
    font-weight: 700;
    color: #5eead4;
}
.title-sub {
    font-size: 1.9rem;
    font-weight: 500;
    color: #5eead4;
}

/* ---------- GLASS CARD ---------- */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(255,255,255,0.08);
}

/* ---------- INPUTS ---------- */
.stTextInput input, .stTextArea textarea {
    background-color: rgba(20,25,40,0.9);
    color: #e6f1f1;
    border-radius: 8px;
}

/* ---------- BUTTON ---------- */
.stButton>button {
    background: linear-gradient(90deg, #5eead4, #38bdf8);
    color: #020617;
    font-weight: 700;
    border-radius: 10px;
    padding: 0.6em 1.6em;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #38bdf8, #5eead4);
}

/* ---------- CENTER INPUT ---------- */
.center-box {
    display: flex;
    justify-content: center;
}

.center-box input {
    width: 45%;
    text-align: center;
    font-size: 1rem;
}

/* ---------- HEADINGS ---------- */
.section-title {
    color: #5eead4;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown("""
<div class="app-title">
    <div class="title-main">🤖 Leveraging Agentic AI</div>
    <div class="title-sub">for Automated Interview Questioning and Performance Evaluation 🚀</div>
</div>
""", unsafe_allow_html=True)

# ================= GEMINI CONFIG =================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.5-flash")

def safe_generate(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception:
        return "⚠️ AI response unavailable due to API limits."

# ================= PDF EXTRACTION =================
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([p.extract_text() or "" for p in reader.pages])

# ================= SESSION STATE =================
for key, default in {
    "questions": [],
    "answers": {},
    "feedback": {},
    "started": False,
    "summary": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ================= JOB ROLE =================
st.markdown('<div class="section-title">👨‍💼 Job Role</div>', unsafe_allow_html=True)
st.markdown('<div class="center-box">', unsafe_allow_html=True)
job_role = st.text_input(
    "Job Role",
    placeholder="Financial Analyst, Business Analyst",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ================= JD & RESUME =================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area("Paste Job Description", height=160)
    jd_pdf = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
    if jd_pdf:
        jd_text = extract_text_from_pdf(jd_pdf)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📑 Resume (PDF)</div>', unsafe_allow_html=True)
    resume_pdf = st.file_uploader("Upload Resume", type=["pdf"])
    resume_text = extract_text_from_pdf(resume_pdf) if resume_pdf else ""
    st.markdown('</div>', unsafe_allow_html=True)

# ================= START =================
if st.button("🚀 Start Interview") and job_role and jd_text and resume_text:

    summary_prompt = f"""
    Summarize this context into bullet points (max 120 words):
    Role: {job_role}
    JD: {jd_text}
    Resume: {resume_text}
    """

    st.session_state.summary = safe_generate(summary_prompt)

    q_prompt = f"""
    From this context, generate EXACTLY 2 interview questions.
    Return only numbered questions.
    Context:
    {st.session_state.summary}
    """

    q_text = safe_generate(q_prompt)
    st.session_state.questions = [q for q in q_text.split("\n") if q.strip()]
    st.session_state.started = True
    st.experimental_rerun()

# ================= INTERVIEW =================
if st.session_state.started:

    for i, q in enumerate(st.session_state.questions):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### 🗣 Question {i+1}")
        st.write(q)

        answer = st.text_area("Your Answer", key=f"a{i}", height=140)

        if answer and i not in st.session_state.answers:
            st.session_state.answers[i] = answer

            fb_prompt = f"""
            Question: {q}
            Answer: {answer}
            Give:
            - 2 strengths
            - 2 weaknesses
            - 2 improvements
            """

            st.session_state.feedback[i] = safe_generate(fb_prompt)

        if i in st.session_state.feedback:
            st.markdown("#### 🧠 AI Feedback")
            st.write(st.session_state.feedback[i])

        st.markdown('</div>', unsafe_allow_html=True)

    if len(st.session_state.answers) == len(st.session_state.questions):
        rating_prompt = f"""
        Rate overall interview out of 10.
        Answers: {st.session_state.answers}
        Format:
        Rating: X/10
        Reason: one line
        """
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⭐ Final Rating")
        st.write(safe_generate(rating_prompt))
        st.markdown('</div>', unsafe_allow_html=True)
