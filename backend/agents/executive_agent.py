def run_executive_agent(risk_result: dict, auditor_result: dict, skills_result: dict, workload_result: dict, incident_result: dict) -> dict:
    recommendations = []

    if skills_result.get("certification_coverage", 0) < 75:
        recommendations.append("Increase certification coverage for critical roles.")

    if workload_result.get("workload_status") == "High":
        recommendations.append("Reduce workload concentration before assigning additional incident response responsibilities.")

    if incident_result.get("incident_response_readiness", 0) < 75:
        recommendations.append("Run incident response drills and create escalation playbooks.")

    if risk_result.get("risk_level") == "High":
        recommendations.append("Prioritize operational readiness improvements within the next 30 days.")

    return {
        "agent": "Executive Insights Agent",
        "summary": "Transforms technical analysis into executive-level recommendations.",
        "operational_readiness_score": risk_result.get("operational_readiness_score"),
        "risk_level": risk_result.get("risk_level"),
        "auditor_confidence": auditor_result.get("confidence"),
        "executive_summary": (
            "OpsGuardian AI identified the current team readiness level, operational risks, "
            "and the most important actions required to improve resilience."
        ),
        "recommendations": recommendations
    }