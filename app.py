import streamlit as st
import google.generativeai as genai
import PyPDF2

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Mock AI",
    layout="wide"
)

# ================= CUSTOM STYLES =================
st.markdown("""
<style>
    body {
        background-color: #0e1117;
        color: #e6e6e6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #4fd1c5;
    }
    .stTextInput>div>div>input,
    .stTextArea textarea {
        background-color: #1a1f2b;
        color: white;
    }
    .stButton>button {
        background-color: #4fd1c5;
        color: black;
        border-radius: 10px;
        padding: 0.6em 1.4em;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #38b2ac;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Leveraging Agentic AI for Automated Interview Questioning and Performance Evaluation 🚀")
st.markdown("---")

# ================= GEMINI CONFIG =================
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ================= SAFE API CALL =================
def safe_generate(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception:
        return "⚠️ AI response could not be generated due to API limits. Please proceed."

# ================= PDF TEXT EXTRACTION =================
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ================= SESSION STATE =================
for key, default in {
    "questions": [],
    "current_q": 0,
    "started": False,
    "context_summary": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ================= INPUT SECTION =================
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🧑‍💼 Job Role")
    job_role = st.text_input(
        "Enter Job Role",
        placeholder="Business Analyst, Data Analyst, Software Engineer"
    )

with col2:
    st.markdown("### 📄 Job Description")
    jd_text = st.text_area(
        "Paste Job Description",
        height=160
    )
    jd_pdf = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
    if jd_pdf:
        jd_text = extract_text_from_pdf(jd_pdf)

st.markdown("### 📑 Upload Resume (PDF only)")
resume_pdf = st.file_uploader("Upload Resume", type=["pdf"])
resume_text = extract_text_from_pdf(resume_pdf) if resume_pdf else ""

st.markdown("---")

# ================= START INTERVIEW =================
if st.button("🚀 Start Mock Interview") and job_role and jd_text and resume_text:

    # ---- SUMMARIZE JD + RESUME ONCE ----
    summary_prompt = f"""
    Summarize the following into key bullet points (max 150 words total):

    Job Role:
    {job_role}

    Job Description:
    {jd_text}

    Resume:
    {resume_text}
    """

    st.session_state.context_summary = safe_generate(summary_prompt)

    # ---- GENERATE ONLY 2 QUESTIONS ----
    question_prompt = f"""
    Using the following context, generate EXACTLY 2 interview questions.
    Questions should be role-relevant, resume-based, and analytical.

    Context:
    {st.session_state.context_summary}

    Return only numbered questions.
    """

    questions_text = safe_generate(question_prompt)
    st.session_state.questions = [q for q in questions_text.split("\n") if q.strip()]
    st.session_state.current_q = 0
    st.session_state.started = True

    st.experimental_rerun()

# ================= INTERVIEW FLOW =================
if st.session_state.started:

    if st.session_state.current_q < len(st.session_state.questions):

        st.markdown(f"## 🗣 Question {st.session_state.current_q + 1}")
        st.markdown(st.session_state.questions[st.session_state.current_q])

        answer = st.text_area("✍️ Your Answer", height=200)

        if st.button("📊 Submit Answer") and answer.strip():

            feedback_prompt = f"""
            Question:
            {st.session_state.questions[st.session_state.current_q]}

            Answer:
            {answer}

            Give concise feedback:
            - 2 Strengths
            - 2 Weaknesses
            - 2 Improvement tips
            - Short sample improved answer
            """

            feedback_text = safe_generate(feedback_prompt)

            st.subheader("🧠 AI Feedback")
            st.write(feedback_text)

            st.session_state.current_q += 1
            st.experimental_rerun()

    else:
        st.success("🎉 Mock Interview Completed!")
        st.markdown("### ✅ You have completed all interview questions.")
        st.markdown("Thank you for using **Smart Mock AI**.")
