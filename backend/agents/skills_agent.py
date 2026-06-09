def run_skills_agent(team_data: dict) -> dict:
    employees = team_data.get("employees", [])

    required_certifications = {
        "Cloud Engineer": ["AZ-900", "AZ-204"],
        "DevOps Engineer": ["AZ-900", "AZ-400"],
        "SRE": ["AZ-900", "AZ-104", "AZ-400"],
        "Data Engineer": ["DP-900", "DP-203"]
    }

    total_required = 0
    total_matched = 0
    gaps = []

    for employee in employees:
        role = employee.get("role")
        certs = employee.get("certifications", [])
        required = required_certifications.get(role, [])

        total_required += len(required)
        matched = len([cert for cert in required if cert in certs])
        total_matched += matched

        missing = [cert for cert in required if cert not in certs]

        if missing:
            gaps.append({
                "employee": employee.get("name"),
                "role": role,
                "missing_certifications": missing
            })

    coverage = round((total_matched / total_required) * 100, 2) if total_required else 0

    return {
        "agent": "Skills Agent",
        "summary": "Evaluates certification and competency coverage across the team.",
        "certification_coverage": coverage,
        "gaps": gaps
    }