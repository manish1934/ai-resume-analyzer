import streamlit as st
import PyPDF2
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import matplotlib.pyplot as plt

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text


# Streamlit UI
st.title("AI Resume Analyzer")

uploaded_resume = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
job_description = st.text_area("Paste Job Description Here")

if uploaded_resume and job_description:

    resume_text = extract_text_from_pdf(uploaded_resume)

    text = [resume_text, job_description]

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text)

    similarity_score = cosine_similarity(count_matrix)[0][1]
    match_percentage = round(similarity_score * 100, 2)

    st.subheader(f"Match Percentage: {match_percentage}%")

    # Create visualization
    data = pd.DataFrame({
        "Category": ["Match", "Gap"],
        "Value": [match_percentage, 100 - match_percentage]
    })

    fig, ax = plt.subplots()
    ax.bar(data["Category"], data["Value"])
    ax.set_ylabel("Percentage")
    ax.set_title("Resume vs Job Description Match")

    st.pyplot(fig)


