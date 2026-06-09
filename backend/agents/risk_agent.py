def run_risk_agent(skills_result: dict, workload_result: dict, incident_result: dict) -> dict:
    skills_score = skills_result.get("certification_coverage", 0)
    incident_score = incident_result.get("incident_response_readiness", 0)

    workload_status = workload_result.get("workload_status", "Moderate")

    workload_penalty = {
        "Healthy": 0,
        "Moderate": 10,
        "High": 25
    }.get(workload_status, 10)

    readiness_score = round(((skills_score + incident_score) / 2) - workload_penalty, 2)
    readiness_score = max(0, min(100, readiness_score))

    if readiness_score >= 80:
        risk_level = "Low"
    elif readiness_score >= 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "agent": "Risk Assessment Agent",
        "summary": "Combines skills, workload, and incident simulation results into an operational risk score.",
        "operational_readiness_score": readiness_score,
        "risk_level": risk_level,
        "reasoning": {
            "skills_score": skills_score,
            "incident_score": incident_score,
            "workload_penalty": workload_penalty
        }
    }