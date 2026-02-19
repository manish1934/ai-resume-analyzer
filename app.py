import streamlit as st
import PyPDF2
import spacy
import re
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

st.title("🚀 AI Resume Analyzer - Advanced ATS System")

uploaded_files = st.file_uploader(
    "Upload Multiple Resumes (PDF)",
    type=["pdf"],
    accept_multiple_files=True
)

job_description = st.text_area("Paste Job Description")

# -------- FUNCTIONS --------

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(tokens)

def extract_skills(text):
    skills = [
        "python", "machine learning", "deep learning", "nlp",
        "tensorflow", "pandas", "numpy", "scikit-learn",
        "streamlit", "mongodb", "react", "node", "express",
        "aws", "docker", "sql", "power bi"
    ]
    return [skill for skill in skills if skill in text.lower()]

def detect_experience(text):
    if "year" in text.lower() or "experience" in text.lower():
        return 1
    return 0

def detect_education(text):
    if "b.tech" in text.lower() or "bca" in text.lower() or "bachelor" in text.lower():
        return 1
    return 0

def detect_achievements(text):
    if "%" in text or "improved" in text.lower() or "increased" in text.lower():
        return True
    return False

# -------- MAIN --------

if st.button("Analyze Resumes"):

    if uploaded_files and job_description:

        results = []
        cleaned_jd = clean_text(job_description)
        jd_skills = extract_skills(job_description)

        for file in uploaded_files:

            resume_text = extract_text_from_pdf(file)
            cleaned_resume = clean_text(resume_text)

            # Similarity Score (Skills based)
            vectorizer = TfidfVectorizer()
            vectors = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            skill_score = similarity * 100

            # Experience Score
            exp_score = 30 if detect_experience(resume_text) else 0

            # Education Score
            edu_score = 20 if detect_education(resume_text) else 0

            # Weighted Final Score
            final_score = round((skill_score * 0.5) + exp_score + edu_score, 2)

            resume_skills = extract_skills(resume_text)
            matched_skills = list(set(resume_skills) & set(jd_skills))
            missing_skills = list(set(jd_skills) - set(resume_skills))

            achievements_present = detect_achievements(resume_text)

            results.append({
                "Name": file.name,
                "Final Score": final_score,
                "Matched Skills": matched_skills,
                "Missing Skills": missing_skills,
                "Achievements": achievements_present
            })

        # Sort by Final Score
        results = sorted(results, key=lambda x: x["Final Score"], reverse=True)

        st.subheader("🏆 Resume Ranking")
        df = pd.DataFrame(results)
        st.dataframe(df[["Name", "Final Score"]])

        # -------- Bar Chart --------
        st.subheader("📊 Candidate Comparison Chart")
        fig, ax = plt.subplots()
        ax.bar(df["Name"], df["Final Score"])
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # -------- Detailed Analysis --------
        st.subheader("📄 Detailed Analysis")

        for candidate in results:

            st.markdown("---")
            st.subheader(candidate["Name"])
            st.write("Final Score:", candidate["Final Score"], "%")
            st.progress(int(candidate["Final Score"]))

            # Suggestion
            if candidate["Final Score"] < 40:
                st.warning("Needs significant improvement.")
            elif candidate["Final Score"] < 70:
                st.info("Good but can improve.")
            else:
                st.success("Excellent candidate!")

            # Achievement suggestion
            if not candidate["Achievements"]:
                st.warning("Add measurable achievements (e.g., improved accuracy by 15%).")

            st.write("✅ Matched Skills:")
            for skill in candidate["Matched Skills"]:
                st.success(skill)

            st.write("❌ Missing Skills:")
            for skill in candidate["Missing Skills"]:
                st.error(skill)

    else:
        st.warning("Please upload resumes and paste job description.")
