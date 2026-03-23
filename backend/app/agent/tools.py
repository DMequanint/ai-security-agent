import asyncio
from app.schemas.models import LogFeatures, ThreatIntel

async def analyze_logs(logs: str) -> LogFeatures:
    await asyncio.sleep(0.1)
    return LogFeatures(
        ip="192.168.1.10",
        failed_logins=25,
        time_window_seconds=120
    )

async def get_threat_intel(ip: str) -> ThreatIntel:
    await asyncio.sleep(0.1)
    return ThreatIntel(
        ip=ip,
        blacklisted=True,
        country="Unknown",
        reputation_score=0.87
    )
