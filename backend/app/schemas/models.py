from pydantic import BaseModel
from typing import List, Literal, Optional

class SecurityEvent(BaseModel):
    event_id: str
    event: str
    logs: str
    source: str
    timestamp: str


class LogFeatures(BaseModel):
    ip: str
    failed_logins: int
    time_window_seconds: int


class ThreatIntel(BaseModel):
    ip: str
    blacklisted: bool
    country: str
    reputation_score: float


class HistoricalContext(BaseModel):
    ip: str
    past_incidents: int
    last_seen: Optional[str]


class RiskScore(BaseModel):
    score: float
    severity: Literal["low", "medium", "high", "critical"]
    factors: List[str]
class ThreatAssessment(BaseModel):
    threat_type: str
    severity: Literal["low", "medium", "high", "critical"]
    confidence: float
    risk_score: float
    recommended_actions: List[str]
    explanation: str
