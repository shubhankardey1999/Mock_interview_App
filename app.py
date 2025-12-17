import streamlit as st
from openai import OpenAI

# Page config
st.set_page_config(
    page_title="Agentic Mock Interviewer",
    layout="centered"
)

st.title("🤖 Agentic Mock Interviewer + Feedback Generator")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- STEP 1 ----------------
st.markdown("### **Step 1: Enter the role you're preparing for**")
job_role = st.text_input("Enter Role (e.g., Data Scientist at Google)")

# ---------------- STEP 2 ----------------
st.markdown("### **Step 2: Click below to get a question**")
question = ""

if st.button("🧠 Generate Interview Question"):
    prompt = f"""
    You're an expert interviewer.
    Ask a challenging and relevant interview question for the role: {job_role}.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    question = response.choices[0].message.content
    st.session_state["question"] = question

    st.markdown(f"#### 🗣 Interview Question:\n{question}")

# ---------------- STEP 3 ----------------
if "question" in st.session_state:
    st.markdown("### **Step 3: Write your answer below**")
    user_answer = st.text_area("Your Answer", height=200)

    # ---------------- FEEDBACK ----------------
    if st.button("📊 Generate Feedback"):
        feedback_prompt = f"""
        You're a professional interviewer.

        Question:
        {st.session_state['question']}

        Answer:
        {user_answer}

        Provide constructive feedback in bullet points including:
        - Strengths
        - Weaknesses
        - How the answer can be improved
        """

        feedback = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": feedback_prompt}],
            temperature=0.7
        )

        st.subheader("🧠 AI Feedback")
        st.markdown(feedback.choices[0].message.content)

        # ---------------- RATING ----------------
        rating_prompt = f"""
        You are an expert interviewer.

        Question:
        {st.session_state['question']}

        Answer:
        {user_answer}

        Respond in this format only:
        Rating: X/5
        Reason: <one-line justification>
        """

        rating_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": rating_prompt}],
            temperature=0.7
        )

        st.subheader("⭐ Final Rating")
        st.markdown(rating_response.choices[0].message.content)
