from dotenv import load_dotenv
load_dotenv()
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
import urllib.parse

# Gemini API config
genai.configure(api_key=os.getenv("google_api"))

# Function to get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Convert uploaded PDF to image bytes for Gemini
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": img_byte_arr
                }
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title='ATS RESUME SCANNER AND JOB FINDER')
st.header("ATS RESUME SCANNER AND JOB FINDER")

input_text = st.text_input("Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)")

if uploaded_file is not None:
    st.write("✅ PDF uploaded successfully!")

# Buttons for ATS evaluation
submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

# Evaluation prompt
input_prompt1 = """
You are experienced HR with Tech Experience in the field of DataScience, 
Full Stack, Web Development, Big Data Engineering, DevOps, Data Analyst.
Review the provided resume against the job description for these profiles.
Share your professional evaluation on whether the candidate's profile aligns 
with the job description and highlight the strengths and weaknesses of the applicant.
"""

# ATS percentage match prompt
input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding 
of Data Science, Web Development, Big Data Engineering, DevOps, Data Analyst roles.
Evaluate the resume against the provided job description.
Return the ATS match percentage first, followed by the list of missing keywords.
"""

# Job suggestions prompt template (will extract job title suggestions)
def job_suggestion_prompt(job_type):
    return f"""
You are a career placement expert with deep knowledge of the tech job market.
Based on the given resume and the selected job type: '{job_type}', suggest 
the top 5 specific job search keywords or job titles (not job descriptions) 
that the candidate should search for on LinkedIn.
Do not explain, just return the 5 job search phrases as a numbered list.
"""

# Button actions for ATS evaluation
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("Evaluation Response:")
        st.write(response)
    else:
        st.write("Please upload a resume PDF.")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("ATS Match Result:")
        st.write(response)
    else:
        st.write("Please upload a resume PDF.")

# Job type selection moved below ATS features
st.subheader("Get Top LinkedIn Job Suggestions based on Resume ")

# Dropdown for job type selection
job_type_option = st.selectbox("Select Job Type:", ["Internship", "Full Time"])

# Button to get job suggestions
submit4 = st.button("Get Top 5 LinkedIn Job Suggestions")

# Action for job suggestions
if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        job_prompt = job_suggestion_prompt(job_type_option)
        response = get_gemini_response(job_prompt, pdf_content, "")
        st.subheader(f"Top 5 LinkedIn Job Search Links ({job_type_option}):")

        # Process response into list of job search links
        job_titles = []
        for line in response.splitlines():
            if line.strip() and (line[0].isdigit() or line[0] == '-'):
                job_titles.append(line.split('.', 1)[-1].strip())
        
        if not job_titles:
            st.write("❌ Couldn’t extract job suggestions. Please retry.")
        else:
            for idx, title in enumerate(job_titles[:5], start=1):
                query = urllib.parse.quote_plus(f"{title} {job_type_option}")
                link = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=India"
                st.markdown(f"{idx}. [{title}]({link})")

    else:
        st.write("Please upload a resume PDF.")
