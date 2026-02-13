import re
from typing import Dict

async def event_reasoner(state: Dict, tools: Dict):
    summaries = []

    for event in state["logs"]:
        match = re.search(r"\b(\d{4,5})\b", event)
        if not match:
            continue

        event_id = int(match.group(1))
        mapping = tools["event_id_mapper"](event_id=event_id)

        summaries.append(f"EventID {event_id}: {mapping['meaning']}")

    if not summaries:
        summaries.append("No known security-relevant EventIDs detected.")

    return {"mapped_events": summaries}
