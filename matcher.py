def rank_candidates(job, candidates):
    ranked = []

    for c in candidates:
        score = 0
        total = 0

        # -------- SKILLS -------- #
        matched_skills = list(set(c["skills"]) & set(job["required_skills"]))
        missing_skills = list(set(job["required_skills"]) - set(c["skills"]))

        score += len(matched_skills) * 3
        total += len(job["required_skills"]) * 3

        # -------- PROJECT MATCH -------- #
        project_matches = 0

        for proj in c["projects"]:
            proj_lower = proj.lower()

            for expected in job["expected_projects"]:
                if any(word in proj_lower for word in expected.lower().split()):
                    project_matches += 1
                    break

        score += project_matches * 2
        total += len(job["expected_projects"]) * 2

        # -------- EXPERIENCE -------- #
        if c["experience_years"] >= job["experience_years"]:
            score += 2
        total += 2

        # -------- EDUCATION -------- #
        if c["education"] in job["preferred_education"]:
            score += 1
        total += 1

        # -------- CERTIFICATIONS -------- #
        cert_matches = list(
            set(c["certifications"]) & set(job["expected_certifications"])
        )

        score += len(cert_matches) * 2
        total += len(job["expected_certifications"]) * 2

        final_score = round((score / total) * 100)

        ranked.append({
            "name": c["name"],
            "id": c["candidate_id"],
            "score": final_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "cert_matches": cert_matches,
            "experience": c["experience_years"],
            "education": c["education"],
            "project_matches": project_matches,
            "projects": c["projects"]
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked