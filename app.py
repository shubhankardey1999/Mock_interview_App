import streamlit as st
import google.generativeai as genai
import PyPDF2
import base64
import re

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

/* ---------- TITLES WITH TOP MARGIN ---------- */
.main-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 800;
    color: #4FE6D8;
    margin-bottom: 0.25rem;
    margin-top: 4.5rem !important;
}

.sub-title {
    text-align: center;
    font-size: 1.25rem;
    color: #E6FFFA;
    margin-bottom: 2.4rem;
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
    padding: 1rem;
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
    padding: 0.6em 1.2em !important;
    border: none;
    display: block;
    margin-left: auto;
    margin-right: auto;
    min-width: 180px !important;
    width: auto !important;
    max-width: 200px !important;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #38BDF8, #4FE6D8);
}

/* ---------- HR ---------- */
hr {
    border: 1px solid rgba(79,230,216,0.35);
    margin-top: 1rem !important;
    margin-bottom: 1.5rem !important;
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
    text-align: center;
}

.rating-justification {
    color: #CBD5E1;
    font-size: 1rem;
    text-align: center;
    margin-top: 0.5rem;
    font-style: italic;
}

/* ---------- REMOVE EXTRA SPACING ---------- */
[data-testid="stVerticalBlock"] > [style*="flex-direction: column;"] > [data-testid="stVerticalBlock"] {
    gap: 0rem;
}

.st-emotion-cache-1jicfl2 {
    padding-top: 0rem;
}

/* ---------- CENTER ALL BUTTONS ---------- */
div[data-testid="column"] .stButton {
    display: flex;
    justify-content: center;
}

/* ---------- REMOVE UNNECESSARY PADDING ---------- */
.st-emotion-cache-1y4p8pa {
    padding: 1rem 1rem 0rem;
}

/* ---------- HIDE EMPTY CONTAINERS ---------- */
div.stButton > button:empty {
    display: none;
}

/* ---------- ALERT ---------- */
.stAlert p {
    color: #FACC15 !important;
    font-weight: 500;
}

/* ---------- FILE UPLOADER STYLING ---------- */
.stFileUploader {
    margin-bottom: 0.5rem;
}

/* ---------- ADD TOP SPACING TO MAIN CONTAINER ---------- */
.st-emotion-cache-1v0mbdj {
    margin-top: 0.5rem;
}

/* ---------- NARROWER BUTTON CONTAINER ---------- */
.narrow-button-container {
    display: flex;
    justify-content: center;
    margin: 1rem 0;
}

