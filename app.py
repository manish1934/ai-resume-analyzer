import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt

# -------- Extract text from PDF --------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

# -------- Expanded Skill Database --------
role_skills = {
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
    ]
}

# -------- General Skill List for Auto Extraction --------
general_skills = list(set(sum(role_skills.values(), [])))

# -------- App UI --------
st.set_page_config(page_title="AI Resume Screening System", page_icon="🚀")
st.title("🚀 AI Resume Screening & Skill Gap Analysis")

mode = st.selectbox("Select Mode", ["Student Mode", "HR Mode"])
job_role = st.text_input("Enter Job Role").lower()

# ====================================================
# 🎓 STUDENT MODE
# ====================================================
if mode == "Student Mode":

    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_resume and job_role:

        resume_text = extract_text_from_pdf(uploaded_resume)

        # Auto Skill Extraction
        extracted_skills = [skill for skill in general_skills if skill in resume_text]

        st.subheader("🔍 Detected Skills in Resume")
        st.write(", ".join(extracted_skills) if extracted_skills else "No known skills detected.")

        if job_role in role_skills:

            required_skills = role_skills[job_role]

            matched_skills = [skill for skill in required_skills if skill in resume_text]
            missing_skills = [skill for skill in required_skills if skill not in resume_text]

            score = round((len(matched_skills) / len(required_skills)) * 100, 2)

            st.subheader("📊 Match Score")
            st.metric("Skill Match Percentage", f"{score}%")
            st.progress(score / 100)

            st.subheader("❌ Skills You Should Add")
            st.write(", ".join(missing_skills) if missing_skills else "Excellent! No major skills missing.")

            # AI Style Suggestion
            st.subheader("💡 Resume Improvement Suggestions")

            if score < 50:
                st.write("- Add more technical skills relevant to this role.")
                st.write("- Add internship or project experience.")
            elif score < 75:
                st.write("- Add measurable achievements (e.g., Improved system performance by 30%).")
                st.write("- Mention certifications.")
            else:
                st.write("- Your resume is strong. Improve formatting for ATS optimization.")

        else:
            st.warning("Role not found in database.")

# ====================================================
# 🏢 HR MODE
# ====================================================
elif mode == "HR Mode":

    uploaded_resumes = st.file_uploader(
        "Upload Multiple Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_resumes and job_role:

        if job_role in role_skills:

            required_skills = role_skills[job_role]
            results = []

            for resume in uploaded_resumes:
                resume_text = extract_text_from_pdf(resume)

                matched_skills = [skill for skill in required_skills if skill in resume_text]
                missing_skills = [skill for skill in required_skills if skill not in resume_text]

                score = round((len(matched_skills) / len(required_skills)) * 100, 2)

                results.append({
                    "Candidate": resume.name,
                    "Match %": score,
                    "Missing Skills": ", ".join(missing_skills)
                })

            df = pd.DataFrame(results)
            df = df.sort_values(by="Match %", ascending=False)

            st.subheader("🏆 Candidate Ranking")
            st.dataframe(df)

            st.success(f"Top Candidate: {df.iloc[0]['Candidate']} ({df.iloc[0]['Match %']}%)")

            # Graph Dashboard
            st.subheader("📊 Score Visualization")

            fig, ax = plt.subplots()
            ax.bar(df["Candidate"], df["Match %"])
            ax.set_ylabel("Match Percentage")
            ax.set_title("Candidate Comparison")
            st.pyplot(fig)

            # CSV Download
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Shortlist as CSV",
                data=csv,
                file_name="candidate_ranking.csv",
                mime="text/csv"
            )

        else:
            st.warning("Role not found in database.")
