import streamlit as st
from openai import OpenAI

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Agentic Mock Interviewer",
    layout="centered"
)

st.title("🤖 Agentic Mock Interviewer + Feedback Generator")

# ---------------- OPENAI CLIENT ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- SESSION STATE ----------------
if "question" not in st.session_state:
    st.session_state.question = None

# ---------------- STEP 1 ----------------
st.markdown("### Step 1: Enter the role you're preparing for")
job_role = st.text_input(
    "Enter Role (e.g., Software Engineer, Data Analyst)"
)

# ---------------- STEP 2 ----------------
st.markdown("### Step 2: Click below to get a question")

if st.button("🧠 Generate Interview Question") and job_role.strip():

    prompt = f"""
    You are an expert interviewer.
    Ask ONE challenging and role-specific interview question
    for a {job_role}.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    st.session_state.question = response.choices[0].message.content.strip()

    st.markdown("#### 🗣 Interview Question")
    st.write(st.session_state.question)

# ---------------- STEP 3 ----------------
if st.session_state.question:
    st.markdown("### Step 3: Write your answer below")
    user_answer = st.text_area("Your Answer", height=200)

    if st.button("📊 Generate Feedback") and user_answer.strip():

        # ---------- FEEDBACK ----------
        feedback_prompt = f"""
        Question:
        {st.session_state.question}

        Candidate Answer:
        {user_answer}

        As an interviewer, provide structured feedback with:
        - Strengths
        - Weaknesses
        - Suggestions for improvement
        """

        feedback_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": feedback_prompt}],
            temperature=0.5
        )

        st.subheader("🧠 AI Feedback")
        st.write(feedback_response.choices[0].message.content)

        # ---------- RATING ----------
        rating_prompt = f"""
        Evaluate the following answer.

        Question:
        {st.session_state.question}

        Answer:
        {user_answer}

        Respond strictly in this format:
        Rating: X/5
        Reason: one-line justification
        """

        rating_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": rating_prompt}],
            temperature=0.4
        )

        st.subheader("⭐ Final Rating")
        st.write(rating_response.choices[0].message.content)
