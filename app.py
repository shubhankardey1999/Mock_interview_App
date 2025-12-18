import streamlit as st
import google.generativeai as genai
import PyPDF2

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Smart Mock AI",
    layout="wide"
)

# ================= CUSTOM UI =================
st.markdown("""
<style>
body { background-color: #0e1117; color: #e6e6e6; }
h1, h2, h3 { color: #4fd1c5; }
.stTextInput input, .stTextArea textarea {
    background-color: #1a1f2b;
    color: white;
}
.stButton>button {
    background-color: #4fd1c5;
    color: black;
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
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
        return "⚠️ AI feedback could not be generated due to API limits."

# ================= PDF TEXT EXTRACTION =================
def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

# ================= SESSION STATE =================
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "feedback" not in st.session_state:
    st.session_state.feedback = {}
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "started" not in st.session_state:
    st.session_state.started = False
if "summary" not in st.session_state:
    st.session_state.summary = ""

# ================= JOB ROLE =================
st.markdown("## 👨‍💼 Job Role")
job_role = st.text_input("Enter Job Role")

# ================= JD + RESUME LAYOUT =================
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 📄 Job Description")
    jd_text = st.text_area("Paste Job Description", height=100)
    jd_pdf = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
    if jd_pdf:
        jd_text = extract_text_from_pdf(jd_pdf)

with col2:
    st.markdown("## 📑 Upload Resume (PDF only)")
    resume_pdf = st.file_uploader("Upload Resume", type=["pdf"])
    resume_text = extract_text_from_pdf(resume_pdf) if resume_pdf else ""

st.markdown("---")

# ================= START INTERVIEW =================
if st.button("🚀 Start Interview") and job_role and jd_text and resume_text:

    summary_prompt = f"""
    Summarize the following in bullet points (max 120 words):

    Job Role: {job_role}
    Job Description: {jd_text}
    Resume: {resume_text}
    """

    st.session_state.summary = safe_generate(summary_prompt)

    question_prompt = f"""
    Based on the context below, generate EXACTLY 2 interview questions.

    Context:
    {st.session_state.summary}

    Return only numbered questions.
    """

    q_text = safe_generate(question_prompt)
    st.session_state.questions = [q for q in q_text.split("\n") if q.strip()]
    st.session_state.started = True
    st.session_state.current_q = 0

    st.experimental_rerun()

# ================= INTERVIEW FLOW =================
if st.session_state.started:

    for i in range(len(st.session_state.questions)):
        st.markdown(f"## 🗣 Question {i+1}")
        st.write(st.session_state.questions[i])

        # Answer box
        answer = st.text_area(
            f"Answer for Question {i+1}",
            key=f"answer_{i}",
            height=150
        )

        if answer and i not in st.session_state.answers:
            st.session_state.answers[i] = answer

            feedback_prompt = f"""
            Question:
            {st.session_state.questions[i]}

            Answer:
            {answer}

            Provide:
            - 2 strengths
            - 2 weaknesses
            - 2 improvement tips
            """

            st.session_state.feedback[i] = safe_generate(feedback_prompt)

        # Show feedback if available
        if i in st.session_state.feedback:
            st.subheader("🧠 AI Feedback")
            st.write(st.session_state.feedback[i])

        st.markdown("---")

    # ================= FINAL RATING =================
    if len(st.session_state.answers) == len(st.session_state.questions):

        rating_prompt = f"""
        Based on the following answers, give an overall rating out of 10.

        Answers:
        {st.session_state.answers}

        Format:
        Rating: X/10
        Reason: one line
        """

        st.subheader("⭐ Final Rating")
        st.write(safe_generate(rating_prompt))

