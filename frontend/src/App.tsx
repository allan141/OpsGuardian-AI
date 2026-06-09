import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

type Employee = {
  name: string;
  role: string;
  certifications: string[];
  workload_hours: number;
};

type AgentResult = {
  agent: string;
  summary: string;
  [key: string]: any;
};

type AnalysisResponse = {
  project: string;
  team: string;
  knowledge_base?: {
    summary: string;
    sources: string[];
  };
  workflow: AgentResult[];
  final_report: {
    operational_readiness_score: number;
    risk_level: string;
    auditor_confidence: string;
    executive_summary: string;
    recommendations: string[];
    
  };
};

const demoPayload = {
  team_name: "Cloud Operations Team",
  incident_scenario: "Azure service outage affecting production APIs",
  employees: [
    {
      name: "Ana",
      role: "Cloud Engineer",
      certifications: ["AZ-900", "AZ-204"],
      workload_hours: 38,
    },
    {
      name: "Pedro",
      role: "DevOps Engineer",
      certifications: ["AZ-900"],
      workload_hours: 46,
    },
    {
      name: "Maria",
      role: "SRE",
      certifications: [],
      workload_hours: 44,
    },
  ],
};

function cleanList(items: any[]): string[] {
  return items
    .map((item) => String(item ?? "").trim())
    .filter((item) => item.length > 0);
}

function getAgentHighlight(agent: AgentResult) {
  if (agent.certification_coverage !== undefined) {
    return `${agent.certification_coverage}% certification coverage`;
  }

  if (agent.workload_status) {
    return `${agent.workload_status} workload pressure`;
  }

  if (agent.incident_response_readiness !== undefined) {
    return `${agent.incident_response_readiness}% incident response readiness`;
  }

  if (agent.operational_readiness_score !== undefined) {
    return `${agent.operational_readiness_score}% readiness / ${agent.risk_level} risk`;
  }

  if (agent.confidence) {
    return `${agent.confidence} confidence validation`;
  }

  if (agent.recommendations) {
    return `${agent.recommendations.length} executive recommendations`;
  }

  return "Analysis completed";
}

function getAgentDetails(agent: AgentResult): string[] {
  if (agent.gaps && agent.gaps.length > 0) {
    return cleanList(
      agent.gaps.map((gap: any) => {
        const employee = gap.employee;
        const missing = gap.missing_certifications || [];

        if (!employee || missing.length === 0) return "";

        return `${employee}: missing ${missing.join(", ")}`;
      })
    );
  }

  if (agent.overloaded_members && agent.overloaded_members.length > 0) {
    return cleanList(
      agent.overloaded_members.map((member: any) => {
        if (!member.employee || member.workload_hours === undefined) return "";
        return `${member.employee}: ${member.workload_hours}h/week`;
      })
    );
  }

  if (agent.weaknesses && agent.weaknesses.length > 0) {
    return cleanList(agent.weaknesses);
  }

  if (agent.reasoning) {
    return cleanList([
      `Skills score: ${agent.reasoning.skills_score}`,
      `Incident score: ${agent.reasoning.incident_score}`,
      `Workload penalty: ${agent.reasoning.workload_penalty}`,
    ]);
  }

  if (agent.concerns && agent.concerns.length > 0) {
    return cleanList(agent.concerns);
  }

  if (agent.recommendations && agent.recommendations.length > 0) {
    return cleanList(agent.recommendations);
  }

  return [];
}

