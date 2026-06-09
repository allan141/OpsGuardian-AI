from agents.skills_agent import run_skills_agent
from agents.workload_agent import run_workload_agent
from agents.incident_agent import run_incident_agent
from agents.risk_agent import run_risk_agent
from agents.auditor_agent import run_auditor_agent
from agents.executive_agent import run_executive_agent
from services.knowledge_base import load_knowledge_base


def run_full_analysis(team_data: dict) -> dict:
    knowledge_base = load_knowledge_base()

    skills_result = run_skills_agent(team_data)
    workload_result = run_workload_agent(team_data)
    incident_result = run_incident_agent(team_data)

    risk_result = run_risk_agent(
        skills_result,
        workload_result,
        incident_result
    )

    auditor_result = run_auditor_agent(
        skills_result,
        workload_result,
        incident_result,
        risk_result
    )

    executive_result = run_executive_agent(
        risk_result,
        auditor_result,
        skills_result,
        workload_result,
        incident_result
    )

    return {
        "project": "OpsGuardian AI",
        "team": team_data.get("team_name", "Unnamed Team"),
        "knowledge_base": {
            "summary": knowledge_base["summary"],
            "sources": knowledge_base["sources"]
        },
        "workflow": [
            skills_result,
            workload_result,
            incident_result,
            risk_result,
            auditor_result,
            executive_result
        ],
        "final_report": executive_result
    }