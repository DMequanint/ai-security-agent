from app.schemas.models import HistoricalContext

MEMORY_DB = {
    "192.168.1.10": {
        "past_incidents": 3,
        "last_seen": "2026-03-10"
    }
}

async def get_historical_context(ip: str) -> HistoricalContext:
    data = MEMORY_DB.get(ip, {"past_incidents": 0, "last_seen": None})
    return HistoricalContext(ip=ip, **data)