function App() {
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [visibleAgents, setVisibleAgents] = useState(0);
  const [employees, setEmployees] = useState<Employee[]>(demoPayload.employees);

  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [certifications, setCertifications] = useState("");
  const [workload, setWorkload] = useState("");

  function addEmployee() {
    if (!name || !role || !workload) return;

    setEmployees([
      ...employees,
      {
        name,
        role,
        certifications: certifications
          .split(",")
          .map((certification) => certification.trim())
          .filter(Boolean),
        workload_hours: Number(workload),
      },
    ]);

    setName("");
    setRole("");
    setCertifications("");
    setWorkload("");
    setResult(null);
    setVisibleAgents(0);
  }

  function resetTeam() {
    setEmployees(demoPayload.employees);
    setResult(null);
    setVisibleAgents(0);
  }

  async function runAnalysis() {
    setResult(null);
    setVisibleAgents(0);
    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/analysis/run",
        {
          ...demoPayload,
          employees,
        }
      );

      setResult(response.data);
    } catch (error) {
      alert("Erro ao conectar com o backend. Verifique se o FastAPI está rodando.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (!result) return;

    setVisibleAgents(0);

    let current = 0;

    const timer = setInterval(() => {
      current++;
      setVisibleAgents(current);

      if (current >= result.workflow.length) {
        clearInterval(timer);
      }
    }, 800);

    return () => clearInterval(timer);
  }, [result]);

  const score = result?.final_report?.operational_readiness_score ?? 0;
  const risk = result?.final_report?.risk_level ?? "Unknown";
  const circumference = 2 * Math.PI * 90;
  const progress = circumference - (score / 100) * circumference;

  return (
    <main className="page">
      <section className="hero">
        <div>
          <p className="eyebrow">Reasoning Agents Challenge</p>
          <h1>OpsGuardian AI</h1>
          <p className="subtitle">
            A multi-agent command center that evaluates workforce readiness,
            simulates incidents, validates risks, and generates executive
            actions before failures happen.
          </p>
        </div>

        <button
          type="button"
          onClick={runAnalysis}
          disabled={loading}
          className="runButton"
        >
          {loading ? "Running Agents..." : "Run Readiness Analysis"}
        </button>
      </section>

      <section className="buildTeamCard">
        <div className="buildTeamHeader">
          <h2>Build Your Team</h2>
          <p>
            Add operational team members, certifications and workload data
            before running the readiness analysis.
          </p>
        </div>

        <div className="formGrid">
          <div className="formField">
            <label>👤 Name</label>
            <input
              placeholder="Ex: Ana"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>

          <div className="formField">
            <label>💼 Role</label>
            <input
              placeholder="Ex: Cloud Engineer"
              value={role}
              onChange={(e) => setRole(e.target.value)}
            />
          </div>

          <div className="formField formWide">
            <label>🏆 Certifications</label>
            <input
              placeholder="AZ-900, AZ-204, AZ-400"
              value={certifications}
              onChange={(e) => setCertifications(e.target.value)}
            />
          </div>

          <div className="formField">
            <label>⏱ Workload Hours</label>
            <input
              placeholder="40"
              value={workload}
              onChange={(e) => setWorkload(e.target.value)}
            />
          </div>

          <div className="formActions">
            <button
              type="button"
              onClick={addEmployee}
              className="addMemberButton"
            >
              + Add Team Member
            </button>

            <button
              type="button"
              onClick={resetTeam}
              className="resetButton"
            >
              Reset Demo Team
            </button>
          </div>
        </div>
      </section>

      <section className="scenario">
        <h2>Demo Scenario</h2>
        <p>
          The Cloud Operations Team needs to assess if it is ready to respond to
          an Azure production outage.
        </p>

        <div className="teamGrid">
          {employees.map((employee, index) => (
            <div className="memberCard" key={`${employee.name}-${index}`}>
              <h3>{employee.name}</h3>
              <p>{employee.role}</p>
              <span>{employee.workload_hours}h/week</span>
              <small>
                Certifications:{" "}
                {employee.certifications.length
                  ? employee.certifications.join(", ")
                  : "None"}
              </small>
            </div>
          ))}
        </div>
      </section>

      {loading && (
        <section className="loadingPanel">
          <h2>Initializing multi-agent workflow...</h2>
          <p>Routing operational data to specialized reasoning agents.</p>
        </section>
      )}

      {result && (
        <>
          <section className="summaryGrid">
            <div className="scoreCard gaugeCard">
              <span>Operational Readiness</span>

              <svg width="220" height="220" viewBox="0 0 220 220">
                <circle
                  cx="110"
                  cy="110"
                  r="90"
                  fill="none"
                  stroke="#1e293b"
                  strokeWidth="16"
                />

                <circle
                  cx="110"
                  cy="110"
                  r="90"
                  fill="none"
                  stroke="#22c55e"
                  strokeWidth="16"
                  strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={progress}
                  transform="rotate(-90 110 110)"
                />

                <text
                  x="110"
                  y="110"
                  textAnchor="middle"
                  dominantBaseline="middle"
                  fill="white"
                  fontSize="32"
                  fontWeight="bold"
                >
                  {score}%
                </text>
              </svg>
            </div>

            <div className={`scoreCard risk ${risk.toLowerCase()}`}>
              <span>Risk Level</span>
              <strong>{risk}</strong>
            </div>

            <div className="scoreCard">
              <span>Auditor Confidence</span>
              <strong>{result.final_report.auditor_confidence}</strong>
            </div>
          </section>
          {result.knowledge_base && (
            <section className="knowledgeSources">
              <h2>Foundry IQ Knowledge Sources</h2>
              <p>{result.knowledge_base.summary}</p>

              <div className="sourceGrid">
                {result.knowledge_base.sources.map((source) => (
                  <div className="sourceCard" key={source}>
                    <h3>Knowledge Document</h3>
                    <span>{source}</span>
                  </div>
                ))}
              </div>
            </section>
          )}
          <section className="agents">
            <h2>Multi-Agent Reasoning Workflow</h2>
            <p className="sectionIntro">
              Each agent analyzes a specific part of the operational readiness
              problem, then the Auditor Agent validates the reasoning before the
              final executive report is generated.
            </p>

            <div className="agentTimeline">
              {result.workflow.slice(0, visibleAgents).map((agent, index) => {
                const details = getAgentDetails(agent);

                return (
                  <div className="agentStep" key={agent.agent}>
                    <div className="stepNumber">{index + 1}</div>

                    <div className="agentContent">
                      <h3>{agent.agent}</h3>

                      <div className="agentStatus">✓ Analysis Completed</div>

                      <p>{agent.summary}</p>

                      <div className="highlight">{getAgentHighlight(agent)}</div>

                      {details.length > 0 && (
                        <ul>
                          {details.map((item: string) => (
                            <li key={item}>{item}</li>
                          ))}
                        </ul>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </section>

          {visibleAgents >= result.workflow.length && (
            <section className="report">
              <h2>Executive Report</h2>
              <p>{result.final_report.executive_summary}</p>

              <h3>Recommended Actions</h3>
              <ul>
                {result.final_report.recommendations.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </section>
          )}
        </>
      )}
    </main>
  );
}

export default App;