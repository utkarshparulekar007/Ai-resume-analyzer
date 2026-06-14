import streamlit as st
import pdfplumber

from skills import job_roles

st.set_page_config(
    page_title="AI Resume Analyzer"
)

st.title("AI Resume Analyzer")
st.subheader("Smart Resume Screening and Skill Analysis")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

selected_role = st.selectbox(
    "Select Target Job Role",
    list(job_roles.keys())
)

if uploaded_file:

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:

        for page in pdf.pages:
            text += page.extract_text()

    text = text.lower()

    required_skills = job_roles[selected_role]

    found_skills = []

    missing_skills = []

    for skill in required_skills:

        if skill.lower() in text:
            found_skills.append(skill)

        else:
            missing_skills.append(skill)

    score = (
        len(found_skills)
        / len(required_skills)
    ) * 100

    st.header("Analysis Report")

    st.write(
        f"Resume Match Score: {score:.2f}%"
    )

    st.subheader("Detected Skills")

    if found_skills:
        for skill in found_skills:
            st.success(skill)

    st.subheader("Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.error(skill)

    st.subheader("Recommendation")

    if score >= 80:
        st.success(
            "Excellent Resume Match"
        )

    elif score >= 50:
        st.warning(
            "Good Resume but can be improved"
        )

    else:
        st.error(
            "Resume needs major improvements"
        )