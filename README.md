# 📄 ATS Resume Scanner & LinkedIn Job Finder

An AI-powered resume evaluation tool built with **Google Gemini 1.5 Flash** and **Streamlit**. Upload your resume PDF, paste a job description, and instantly get ATS match scores, skill gap analysis, and personalized LinkedIn job search links.

---

## 🚀 Features

- **Resume Evaluation** — HR-style professional review of your resume against a job description
- **ATS Percentage Match** — Scores your resume like a real Applicant Tracking System and lists missing keywords
- **LinkedIn Job Suggestions** — Generates top 5 targeted job search links (Internship or Full Time) based on your resume content
- **PDF Vision Parsing** — Uses Gemini Vision to read your resume directly from PDF without any text extraction errors

---

## 📁 Folder Structure

```
ats-resume-scanner/
│
├── app.py              # Main Streamlit application
├── .env                # API keys (Google Gemini)
└── requirement.txt     # Python dependencies
```

---

## 🧠 How It Works

```
[ Upload Resume PDF ]
        │
        ▼
[ pdf2image converts PDF → JPEG ]
        │
        ▼
[ Gemini 1.5 Flash Vision reads the image ]
        │
        ├──► "Tell Me About the Resume"
        │         └──► HR-style evaluation against job description
        │
        ├──► "Percentage Match"
        │         └──► ATS score + missing keywords list
        │
        └──► "Get Top 5 LinkedIn Job Suggestions"
                  └──► Extracts job titles → builds LinkedIn search URLs
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.9+
- Google Gemini API key — get one free at [aistudio.google.com](https://aistudio.google.com)
- `poppler` installed on your system (required by `pdf2image`)

### Install Poppler

**Windows:**
```bash
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
# Extract and add the bin/ folder to your system PATH
```

**macOS:**
```bash
brew install poppler
```

**Linux / Ubuntu:**
```bash
sudo apt-get install poppler-utils
```

### Install Python Dependencies

```bash
git clone <your-repo-url>
cd ats-resume-scanner

pip install -r requirement.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
google_api=AIza...your_gemini_api_key_here...
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## 🖥️ Usage

1. Paste the **Job Description** into the text input
2. Upload your **Resume as a PDF**
3. Choose an action:

| Button | What It Does |
|---|---|
| **Tell Me About the Resume** | Professional HR-style review — strengths, weaknesses, alignment with JD |
| **Percentage Match** | ATS score (e.g. 78%) + list of missing keywords to add to your resume |
| **Get Top 5 LinkedIn Job Suggestions** | Select Internship or Full Time → get 5 clickable LinkedIn job search links |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **AI Model** | Google Gemini 1.5 Flash (Vision) |
| **PDF Processing** | pdf2image + Pillow |
| **API Client** | google-generativeai |
| **Config** | python-dotenv |

---

## 📦 Dependencies

```
streamlit
google-generativeai
python-dotenv
pdf2image
```

Install with:
```bash
pip install -r requirement.txt
```
