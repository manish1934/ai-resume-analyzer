import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Extract text from PDF
# ---------------------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------------------
# Master IT Skills List
# ---------------------------
master_skills = [
    "python", "java", "c++", "c#", "javascript", "html", "css",
    "react", "angular", "node", "django", "flask",
    "sql", "mongodb", "mysql", "postgresql",
    "machine learning", "deep learning", "ai",
    "data analysis", "pandas", "numpy",
    "aws", "azure", "gcp",
    "docker", "kubernetes",
    "linux", "git", "github",
    "api", "rest api",
    "data structures", "algorithms",
    "cyber security", "network security",
    "testing", "selenium",
    "android", "kotlin", "swift",
    "blockchain"
]

# ---------------------------
# Dynamic Skill Filter Based on Job Role
# ---------------------------
def get_required_skills(job_title):
    job_title = job_title.lower()

    required = []

    for skill in master_skills:
        if skill in job_title:
            required.append(skill)

    # If no direct match found, return general IT core skills
    if not required:
        required = [
            "python", "sql", "git",
            "data structures", "algorithms"
        ]

    return required

# ---------------------------
# UI Setup
# ---------------------------
st.set_page_config(page_title="AI Resume Screening System", page_icon="🚀")
st.title("🚀 AI Resume Skill Analyzer (Dynamic IT Mode)")

mode = st.selectbox("Select Mode", ["Student Mode", "HR Mode"])
job_title = st.text_input("Enter Any IT Job Role (Example: Cloud Engineer, AI Developer)")

required_skills = get_required_skills(job_title)

# ====================================================
# 🎓 STUDENT MODE
# ====================================================
if mode == "Student Mode":

    uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if job_title and uploaded_resume:

        resume_text = extract_text_from_pdf(uploaded_resume)

        matched_skills = [skill for skill in required_skills if skill in resume_text]
        missing_skills = [skill for skill in required_skills if skill not in resume_text]

        score = round((len(matched_skills) / len(required_skills)) * 100, 2)

        st.subheader("📌 Required Skills (Auto Generated)")
        st.write(", ".join(required_skills))

        st.subheader("📊 Match Score")
        st.metric("Skill Match %", f"{score}%")
        st.progress(score / 100)

        st.subheader("✅ Skills Found")
        st.write(", ".join(matched_skills) if matched_skills else "No matching skills found.")

        st.subheader("❌ Missing Skills")
        st.write(", ".join(missing_skills) if missing_skills else "No major skills missing.")

# ====================================================
# 🏢 HR MODE
# ====================================================
elif mode == "HR Mode":

    uploaded_resumes = st.file_uploader(
        "Upload Multiple Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if job_title and uploaded_resumes:

        results = []

        for resume in uploaded_resumes:
            resume_text = extract_text_from_pdf(resume)

            matched_skills = [skill for skill in required_skills if skill in resume_text]
            score = round((len(matched_skills) / len(required_skills)) * 100, 2)

            results.append({
                "Candidate": resume.name,
                "Match %": score
            })

        df = pd.DataFrame(results)
        df = df.sort_values(by="Match %", ascending=False).reset_index(drop=True)

        st.subheader("🏆 Candidate Ranking")
        st.dataframe(df)

        # Graph
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(df["Candidate"][::-1], df["Match %"][::-1])
        ax.set_xlabel("Match Percentage")
        plt.tight_layout()
        st.pyplot(fig)

        # CSV Download
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="📥 Download Ranking CSV",
            data=csv,
            file_name="candidate_ranking.csv",
            mime="text/csv"
        )
