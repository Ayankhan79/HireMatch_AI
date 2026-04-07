def generate_explanation(client, job, candidate, max_tokens=120):
    prompt = f"""
Candidate: {candidate['name']}
Matched Skills: {candidate['matched_skills']}
Missing Skills: {candidate['missing_skills']}
Experience: {candidate['experience']} years

Explain suitability for the job(Briefly explain the candidate’s suitability for the role, considering strengths and gaps. Keep it concise.)
"""

    try:
        res = client.generate_completion(
            prompt=prompt,
            max_tokens=max_tokens
        )
        return res['choices'][0]['message']['content']
    except:
        return "Explanation unavailable."


def explain_projects(client, candidate, max_tokens=120):
    prompt = f"""
Projects:
{candidate['projects']}

Explain what the candidate has built and skills shown.
(Briefly explain what the candidate has built and the key skills demonstrated. Keep it short and to the point.)
"""

    try:
        res = client.generate_completion(
            prompt=prompt,
            max_tokens=max_tokens
        )
        return res['choices'][0]['message']['content']
    except:
        return "Project explanation unavailable."


def rag_match_score(client, db, job, max_tokens=150):

    docs = db.max_marginal_relevance_search(
        job["role"],
        k=8,
        fetch_k=20
    )

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
Job Role: {job['role']}
Required Skills: {job['required_skills']}

Resume:
{context}

Give:
1. Match score (0-100)
2. Reason
"""

    try:
        res = client.generate_completion(
            prompt=prompt,
            max_tokens=max_tokens
        )
        return res['choices'][0]['message']['content']
    except:
        return "RAG failed."


def growth_suggestions(candidate):
    return candidate["missing_skills"]