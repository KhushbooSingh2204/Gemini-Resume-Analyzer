import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Resume Analyzer")

# Title
st.title("📄 AI Resume Analyzer")
st.caption("Analyze resumes using Gemini AI and get ATS-style feedback")

# Sidebar
st.sidebar.header("About")

st.sidebar.info("""
This AI Resume Analyzer uses Gemini AI to:

• Evaluate resumes
• Generate ATS score
• Identify missing skills
• Suggest improvements
• Assess job readiness
""")

# API Key
api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

# Job Role
job_role = st.text_input(
    "Target Job Role",
    placeholder="Data Analyst, AI Engineer, Prompt Engineer..."
)

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type="pdf"
)

# Process Resume
if uploaded_file and api_key:

    genai.configure(api_key=api_key)

    pdf_reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in pdf_reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text

    st.success("✅ Resume uploaded successfully")

    # Resume Statistics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Characters", len(resume_text))

    with col2:
        st.metric("Words", len(resume_text.split()))

    # Analyze Button
    if st.button("🔍 Analyze Resume"):

        if not job_role:
            st.warning("Please enter a target job role.")
        else:

            prompt = f"""
            Analyze this resume for the role of {job_role}.

            Provide:

            1. ATS Score (0-100)
            2. Overall Resume Score
            3. Key Strengths
            4. Missing Skills
            5. Weak Areas
            6. Suggested Improvements
            7. Interview Readiness
            8. Final Recommendation

            Resume:
            {resume_text}
            """

            model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            with st.spinner("Analyzing Resume..."):
                response = model.generate_content(prompt)

            st.subheader("📊 Resume Analysis")
            st.write(response.text)

# Validation Messages
elif uploaded_file and not api_key:
    st.warning("Please enter your Gemini API Key.")

elif api_key and not uploaded_file:
    st.info("Upload a resume PDF to begin analysis.")

# Footer
st.markdown("---")
st.caption(
    "Built with Gemini AI, Streamlit and PyPDF"
)