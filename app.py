import streamlit as st
import json
import os
from dotenv import load_dotenv
from euriai import EuriaiClient

from matcher import rank_candidates
from utils import (
    generate_explanation,
    growth_suggestions,
    explain_projects,
    rag_match_score
)
from rag import load_multiple_pdfs

# -------- LOAD ENV -------- #
load_dotenv()
api_key = os.getenv("EURI_API_KEY")

client = EuriaiClient(api_key=api_key)
client.model = "gpt-4o-mini"

st.set_page_config(page_title="HireMatch AI", page_icon="🤖")

st.title("💼 HireMatch AI")
st.caption("AI-powered Resume Screening System")

# -------- LOAD DATA -------- #
with open("data/job_descriptions.json") as f:
    jobs = json.load(f)

with open("data/resumes.json") as f:
    candidates = json.load(f)

# -------- SIDEBAR -------- #
with st.sidebar:
    st.header("⚙️ Settings")

    selected_role = st.selectbox(
        "Select Job Role",
        [job["role"] for job in jobs]
    )

    max_tokens = st.slider("LLM Tokens", 50, 300, 120)

    st.header("📄 Upload Resume(s)")
    uploaded_files = st.file_uploader(
        "Upload PDF Resume",
        type=["pdf"],
        accept_multiple_files=True
    )

# -------- LOAD RAG DB (ONCE) -------- #
if uploaded_files and "db" not in st.session_state:

    file_paths = []

    for i, file in enumerate(uploaded_files):
        path = f"uploads/temp_{i}.pdf"

        with open(path, "wb") as f:
            f.write(file.read())

        file_paths.append(path)

    with st.spinner("🔄 Processing resumes..."):
        st.session_state.db = load_multiple_pdfs(file_paths)

    st.sidebar.success(f"✅ Loaded {len(file_paths)} resumes!")

# -------- SELECT JOB -------- #
job = next(j for j in jobs if j["role"] == selected_role)

st.subheader(f"📌 {job['role']}")
st.write(f"**Skills Required:** {', '.join(job['required_skills'])}")
st.write(f"**Experience:** {job['experience_years']} years")
st.write(f"**Education:** {', '.join(job['preferred_education'])}")

# -------- RUN MATCHING -------- #
if st.button("🚀 Find Candidates"):

    with st.spinner("Matching candidates..."):
        results = rank_candidates(job, candidates)

    st.success("Ranking complete!")

    # -------- RAG MATCH -------- #
    if "db" in st.session_state:
        st.markdown("## 🤖 Uploaded Resume Match")

        rag_result = rag_match_score(
            client,
            st.session_state.db,
            job,
            max_tokens
        )

        st.info(rag_result)

    # -------- CANDIDATE LIST -------- #
    for r in results[:5]:

        st.markdown("---")
        st.subheader(f"👤 {r['name']} — {r['score']}%")

        st.write(f"✅ Matched Skills: {', '.join(r['matched_skills'])}")
        st.write(f"❌ Missing Skills: {', '.join(r['missing_skills'])}")
        st.write(f"📁 Project Matches: {r['project_matches']}")
        st.write(f"🎓 Education: {r['education']}")
        st.write(f"💼 Experience: {r['experience']} years")

        if r["cert_matches"]:
            st.write(f"📜 Certifications Match: {', '.join(r['cert_matches'])}")

        explanation = generate_explanation(client, job, r, max_tokens)
        st.info(f"🧠 {explanation}")

        project_expl = explain_projects(client, r, max_tokens)
        st.success(f"📁 {project_expl}")

        if r["score"] < 65:
            st.warning(
                f"📈 Improve by learning: {', '.join(growth_suggestions(r))}"
            )