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

/* ---------- TITLES ---------- */
.main-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 800;
    color: #5EEAD4;
}
.sub-title {
    text-align: center;
    font-size: 1.25rem;
    color: #E6FFFA;
    margin-bottom: 1.4rem;
}

/* ---------- SECTIONS ---------- */
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #5EEAD4;
}

/* ---------- CARDS ---------- */
.card {
    background: rgba(15,23,42,0.95);
    border: 1px solid rgba(94,234,212,0.35);
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

/* ---------- PLACEHOLDER + LABELS ---------- */
label, .stFileUploader label {
    color: #E6FFFA !important;
}
::placeholder {
    color: #CBD5E1 !important;
}

/* ---------- JOB ROLE CENTER ---------- */
.center-input {
    display: flex;
    justify-content: center;
}
.center-input input {
    width: 40%;
    text-align: center;
}

/* ---------- CENTER BUTTON ---------- */
.center-btn {
    display: flex;
    justify-content: center;
    margin: 1.8rem 0;
}

/* ---------- BUTTON ---------- */
.stButton>button {
    background: linear-gradient(90deg, #5EEAD4, #38BDF8);
    color: #020617;
    font-weight: 800;
    border-radius: 14px;
    padding: 0.75em 2.4em;
    border: none;
    font-size: 1.05rem;
}

/* ---------- QUESTION ---------- */
.question-title {
    color: #38BDF8;
    font-size: 1.4rem;
    font-weight: 700;
}
.question-text {
    color: #E6FFFA;
    font-size: 1.1rem;
}

/* ---------- FEEDBACK COLORS ---------- */
.strengths-title { color: #4ADE80; font-weight: 700; }
.weaknesses-title { color: #F87171; font-weight: 700; }
.improvement-title { color: #FACC15; font-weight: 700; }

.feedback-text {
    color: #F8FAFC;
    line-height: 1.6;
}

/* ---------- RATING ---------- */
.rating-text {
    color: #4ADE80;
    font-size: 1.3rem;
    font-weight: 800;
}

hr { border: 1px solid rgba(94,234,212,0.35); }

</style>
""", unsafe_allow_html=True)

# ================= TITLES =================
st.markdown("""
<div class="main-title">AI BASED MOCK INTERVIEW</div>
<div class="sub-title">
Leveraging Agentic AI for Automated Interview Questioning and Performance Evaluation 🚀
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
        return "<p style='color:#FACC15;'>⚠️ AI feedback unavailable (quota limit).</p>"

# ================= PDF EXTRACTION =================
def extract_text(file):
    reader = PyPDF2.PdfReader(file)
    return " ".join([p.extract_text() or "" for p in reader.pages])

# ================= SESSION STATE =================
for key in ["questions", "answers", "feedback", "summary"]:
    if key not in st.session_state:
        st.session_state[key] = {} if key in ["answers","feedback"] else []
if "started" not in st.session_state:
    st.session_state.started = False

# ================= JOB ROLE =================
st.markdown('<div class="section-title">👨‍💼 Job Role</div>', unsafe_allow_html=True)
st.markdown('<div class="center-input">', unsafe_allow_html=True)
job_role = st.text_input("", placeholder="Financial Analyst, Business Analyst")
st.markdown('</div>', unsafe_allow_html=True)

# ================= JD + RESUME =================
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="card"><div class="section-title">📄 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area("", height=80)
    jd_pdf = st.file_uploader("Upload JD (PDF)", type=["pdf"])
    if jd_pdf:
        jd_text = extract_text(jd_pdf)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card"><div class="section-title">📑 Resume (PDF)</div>', unsafe_allow_html=True)
    resume_pdf = st.file_uploader("Upload Resume", type=["pdf"])
    resume_text = extract_text(resume_pdf) if resume_pdf else ""
    st.markdown('</div>', unsafe_allow_html=True)

# ================= START INTERVIEW =================
st.markdown('<div class="center-btn">', unsafe_allow_html=True)
start = st.button("🚀 Start Interview")
st.markdown('</div>', unsafe_allow_html=True)

if start and job_role and jd_text and resume_text:
    st.session_state.summary = safe_generate(
        f"Summarize briefly: Role={job_role}, JD={jd_text}, Resume={resume_text}"
    )
    q_text = safe_generate(
        f"Generate EXACTLY 2 interview questions from: {st.session_state.summary}"
    )
    st.session_state.questions = [q for q in q_text.split("\n") if q.strip()]
    st.session_state.started = True
    st.experimental_rerun()

# ================= INTERVIEW FLOW =================
if st.session_state.started:
    for i, q in enumerate(st.session_state.questions):
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown(
            f'<div class="question-title">🗣 Question {i+1}</div>',
            unsafe_allow_html=True
        )
        st.markdown(f'<div class="question-text">{q}</div>', unsafe_allow_html=True)

        ans = st.text_area("Your Answer", key=f"a{i}", height=120)

        if ans and i not in st.session_state.answers:
            st.session_state.answers[i] = ans
            st.session_state.feedback[i] = safe_generate(
                f"""
                Give SHORT HTML feedback:
                <h4 class='strengths-title'>Strengths</h4><ul><li>...</li><li>...</li></ul>
                <h4 class='weaknesses-title'>Weaknesses</h4><ul><li>...</li><li>...</li></ul>
                <h4 class='improvement-title'>Improvement Tips</h4><ul><li>...</li><li>...</li></ul>
                Question: {q}
                Answer: {ans}
                """
            )

        if i in st.session_state.feedback:
            st.markdown(
                f"<div class='feedback-text'>{st.session_state.feedback[i]}</div>",
                unsafe_allow_html=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

    if len(st.session_state.answers) == len(st.session_state.questions):
        rating = safe_generate(f"Give rating out of 10. Answers: {st.session_state.answers}")
        st.markdown(
            f"<div class='card'><div class='rating-text'>⭐ Final Rating<br>{rating}</div></div>",
            unsafe_allow_html=True
        )
