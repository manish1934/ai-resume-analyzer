import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import matplotlib.pyplot as plt

# --------- Function to extract text from PDF ----------
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()


# --------- Predefined Skills List ----------
skills_list = [
    "python", "java", "c++", "sql", "machine learning",
    "data analysis", "excel", "aws", "docker",
    "power bi", "tableau", "html", "css",
    "javascript", "react", "node"
]


# --------- Streamlit UI ----------
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")

st.title("📄 AI Resume Analyzer Pro")

uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description Here")

if uploaded_resume and job_description:

    resume_text = extract_text_from_pdf(uploaded_resume)
    job_description = job_description.lower()

    # -------- Similarity Score --------
    text = [resume_text, job_description]

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)

    similarity_score = cosine_similarity(count_matrix)[0][1]
    match_percentage = round(similarity_score * 100, 2)

    st.subheader("📊 Match Score")
    st.metric(label="Resume Match Percentage", value=f"{match_percentage}%")
    st.progress(similarity_score)

    # -------- Skill Matching --------
    resume_skills = [skill for skill in skills_list if skill in resume_text]
    job_skills = [skill for skill in skills_list if skill in job_description]

    matched_skills = list(set(resume_skills) & set(job_skills))
    missing_skills = list(set(job_skills) - set(resume_skills))

    st.subheader("✅ Matched Skills")
    if matched_skills:
        st.write(", ".join(matched_skills))
    else:
        st.write("No matched skills found.")

    st.subheader("❌ Missing Skills (You Should Add)")
    if missing_skills:
        st.write(", ".join(missing_skills))
    else:
        st.write("Great! No major skills missing.")

    # -------- Suggestions --------
    st.subheader("💡 Suggestions to Improve Resume")

    if match_percentage < 50:
        st.write("- Add more relevant technical skills.")
        st.write("- Customize resume according to job description.")
    elif match_percentage < 75:
        st.write("- Add measurable achievements (e.g., Increased sales by 30%).")
        st.write("- Include certifications or projects.")
    else:
        st.write("- Your resume is well optimized!")
        st.write("- Just improve formatting for better ATS compatibility.")

    # -------- Visualization --------
    data = pd.DataFrame({
        "Category": ["Match", "Gap"],
        "Value": [match_percentage, 100 - match_percentage]
    })

    fig, ax = plt.subplots()
    ax.bar(data["Category"], data["Value"])
    ax.set_ylabel("Percentage")
    ax.set_title("Resume vs Job Description Match")
    st.pyplot(fig)


