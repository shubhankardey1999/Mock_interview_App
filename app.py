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
    margin-bottom: 0.25rem;
}

.sub-title {
    text-align: center;
    font-size: 1.25rem;
    color: #E6FFFA;
    margin-bottom: 1.4rem;
}

/* ---------- SECTION HEADERS ---------- */
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #4FE6D8;
    margin-bottom: 0.4rem;
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

/* ---------- LABELS & PLACEHOLDERS ---------- */
label,
.stTextInput label,
.stTextArea label,
.stFileUploader label {
    color: #E6FFFA !important;
    font-weight: 500;
}

::placeholder {
    color: #CBD5E1 !important;
    opacity: 1;
}

.stFileUploader div,
.stFileUploader span {
    color: #E6FFFA !important;
}

/* ---------- JOB ROLE CENTER ---------- */
.center-input {
    display: flex;
    justify-content: center;
    margin-bottom: 1.4rem;
}

.center-input input {
    width: 40%;
    text-align: center;
    font-size: 1rem;
}

/* ---------- BUTTON ---------- */
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

/* ---------- HR ---------- */
hr {
    border: 1px solid rgba(79,230,216,0.35);
}

/* ---------- QUESTION TITLES ---------- */
.question-title {
    color: #38BDF8;
    font-size: 1.4rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
}

/* ---------- QUESTION TEXT ---------- */
.question-text {
    color: #E6FFFA;
    font-size: 1.15rem;
    font-weight: 500;
}

/* ---------- ANSWER LABEL ---------- */
.answer-label {
    color: #A7F3D0;
    font-weight: 600;
    margin-bottom: 0.3rem;
    margin-top: 1rem;
}

/* ---------- FEEDBACK HEADERS ---------- */
.feedback-header {
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
}

.strengths-title {
    color: #4ADE80;
}

.weaknesses-title {
    color: #F87171;
}

.improvement-title {
    color: #FACC15;
}

/* ---------- FEEDBACK CONTENT ---------- */
.feedback-content {
    color: #CBD5E1;
    line-height: 1.5;
    margin-bottom: 0.5rem;
}

/* ---------- RATING ---------- */
.rating-text {
    color: #4ADE80;
    font-size: 1.3rem;
    font-weight: 800;
}

/* ---------- CENTERED BUTTON CONTAINER ---------- */
.center-button {
    display: flex;
    justify-content: center;
    margin: 2rem 0;
}

/* ---------- ALERT ---------- */
.stAlert p {
    color: #FACC15 !important;
    font-weight: 500;
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
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "feedback" not in st.session_state:
    st.session_state.feedback = {}
if "started" not in st.session_state:
    st.session_state.started = False
if "summary" not in st.session_state:
    st.session_state.summary = ""

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
    jd_text = st.text_area("Paste Job Description", height=70)
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

# ================= CENTERED START BUTTON =================
st.markdown('<div class="center-button">', unsafe_allow_html=True)
if st.button("🚀 Start Interview", key="start_interview") and job_role and jd_text and resume_text:
    
    st.session_state.summary = safe_generate(
        f"""
        Summarize concisely:
        Role: {job_role}
        Job Description: {jd_text}
        Resume: {resume_text}
        """
    )
    
    q_text = safe_generate(
        f"""
        Generate EXACTLY 2 interview questions.
        Context:
        {st.session_state.summary}
        Format each question on a new line.
        """
    )
    
    st.session_state.questions = [q for q in q_text.split("\n") if q.strip()]
    st.session_state.started = True
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ================= INTERVIEW FLOW =================
if st.session_state.started:
    
    for i, q in enumerate(st.session_state.questions):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # Colored Question Title
        st.markdown(
            f'<div class="question-title">🗣 Question {i+1}</div>',
            unsafe_allow_html=True
        )
        
        st.markdown(f'<div class="question-text">{q}</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="answer-label">Your Answer</div>', unsafe_allow_html=True)
        ans = st.text_area("", key=f"a{i}", height=140)
        
        if ans and i not in st.session_state.answers:
            st.session_state.answers[i] = ans
            
            # Request structured HTML feedback from Gemini
            feedback_prompt = f"""
            Question: {q}
            Answer: {ans}
            
            Provide feedback in this EXACT HTML format:
            
            <h4 class="feedback-header strengths-title">Strengths</h4>
            <div class="feedback-content">
            <ul>
            <li>Point 1 (max 15 words)</li>
            <li>Point 2 (max 15 words)</li>
            </ul>
            </div>
            
            <h4 class="feedback-header weaknesses-title">Weaknesses</h4>
            <div class="feedback-content">
            <ul>
            <li>Point 1 (max 15 words)</li>
            <li>Point 2 (max 15 words)</li>
            </ul>
            </div>
            
            <h4 class="feedback-header improvement-title">Improvement Tips</h4>
            <div class="feedback-content">
            <ul>
            <li>Tip 1 (max 15 words)</li>
            <li>Tip 2 (max 15 words)</li>
            </ul>
            </div>
            """
            
            st.session_state.feedback[i] = safe_generate(feedback_prompt)
        
        if i in st.session_state.feedback:
            # Render the HTML feedback
            st.markdown(
                f'<div class="feedback-content">{st.session_state.feedback[i]}</div>',
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    if len(st.session_state.answers) == len(st.session_state.questions):
        rating = safe_generate(
            f"Rate interview out of 10. Answers: {st.session_state.answers}"
        )
        st.markdown(
            f'<div class="card"><div class="rating-text">⭐ Final Rating<br>{rating}</div></div>',
            unsafe_allow_html=True
        )
