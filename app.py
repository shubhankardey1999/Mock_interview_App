import streamlit as st
import google.generativeai as genai
import PyPDF2
import base64

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Mock AI",
    layout="wide"
)

# ================= BACKGROUND =================
def set_bg(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(
                    rgba(8, 12, 20, 0.92),
                    rgba(8, 12, 20, 0.92)
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

# ================= UI STYLE =================
st.markdown("""
<style>

/* -------- GLOBAL -------- */
body {
    font-family: "Segoe UI", sans-serif;
    color: #EAFBFF;
}

/* -------- TITLE -------- */
.center-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    color: #4FE6D8;
    margin-bottom: 1.2rem;
}

/* -------- SECTION HEADERS -------- */
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #4FE6D8;
    margin-bottom: 0.4rem;
}

/* -------- CARD -------- */
.card {
    background: rgba(15, 22, 35, 0.95);
    border: 1px solid rgba(79, 230, 216, 0.25);
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 1.5rem;
}

/* -------- INPUTS -------- */
.stTextInput input,
.stTextArea textarea {
    background-color: #111827;
    color: #EAFBFF;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.15);
}

/* -------- CENTER INPUT -------- */
.center-box {
    display: flex;
    justify-content: center;
    margin-bottom: 1.2rem;
}

.center-box input {
    width: 45%;
    text-align: center;
    font-size: 1rem;
}

/* -------- BUTTON -------- */
.stButton>button {
    background: linear-gradient(90deg, #4FE6D8, #38BDF8);
    color: #020617;
    font-weight: 700;
    border-radius: 10px;
    padding: 0.6em 1.6em;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #38BDF8, #4FE6D8);
}

hr {
    border: 1px solid rgba(79,230,216,0.35);
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE (ONE LINE, CENTERED) =================
st.markdown("""
<div class="center-title">
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
        return "⚠️ AI response unavailable due to API limits."

# ================= PDF READER =================
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([p.extract_text() or "" for p in reader.pages])

# ================= SESSION STATE =================
for k, v in {
    "questions": [],
    "answers": {},
    "feedback": {},
    "started": False,
    "summary": ""
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

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
    Summarize into bullet points (max 120 words):
    Role: {job_role}
    JD: {jd_text}
    Resume: {resume_text}
    """

    st.session_state.summary = safe_generate(summary_prompt)

    q_prompt = f"""
    Generate EXACTLY 2 interview questions from this context.
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
            st.session_state.feedback[i] = safe_generate(
                f"""
                Question: {q}
                Answer: {answer}
                Give:
                - 2 strengths
                - 2 weaknesses
                - 2 improvements
                """
            )

        if i in st.session_state.feedback:
            st.markdown("#### 🧠 AI Feedback")
            st.write(st.session_state.feedback[i])

        st.markdown('</div>', unsafe_allow_html=True)

    if len(st.session_state.answers) == len(st.session_state.questions):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### ⭐ Final Rating")
        st.write(safe_generate(
            f"Rate interview out of 10. Answers: {st.session_state.answers}"
        ))
        st.markdown('</div>', unsafe_allow_html=True)
