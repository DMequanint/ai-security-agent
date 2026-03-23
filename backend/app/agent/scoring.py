from app.schemas.models import LogFeatures, ThreatIntel, HistoricalContext, RiskScore

def compute_risk(logs: LogFeatures, intel: ThreatIntel, history: HistoricalContext) -> RiskScore:
    score = 0
    factors = []

    if logs.failed_logins > 20:
        score += 0.3
        factors.append("High failed login count")

    if intel.blacklisted:
        score += 0.4
        factors.append("Blacklisted IP")

    if history.past_incidents > 0:
        score += 0.2
        factors.append("Repeat offender")

    score = min(score, 1.0)

    if score > 0.8:
        severity = "critical"
    elif score > 0.6:
        severity = "high"
    elif score > 0.3:
        severity = "medium"
    else:
        severity = "low"

    return RiskScore(score=score, severity=severity, factors=factors)
