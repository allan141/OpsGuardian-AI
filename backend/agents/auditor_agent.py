def run_auditor_agent(skills_result: dict, workload_result: dict, incident_result: dict, risk_result: dict) -> dict:
    concerns = []

    if skills_result.get("certification_coverage", 0) < 60:
        concerns.append("Certification coverage is below recommended operational readiness level.")

    if workload_result.get("workload_status") == "High":
        concerns.append("High workload may reduce the team's ability to respond to incidents.")

    if incident_result.get("incident_response_readiness", 0) < 70:
        concerns.append("Incident response readiness is below the safe threshold.")

    if not concerns:
        confidence = "High"
        validation = "The analysis is consistent and supported by available evidence."
    elif len(concerns) <= 2:
        confidence = "Medium"
        validation = "The analysis is mostly supported, but some operational risks require attention."
    else:
        confidence = "Low"
        validation = "The analysis identifies multiple critical gaps and should be reviewed by a human manager."

    return {
        "agent": "Auditor Agent",
        "summary": "Challenges assumptions, validates evidence, and improves reliability.",
        "confidence": confidence,
        "validation": validation,
        "concerns": concerns,
        "reviewed_risk_level": risk_result.get("risk_level")
    }