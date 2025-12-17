import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Agentic Mock Interviewer",
    layout="centered"
)

st.title("🤖 Agentic Mock Interviewer + Feedback Generator")

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- SESSION STATE ----------------
if "question" not in st.session_state:
    st.session_state.question = None

# ---------------- STEP 1 ----------------
st.markdown("### **Step 1: Enter the role you're preparing for**")
job_role = st.text_input("Enter Role (e.g., Software Engineer, Data Analyst)")

# ---------------- STEP 2 ----------------
st.markdown("### **Step 2: Click below to get a question**")

if st.button("🧠 Generate Interview Question") and job_role.strip():
    question_prompt = f"""
    You are an expert technical interviewer.
    Ask ONE challenging and role-relevant interview question for a {job_role}.
    """

    response = model.generate_content(question_prompt)
    st.session_state.question = response.text.strip()

    st.markdown("#### 🗣 Interview Question")
    st.write(st.session_state.question)

# ---------------- STEP 3 ----------------
if st.session_state.question:
    st.markdown("### **Step 3: Write your answer below**")
    user_answer = st.text_area("Your Answer", height=200)

    if st.button("📊 Generate Feedback") and user_answer.strip():

        # ---------- FEEDBACK ----------
        feedback_prompt = f"""
        You are a professional interviewer.

        Question:
        {st.session_state.question}

        Candidate Answer:
        {user_answer}

        Provide structured feedback in bullet points covering:
        - Strengths
        - Weaknesses
        - How the answer can be improved
        """

        feedback_response = model.generate_content(feedback_prompt)

        st.subheader("🧠 AI Feedback")
        st.write(feedback_response.text)

        # ---------- RATING ----------
        rating_prompt = f"""
        You are an expert interviewer.

        Question:
        {st.session_state.question}

        Answer:
        {user_answer}

        Give a rating strictly in this format:
        Rating: X/5
        Reason: one-line justification
        """

        rating_response = model.generate_content(rating_prompt)

        st.subheader("⭐ Final Rating")
        st.write(rating_response.text)

