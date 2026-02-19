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
# Global Skill Database (Scalable)
# Add more skills anytime
# ---------------------------
global_skills = [
    "python","java","c++","c","sql","mysql","mongodb",
    "machine learning","deep learning","data science",
    "pandas","numpy","tensorflow","keras","statistics",
    "excel","power bi","tableau","data visualization",
    "aws","azure","gcp","cloud computing",
    "docker","kubernetes","linux","git","github",
    "html","css","javascript","react","node","express",
    "flask","django","api","rest api",
    "cyber security","network security","penetration testing",
    "devops","jenkins","ci/cd",
    "problem solving","data structures","algorithms"
]

# ---------------------------
# Extract skills from text
# ---------------------------
def extract_skills(text):
    detected = []
    for skill in global_skills:
        if skill in text:
            detected.append(skill)
    return list(set(detected))

# ---------------------------
# UI
# ---------------------------
st.set_page_config(page_title="AI Resume Screening System", page_icon="🚀")
st.title("🚀 AI Resume Screening & Skill Gap Analysis (Dynamic Version)")

mode = st.selectbox("Select Mode", ["Student Mode", "HR Mode"])

job_description = st.text_area("Paste Job Description Here")

# =====================================================
# 🎓 STUDENT MODE
# =====================================================
if mode == "Student Mode":

    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if uploaded_resume and job_description:

        resume_text = extract_text_from_pdf(uploaded_resume)
        jd_text = job_description.lower()

        required_skills = extract_skills(jd_text)
        resume_skills = extract_skills(resume_text)

        matched_skills = list(set(required_skills) & set(resume_skills))
        missing_skills = list(set(required_skills) - set(resume_skills))

        if len(required_skills) > 0:
            score = round((len(matched_skills) / len(required_skills)) * 100, 2)
        else:
            score = 0

        st.subheader("📊 Match Score")
        st.metric("Match Percentage", f"{score}%")
        st.progress(score / 100 if score > 0 else 0)

        st.subheader("📌 Required Skills (From JD)")
        st.write(", ".join(required_skills) if required_skills else "No skills detected from JD.")

        st.subheader("✅ Skills Present in Resume")
        st.write(", ".join(matched_skills) if matched_skills else "No matching skills found.")

        st.subheader("❌ Missing Skills (Add These)")
        st.write(", ".join(missing_skills) if missing_skills else "Excellent! No major skills missing.")

        st.subheader("💡 Suggestions")
        if score < 50:
            st.write("- Add more relevant technical skills.")
            st.write("- Customize resume based on job description.")
        elif score < 75:
            st.write("- Add measurable achievements.")
            st.write("- Add certifications or projects.")
        else:
            st.write("- Your resume is well aligned with this job.")

# =====================================================
# 🏢 HR MODE
# =====================================================
elif mode == "HR Mode":

    uploaded_resumes = st.file_uploader(
        "Upload Multiple Resumes (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_resumes and job_description:

        jd_text = job_description.lower()
        required_skills = extract_skills(jd_text)

        results = []

        for resume in uploaded_resumes:
            resume_text = extract_text_from_pdf(resume)
            resume_skills = extract_skills(resume_text)

            matched_skills = list(set(required_skills) & set(resume_skills))

            if len(required_skills) > 0:
                score = round((len(matched_skills) / len(required_skills)) * 100, 2)
            else:
                score = 0

            results.append({
                "Candidate": resume.name,
                "Match %": score,
                "Matched Skills": ", ".join(matched_skills)
            })

        df = pd.DataFrame(results)
        df = df.sort_values(by="Match %", ascending=False)

        st.subheader("🏆 Candidate Ranking")
        st.dataframe(df)

        if not df.empty:
            st.success(f"Top Candidate: {df.iloc[0]['Candidate']} ({df.iloc[0]['Match %']}%)")

        # Graph
        st.subheader("📊 Comparison Chart")
        fig, ax = plt.subplots()
        ax.bar(df["Candidate"], df["Match %"])
        ax.set_ylabel("Match Percentage")
        st.pyplot(fig)

        # CSV Download
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Ranking CSV",
            data=csv,
            file_name="candidate_ranking.csv",
            mime="text/csv"
        )
