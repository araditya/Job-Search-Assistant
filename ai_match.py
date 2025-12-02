def match_resume_to_job(resume_text, job):
    req_skills = [w.strip() for w in " ".join(job.get("requirements", [])).split() if w.isalpha()]
    score = sum(skill.lower() in resume_text.lower() for skill in req_skills)
    if score >= len(req_skills):
        match = "Very Strong"
    elif score >= max(len(req_skills) // 2, 1):
        match = "Medium"
    elif score > 0:
        match = "Low"
    else:
        match = "Low"
    cover_letter = f"Dear {job.get('company','Hiring Manager')}, my experience in {', '.join(req_skills)} makes me a great fit."
    return match, cover_letter
