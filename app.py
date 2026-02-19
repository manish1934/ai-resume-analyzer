import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# Extract Text From PDF
# ---------------------------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# ---------------------------
# Role Based Skill Database
# ---------------------------
role_based_skills = {
    "ai engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "numpy"
    ],
    "ml engineer": [
        "python", "machine learning", "scikit-learn",
        "pandas", "numpy", "model"
    ],
    "data scientist": [
        "python", "machine learning", "statistics",
        "pandas", "numpy", "sql"
    ],
    "cloud engineer": [
        "aws", "azure", "gcp",
        "docker", "kubernetes", "linux"
    ],
    "devops engineer": [
        "docker", "kubernetes", "linux",
        "ci/cd", "jenkins", "aws"
    ],
    "frontend developer": [
        "html", "css", "javascript",
        "react", "bootstrap"
    ],
    "backend developer": [
        "python", "django", "flask",
        "node", "sql", "api"
    ],
    "software engineer": [
        "python", "java", "c++",
        "data structures", "algorithms", "git"
    ]
}

# ---------------------------
# Smart Role Matching
# ---------------------------
def get_required_skills(job_title):
    job_title = job_title.lower().strip()

    for role in role_based_skills:
        if role in job_title:
            return role, role_based_skills[role]

    return None, None

# ---------------------------
# UI Setup
# ---------------------------
st.set_page_config(page_title="AI Resume Screening System", page_icon="🚀")
st.title("🚀 AI Resume Skill Analyzer")

mode = st.selectbox("Select Mode", ["Student Mode", "HR Mode"])
job_title = st.text_input("Enter IT Job Role (Example: AI Engineer, Backend Developer)")

matched_role, required_skills = get_required_skills(job_title)

# ====================================================
# 🎓 STUDENT MODE
# ====================================================
if mode == "Student Mode":

    uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

    if job_title and uploaded_resume:

        if matched_role:

            resume_text = extract_text_from_pdf(uploaded_resume)

            matched_skills = [
                skill for skill in required_skills
                if skill in resume_text
            ]

            missing_skills = [
                skill for skill in required_skills
                if skill not in resume_text
            ]

            score = round(
                (len(matched_skills) / len(required_skills)) * 100, 2
            )

            st.subheader(f"📌 Matched Role: {matched_role.title()}")

            st.subheader("📊 Match Score")
            st.metric("Skill Match %", f"{score}%")
            st.progress(score / 100)

            st.subheader("✅ Skills Found")
            st.write(", ".join(matched_skills) if matched_skills else "No matching skills found.")

            st.subheader("❌ Missing Skills")
            st.write(", ".join(missing_skills) if missing_skills else "No major skills missing.")

        else:
            st.error("Role not found in system database.")

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

        if matched_role:

            results = []

            for resume in uploaded_resumes:
                resume_text = extract_text_from_pdf(resume)

                matched_skills = [
                    skill for skill in required_skills
                    if skill in resume_text
                ]

                score = round(
                    (len(matched_skills) / len(required_skills)) * 100, 2
                )

                results.append({
                    "Candidate": resume.name,
                    "Match %": score,
                    "Matched Skills Count": len(matched_skills)
                })

            df = pd.DataFrame(results)

            df = df.sort_values(
                by=["Match %", "Matched Skills Count"],
                ascending=False
            ).reset_index(drop=True)

            st.subheader(f"🏆 Ranking for: {matched_role.title()}")
            st.dataframe(df)

            if not df.empty:
                st.success(
                    f"Top Candidate: {df.iloc[0]['Candidate']} "
                    f"({df.iloc[0]['Match %']}%)"
                )

            # Horizontal Graph
            st.subheader("📊 Candidate Comparison")

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(df["Candidate"][::-1], df["Match %"][::-1])
            ax.set_xlabel("Match Percentage")
            ax.set_ylabel("Candidates")
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

        else:
            st.error("Role not found in system database.")


