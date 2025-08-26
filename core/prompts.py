# core/prompts.py

def build_role_prompt(candidate: dict, num_questions: int = 5) -> str:
    role = candidate.get("role", "Unknown Role")
    skills = ", ".join(candidate.get("skills", [])) or "Not specified"
    years = candidate.get("years_exp", "N/A")
    positions = candidate.get("role", role)
    return (
        f"You are an expert interviewer. Based on the following candidate details, generate {num_questions} interview questions.\n"
        f"Candidate Role: {role}\n"
        f"Candidate Skills: {skills}\n"
        f"Years of Experience: {years}\n"
        f"Desired Position: {positions}\n"
        "Return questions as a numbered list. Focus on conceptual and practical aspects relevant to the role. "
        "Do not add commentary."
    )
