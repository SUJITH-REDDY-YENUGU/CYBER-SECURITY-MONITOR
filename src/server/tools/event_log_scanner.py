# import subprocess
# import json

# class EventLogScannerTool:
#     def __init__(self):
#         self.name = "event_log_scanner"
#         self.description = "Fetches the most recent Windows Security event logs"

#     def run(self, payload: dict):
#         limit = payload.get("limit", 50)
#         event_id = payload.get("event_id")  # optional

#         ps_script = f"""
#         $events = Get-WinEvent -FilterHashtable @{{LogName='Security'}} -MaxEvents {limit} |
#         Select @{{
#             Name='TimeCreated';
#             Expression={{ $_.TimeCreated.ToString("o") }}
#         }}, Id, LevelDisplayName, Message

#         $events | ConvertTo-Json -Depth 3
#         """

#         try:
#             result = subprocess.run(
#                 ["powershell", "-NoProfile", "-Command", ps_script],
#                 capture_output=True,
#                 text=True
#             )

#             if result.returncode != 0:
#                 return {
#                     "response": [],
#                     "error": "Insufficient privileges to read Security logs",
#                     "metadata": {"source": "Windows Security Log"}
#                 }

#             events = json.loads(result.stdout)

#             # Ensure list (PowerShell returns dict if single event)
#             if isinstance(events, dict):
#                 events = [events]

#             # Optional EventID filtering
#             if event_id:
#                 events = [e for e in events if e["Id"] == event_id]

#             return {
#                 "response": events,
#                 "error": None,
#                 "metadata": {
#                     "source": "Windows Security Log",
#                     "count": len(events)
#                 }
#             }

#         except Exception as e:
#             return {
#                 "response": [],
#                 "error": str(e),
#                 "metadata": {"source": "Windows Security Log"}
#             }




import subprocess
import json
from mcp.server.fastmcp import FastMCP

def register(mcp: FastMCP):

    @mcp.tool()
    def event_log_scanner(limit: int = 50, event_id: int | None = None):
        """
        Fetch recent Windows Security event logs
        """

        ps_script = f"""
        Get-WinEvent -FilterHashtable @{{LogName='Security'}} -MaxEvents {limit} |
        Select @{{
            Name='TimeCreated';
            Expression={{ $_.TimeCreated.ToString("o") }}
        }}, Id, LevelDisplayName, Message |
        ConvertTo-Json -Depth 3
        """

        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {"error": "Insufficient privileges to read Security log"}

        events = json.loads(result.stdout)
        if isinstance(events, dict):
            events = [events]

        if event_id:
            events = [e for e in events if e["Id"] == event_id]

        return {
            "events": events,
            "count": len(events)
        }
