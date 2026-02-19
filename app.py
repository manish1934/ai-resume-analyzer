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
# Job Title Based Skill Database
# ---------------------------
job_skill_database = {
    "software engineer": [
        "python", "java", "c++", "data structures",
        "algorithms", "sql", "git", "api",
        "oop", "problem solving"
    ],
    "data analyst": [
        "excel", "sql", "python",
        "power bi", "tableau",
        "statistics", "data visualization"
    ],
    "data scientist": [
        "python", "machine learning",
        "deep learning", "pandas",
        "numpy", "statistics"
    ],
    "frontend developer": [
        "html", "css", "javascript",
        "react", "bootstrap"
    ],
    "backend developer": [
        "python", "django", "flask",
        "node", "sql", "api", "mongodb"
    ]
}

# ---------------------------
# UI
# ---------------------------
st.set_page_config(page_title="AI Resume Screening System", page_icon="🚀")
st.title("🚀 AI Resume Skill Analyzer")

mode = st.selectbox("Select Mode", ["Student Mode", "HR Mode"])

job_title = st.text_input("Enter Job Title").lower()

# ====================================================
# 🎓 STUDENT MODE
# ====================================================
if mode == "Student Mode":

    uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if job_title and uploaded_resume:

        if job_title in job_skill_database:

            resume_text = extract_text_from_pdf(uploaded_resume)
            required_skills = job_skill_database[job_title]

            matched_skills = [skill for skill in required_skills if skill in resume_text]
            missing_skills = [skill for skill in required_skills if skill not in resume_text]

            score = round((len(matched_skills) / len(required_skills)) * 100, 2)

            st.subheader("📊 Match Score")
            st.metric("Skill Match %", f"{score}%")
            st.progress(score / 100)

            st.subheader("📌 Required Skills")
            st.write(", ".join(required_skills))

            st.subheader("✅ Skills Found")
            st.write(", ".join(matched_skills) if matched_skills else "No matching skills found.")

            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing_skills) if missing_skills else "No major skills missing.")

        else:
            st.warning("Job title not found in database.")

# ====================================================
# 🏢 HR MODE
# ====================================================
elif mode == "HR Mode":

    uploaded_resumes = st.file_uploader(
        "Upload Multiple Resumes",
        type=["pdf"],
        accept_multiple_files=True
    )

    if job_title and uploaded_resumes:

        if job_title in job_skill_database:

            required_skills = job_skill_database[job_title]
            results = []

            for resume in uploaded_resumes:
                resume_text = extract_text_from_pdf(resume)

                matched_skills = [skill for skill in required_skills if skill in resume_text]
                score = round((len(matched_skills) / len(required_skills)) * 100, 2)

                results.append({
                    "Candidate": resume.name,
                    "Match %": score,
                    "Matched Skills Count": len(matched_skills)
                })

            df = pd.DataFrame(results)

            # Smart Sorting
            df = df.sort_values(
                by=["Match %", "Matched Skills Count"],
                ascending=False
            ).reset_index(drop=True)

            st.subheader("🏆 Candidate Ranking")
            st.dataframe(df)

            if not df.empty:
                st.success(f"Top Candidate: {df.iloc[0]['Candidate']} ({df.iloc[0]['Match %']}%)")

            # Horizontal Graph
            st.subheader("📊 Candidate Comparison")

            fig, ax = plt.subplots(figsize=(10, 6))

            ax.barh(df["Candidate"][::-1], df["Match %"][::-1])
            ax.set_xlabel("Match Percentage")
            ax.set_ylabel("Candidates")
            ax.set_title("Candidate Match Comparison")

            plt.tight_layout()
            st.pyplot(fig)

        else:
            st.warning("Job title not found in database.")
