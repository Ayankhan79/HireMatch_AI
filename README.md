# 💼 HireMatch AI

An AI-powered Resume Screening System that ranks candidates based on skills, projects, experience, education, and certifications. The application also leverages a Large Language Model (LLM) to generate hiring insights and uses Retrieval-Augmented Generation (RAG) to analyze uploaded resumes against job descriptions.

## 🚀 Features
- Multi-factor candidate ranking
- AI-generated candidate suitability explanations
- Project-based resume evaluation
- Resume upload and RAG-powered analysis
- Personalized skill improvement suggestions
- Interactive Streamlit dashboard

## 🛠️ Tech Stack
- Python
- Streamlit
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Euriai GPT-4o-mini
- JSON

## 📂 Project Structure
```
HireMatch-AI/
│── app.py
│── matcher.py
│── rag.py
│── utils.py
│── data/
│   ├── job_descriptions.json
│   └── resumes.json
```

## ▶️ Run the Project
```bash
streamlit run app.py
```

## 📌 Future Enhancements
- ATS resume parsing
- Semantic skill matching
- Recruiter analytics dashboard
- Interview question generation
- Resume scoring using custom embeddings

---
**Built with Python, Streamlit, LLMs, and RAG to simulate a real-world AI-powered hiring system.**
