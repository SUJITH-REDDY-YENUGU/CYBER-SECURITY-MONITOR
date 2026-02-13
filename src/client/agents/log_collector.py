from typing import Dict

async def log_collector(state: Dict, tools: Dict):
    logs = tools["event_log_scanner"](limit=10)
    return {"logs": logs}
