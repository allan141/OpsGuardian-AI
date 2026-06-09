def run_incident_agent(team_data: dict) -> dict:
    scenario = team_data.get("incident_scenario", "Azure service outage")
    employees = team_data.get("employees", [])

    roles = [employee.get("role") for employee in employees]
    certifications = []
    for employee in employees:
        certifications.extend(employee.get("certifications", []))

    strengths = []
    weaknesses = []

    if "SRE" in roles:
        strengths.append("SRE role present in the team.")
    else:
        weaknesses.append("No dedicated SRE role detected.")

    if "AZ-400" in certifications:
        strengths.append("DevOps certification coverage detected.")
    else:
        weaknesses.append("No AZ-400 coverage for DevOps incident response.")

    if "AZ-204" in certifications:
        strengths.append("Application development certification coverage detected.")
    else:
        weaknesses.append("Limited application troubleshooting certification coverage.")

    readiness = max(30, 100 - (len(weaknesses) * 20))

    return {
        "agent": "Incident Simulation Agent",
        "summary": "Simulates an operational incident and evaluates response preparedness.",
        "scenario": scenario,
        "incident_response_readiness": readiness,
        "strengths": strengths,
        "weaknesses": weaknesses
    }