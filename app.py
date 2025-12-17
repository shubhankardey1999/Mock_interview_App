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

# ✅ MOST STABLE MODEL
model = genai.GenerativeModel("gemini-1.0-pro")

# ---------------- SESSION STATE ----------------
if "question" not in st.session_state:
    st.session_state.question = None

# ---------------- STEP 1 ----------------
st.markdown("### Step 1: Enter the role you're preparing for")
job_role = st.text_input("Enter Role (e.g., Software Engineer, Data Analyst)")

# ---------------- STEP 2 ----------------
st.markdown("### Step 2: Click below to get a question")

if st.button("🧠 Generate Interview Question") and job_role.strip():
    question_prompt = f"""
    You are an expert interviewer.
    Ask ONE challenging interview question for a {job_role}.
    """

    response = model.generate_content(question_prompt)
    st.session_state.question = response.text.strip()

    st.markdown("#### 🗣 Interview Question")
    st.write(st.session_state.question)

# ---------------- STEP 3 ----------------
if st.session_state.question:
    st.markdown("### Step 3: Write your answer below")
    user_answer = st.text_area("Your Answer", height=200)

    if st.button("📊 Generate Feedback") and user_answer.strip():

        feedback_prompt = f"""
        Question:
        {st.session_state.question}

        Answer:
        {user_answer}

        Provide feedback with:
        - Strengths
        - Weaknesses
        - Improvement suggestions
        """

        feedback = model.generate_content(feedback_prompt)

        st.subheader("🧠 AI Feedback")
        st.write(feedback.text)

        rating_prompt = f"""
        Rate the answer out of 5.

        Question:
        {st.session_state.question}

        Answer:
        {user_answer}

        Format strictly:
        Rating: X/5
        Reason: one line
        """

        rating = model.generate_content(rating_prompt)

        st.subheader("⭐ Final Rating")
        st.write(rating.text)
