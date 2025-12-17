import streamlit as st
import google.generativeai as genai
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🎓 Smart Mock AI",
    layout="centered"
)

st.title("🤖 Leveraging Agentic AI for Automated Interview Questioning and Performance Evaluation 🚀")

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- HELPER FUNCTION ----------------
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# ---------------- SESSION STATE ----------------
if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "started" not in st.session_state:
    st.session_state.started = False

# ---------------- STEP 1: ROLE ----------------
st.markdown("### 🧑‍💼 Enter Job Role")
job_role = st.text_input("Job Role (e.g., Software Engineer, Marketing Executive, Data Analyst, HRBP)")

# ---------------- STEP 2: JOB DESCRIPTION ----------------
st.markdown("### 📄 Job Description")
jd_text = st.text_area("Write Job Description (OR upload PDF below)", height=150)

jd_pdf = st.file_uploader("Upload Job Description (PDF only)", type=["pdf"])
if jd_pdf:
    jd_text = extract_text_from_pdf(jd_pdf)

# ---------------- STEP 3: RESUME ----------------
st.markdown("### 📑 Upload Resume (PDF only)")
resume_pdf = st.file_uploader("Upload Resume", type=["pdf"])
resume_text = extract_text_from_pdf(resume_pdf) if resume_pdf else ""

# ---------------- STEP 4: GENERATE QUESTIONS ----------------
if st.button("🚀 Start Mock Interview") and job_role and jd_text and resume_text:

    question_prompt = f"""
    You are an expert interviewer.

    Job Role:
    {job_role}

    Job Description:
    {jd_text}

    Candidate Resume:
    {resume_text}

    Generate 6 to 10 interview questions.
    Questions should be:
    - Resume-based
    - Job-description aligned
    - Increasing in difficulty
    - Technical + behavioral mix

    Return ONLY numbered questions.
    """

    response = model.generate_content(question_prompt)
    raw_questions = response.text.strip().split("\n")

    st.session_state.questions = [q for q in raw_questions if q.strip()]
    st.session_state.current_q = 0
    st.session_state.started = True

# ---------------- INTERVIEW FLOW ----------------
if st.session_state.started:

    if st.session_state.current_q < len(st.session_state.questions):

        st.markdown(f"## 🗣 Question {st.session_state.current_q + 1}")
        st.write(st.session_state.questions[st.session_state.current_q])

        answer = st.text_area("Your Answer", height=200)

        if st.button("📊 Submit Answer") and answer.strip():

            # -------- FEEDBACK --------
            feedback_prompt = f"""
            You are a professional interviewer.

            Question:
            {st.session_state.questions[st.session_state.current_q]}

            Candidate Answer:
            {answer}

            Provide feedback:
            - Strengths (≤300 words)
            - Weaknesses (≤300 words)
            - Improvement suggestions (≤100 words)
            - Sample ideal answer
            """

            feedback = model.generate_content(feedback_prompt)

            st.subheader("🧠 AI Feedback")
            st.write(feedback.text)

            # Move to next question
            st.session_state.current_q += 1
            st.button("➡️ Next Question")

    else:
        st.success("🎉 Mock Interview Completed!")
        st.markdown("### ✅ You have answered all questions. Great job!")


