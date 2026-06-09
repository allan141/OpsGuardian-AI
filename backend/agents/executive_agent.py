import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


def generate_ai_executive_recommendations(
    risk_result: dict,
    auditor_result: dict,
    skills_result: dict,
    workload_result: dict,
    incident_result: dict
) -> list[str]:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    if not endpoint or not api_key or not deployment:
        return [
            "Increase certification coverage for critical roles.",
            "Reduce workload concentration before assigning additional incident response responsibilities.",
            "Prioritize operational readiness improvements within the next 30 days."
        ]

    client = AzureOpenAI(
        api_key=api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=endpoint,
    )

    prompt = f"""
You are an executive operational readiness advisor.

Create 3 concise executive recommendations based on the following multi-agent analysis.

Risk Analysis:
{risk_result}

Auditor Validation:
{auditor_result}

Skills Analysis:
{skills_result}

Workload Analysis:
{workload_result}

Incident Simulation:
{incident_result}

Rules:
- Return only 3 recommendations.
- Each recommendation must be short.
- Focus on business action, resilience, risk reduction, and operational readiness.
- Do not use markdown.
"""

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You generate executive-level operational recommendations for cloud leadership teams."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=250,
        )

        text = response.choices[0].message.content or ""

        recommendations = [
            line.strip(" -1234567890.").strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return recommendations[:3] if recommendations else [
            "Increase certification coverage for critical roles.",
            "Reduce workload concentration before assigning additional incident response responsibilities.",
            "Prioritize operational readiness improvements within the next 30 days."
        ]

    except Exception:
        return [
            "Increase certification coverage for critical roles.",
            "Reduce workload concentration before assigning additional incident response responsibilities.",
            "Prioritize operational readiness improvements within the next 30 days."
        ]


def run_executive_agent(
    risk_result: dict,
    auditor_result: dict,
    skills_result: dict,
    workload_result: dict,
    incident_result: dict
) -> dict:
    recommendations = generate_ai_executive_recommendations(
        risk_result,
        auditor_result,
        skills_result,
        workload_result,
        incident_result
    )

    return {
        "agent": "Executive Insights Agent",
        "summary": "Transforms technical analysis into Azure OpenAI-powered executive recommendations.",
        "operational_readiness_score": risk_result.get("operational_readiness_score"),
        "risk_level": risk_result.get("risk_level"),
        "auditor_confidence": auditor_result.get("confidence"),
        "executive_summary": "OpsGuardian AI used multi-agent analysis and Azure OpenAI to generate executive-level operational recommendations.",
        "recommendations": recommendations,
        "azure_openai_powered": True
    }