.narrow-button-container .stButton > button {
    min-width: 160px !important;
    max-width: 180px !important;
    padding: 0.5em 1em !important;
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
model = genai.GenerativeModel("models/gemini-2.5-flash-lite")


def safe_generate(prompt):
    try:
        return model.generate_content(prompt).text
    except Exception:
        return "⚠️ AI response could not be generated due to API limits."


# ================= CLEAN FEEDBACK TEXT =================
def clean_feedback_text(feedback):
    """Remove unwanted HTML tags and artifacts from feedback text"""
    if not feedback:
        return ""

    # Remove triple backticks and html markers
    feedback = re.sub(r'```html|```', '', feedback, flags=re.IGNORECASE)

    # Remove any stray quotes at the beginning or end
    feedback = feedback.strip().strip('"').strip("'")

    # Remove any "html" text that might appear at the beginning
    if feedback.lower().startswith('html'):
        feedback = feedback[4:].strip()

    # Remove any markdown code blocks
    feedback = re.sub(r'^```.*?```', '', feedback, flags=re.DOTALL | re.MULTILINE)

    # Clean up extra whitespace
    feedback = re.sub(r'\n\s*\n', '\n\n', feedback)

    return feedback.strip()


# ================= PDF EXTRACTION =================
def extract_text(file):
    if file:
        reader = PyPDF2.PdfReader(file)
        return " ".join([p.extract_text() or "" for p in reader.pages])
    return ""


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
if "submitted" not in st.session_state:
    st.session_state.submitted = {}

# ================= JOB ROLE =================
st.markdown('<div class="section-title">👨‍💼 Job Role</div>', unsafe_allow_html=True)
st.markdown('<div class="center-input">', unsafe_allow_html=True)
job_role = st.text_input(
    "Job Role",
    placeholder="Software Engineer, Marketing Executive, Business Analyst, HRBP..",
    label_visibility="collapsed",
    key="job_role_input"
)
st.markdown('</div>', unsafe_allow_html=True)

# ================= JD + RESUME =================
col1, col2 = st.columns(2)

with col1:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📄 Job Description</div>', unsafe_allow_html=True)
    jd_text = st.text_area("Write Job Description", height=40, key="jd_text_area")
    jd_pdf = st.file_uploader("Upload Job Description (PDF)", type=["pdf"], key="jd_uploader")
    if jd_pdf:
        jd_text = extract_text(jd_pdf) or jd_text
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
  #  /*st.markdown('<div class="card">', unsafe_allow_html=True)*/
    st.markdown('<div class="section-title">📑 Resume </div>', unsafe_allow_html=True)
    resume_pdf = st.file_uploader("Upload Resume (Only PDF format)", type=["pdf"], key="resume_uploader")
    resume_text = extract_text(resume_pdf) if resume_pdf else ""
    st.markdown('</div>', unsafe_allow_html=True)

# ================= CENTERED START BUTTON =================
st.markdown('<div class="narrow-button-container">', unsafe_allow_html=True)
if st.button("🚀 Start Interview", key="start_interview", use_container_width=False):
    if job_role and (jd_text or jd_pdf) and resume_pdf:
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
        st.session_state.answers = {}
        st.session_state.feedback = {}
        st.session_state.submitted = {}
        st.rerun()
    else:
        st.warning("Please fill in all fields: Job Role, Job Description, and upload a Resume.")
st.markdown('</div>', unsafe_allow_html=True)

# ================= INTERVIEW FLOW =================
if st.session_state.started:

    for i, q in enumerate(st.session_state.questions):
        #st.markdown('<div class="card">', unsafe_allow_html=True)

        # Colored Question Title
        st.markdown(
            f'<div class="question-title">🗣 Question {i + 1}</div>',
            unsafe_allow_html=True
        )

        st.markdown(f'<div class="question-text">{q}</div>', unsafe_allow_html=True)

        st.markdown('<div class="answer-label">Your Answer</div>', unsafe_allow_html=True)
        ans = st.text_area("", key=f"a{i}", height=140, label_visibility="collapsed")

        # Centered Submit Button for each question
        st.markdown('<div class="narrow-button-container">', unsafe_allow_html=True)
        if st.button(f"✅ Submit Answer {i + 1}", key=f"submit_{i}", use_container_width=False):
            if ans:
                st.session_state.answers[i] = ans
                st.session_state.submitted[i] = True

                # Request structured HTML feedback from Gemini
                feedback_prompt = f"""
                Question: {q}
                Answer: {ans}

                Provide feedback in this EXACT HTML format (NO backticks, NO code blocks, just plain HTML):

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

                IMPORTANT: Do NOT wrap this in ```html or any code blocks. Just provide the HTML directly.
                """

                raw_feedback = safe_generate(feedback_prompt)
                # Clean the feedback before storing
                st.session_state.feedback[i] = clean_feedback_text(raw_feedback)
                st.rerun()
            else:
                st.warning("Please enter an answer before submitting.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Show feedback if submitted
        if i in st.session_state.submitted and st.session_state.submitted[i]:
            st.markdown("---")
            if i in st.session_state.feedback and st.session_state.feedback[i]:
                # Render the cleaned HTML feedback
                st.markdown(
                    f'<div class="feedback-content">{st.session_state.feedback[i]}</div>',
                    unsafe_allow_html=True
                )

        st.markdown('</div>', unsafe_allow_html=True)

    # Final Rating
    if len(st.session_state.answers) == len(st.session_state.questions):
        rating_prompt = f"""
        Rate this interview out of 10.
        Questions: {st.session_state.questions}
        Answers: {st.session_state.answers}

        Provide output in this exact format:
        RATING: X/10
        JUSTIFICATION: [one-line justification here]
        """

        rating_response = safe_generate(rating_prompt)

        # Parse the response
        rating = "7/10"
        justification = "Good overall performance with room for improvement."

        if "RATING:" in rating_response:
            lines = rating_response.split("\n")
            for line in lines:
                if line.startswith("RATING:"):
                    rating = line.replace("RATING:", "").strip()
                elif line.startswith("JUSTIFICATION:"):
                    justification = line.replace("JUSTIFICATION:", "").strip()

        st.markdown(
            f'''
            <div class="card">
                <div class="rating-text">⭐ Overall Interview Rating</div>
                <div class="rating-text">{rating}</div>
                <div class="rating-justification">"{justification}"</div>
            </div>
            ''',
            unsafe_allow_html=True
        )













