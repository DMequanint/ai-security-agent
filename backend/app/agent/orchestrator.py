import asyncio
from app.agent.tools import analyze_logs, get_threat_intel
from app.agent.memory import get_historical_context
from app.agent.scoring import compute_risk
from app.schemas.models import ThreatAssessment

async def run_agent(event):
    # Analyze logs
    log_features = await analyze_logs(event.logs)

    #Fetch threat intel + history in parallel
    intel_task = get_threat_intel(log_features.ip)
    history_task = get_historical_context(log_features.ip)
    intel, history = await asyncio.gather(intel_task, history_task)

    # Compute risk
    risk = compute_risk(log_features, intel, history)

    #Build ThreatAssessment
    assessment = ThreatAssessment(
        threat_type="Brute Force" if log_features.failed_logins > 5 else "Suspicious Activity",
        severity=risk.severity,
        confidence=risk.score,
        risk_score=risk.score,
        recommended_actions=[
            "Block IP" if risk.score > 0.5 else "Monitor activity",
            "Notify admin" if risk.score > 0.7 else "Log for review"
        ],
        explanation=f"{log_features.failed_logins} failed logins detected from IP {log_features.ip}"
    )

    return assessment
