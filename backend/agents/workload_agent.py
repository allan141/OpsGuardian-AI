def run_workload_agent(team_data: dict) -> dict:
    employees = team_data.get("employees", [])

    total_workload = 0
    overloaded = []

    for employee in employees:
        workload = employee.get("workload_hours", 40)
        total_workload += workload

        if workload > 42:
            overloaded.append({
                "employee": employee.get("name"),
                "workload_hours": workload,
                "risk": "Overloaded"
            })

    average_workload = round(total_workload / len(employees), 2) if employees else 0

    if average_workload > 42:
        workload_status = "High"
    elif average_workload >= 35:
        workload_status = "Moderate"
    else:
        workload_status = "Healthy"

    return {
        "agent": "Workload Agent",
        "summary": "Analyzes team capacity, workload pressure, and availability.",
        "average_workload": average_workload,
        "workload_status": workload_status,
        "overloaded_members": overloaded
    }