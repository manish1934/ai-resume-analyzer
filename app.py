import streamlit as st
import PyPDF2

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
# (You can add more roles anytime)
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
        "react", "bootstrap", "responsive design"
    ],
    "backend developer": [
        "python", "django", "flask",
        "node", "sql", "api", "mongodb"
    ],
    "devops engineer": [
        "aws", "docker", "kubernetes",
        "linux", "ci/cd", "jenkins"
    ],
    "cyber security analyst": [
        "network security", "linux",
        "penetration testing", "firewall",
        "cyber security"
    ]
}

# ---------------------------
# UI Setup
# ---------------------------
st.set_page_config(page_title="Smart Resume Skill Analyzer", page_icon="🚀")
st.title("🚀 Smart Resume Skill Analyzer")

job_title = st.text_input("Enter Job Title (e.g., Software Engineer)").lower()
uploaded_resume = st.file_uploader("Upload Your Resume (PDF)", type=["pdf"])

# ---------------------------
# MAIN LOGIC
# ---------------------------
if job_title and uploaded_resume:

    resume_text = extract_text_from_pdf(uploaded_resume)

    if job_title in job_skill_database:

        required_skills = job_skill_database[job_title]

        matched_skills = [skill for skill in required_skills if skill in resume_text]
        missing_skills = [skill for skill in required_skills if skill not in resume_text]

        match_score = round((len(matched_skills) / len(required_skills)) * 100, 2)

        st.subheader("📊 Overall Match Score")
        st.metric("Skill Match Percentage", f"{match_score}%")
        st.progress(match_score / 100)

        st.subheader("📌 Required Skills for This Job")
        st.write(", ".join(required_skills))

        st.subheader("✅ Skills Found in Your Resume")
        st.write(", ".join(matched_skills) if matched_skills else "No required skills found.")

        st.subheader("❌ Skills Missing (You Should Add These)")
        st.write(", ".join(missing_skills) if missing_skills else "Great! No major skills missing.")

        st.subheader("💡 Suggestions")
        if match_score < 50:
            st.write("- Add more relevant technical skills.")
            st.write("- Work on projects related to this job role.")
            st.write("- Customize your resume based on this role.")
        elif match_score < 75:
            st.write("- Add measurable achievements.")
            st.write("- Add internships or certifications.")
        else:
            st.write("- Your resume is well aligned for this role.")
            st.write("- Improve formatting for better ATS compatibility.")

    else:
        st.warning("Job title not found in database. Try common roles like Software Engineer, Data Analyst, Data Scientist, etc.")
