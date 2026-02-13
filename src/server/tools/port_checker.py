# import subprocess
# import json

# class PortCheckerTool:
#     def __init__(self):
#         self.name = "port_checker"
#         self.description = "Checks if a local TCP port is listening and identifies the owning process"

#     def run(self, payload: dict):
#         port = payload.get("port")

#         if not port:
#             return {
#                 "response": None,
#                 "error": "Port is required",
#                 "metadata": {}
#             }

#         ps_script = f"""
#         $port = {port}

#         $conn = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue

#         if ($conn) {{
#             $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue

#             [PSCustomObject]@{{
#                 Port = $port
#                 Status = "LISTENING"
#                 PID = $conn.OwningProcess
#                 ProcessName = $proc.ProcessName
#             }} | ConvertTo-Json
#         }} else {{
#             [PSCustomObject]@{{
#                 Port = $port
#                 Status = "NOT_LISTENING"
#             }} | ConvertTo-Json
#         }}
#         """

#         try:
#             result = subprocess.run(
#                 ["powershell", "-NoProfile", "-Command", ps_script],
#                 capture_output=True,
#                 text=True
#             )

#             if result.returncode != 0:
#                 return {
#                     "response": None,
#                     "error": "Failed to check port",
#                     "metadata": {}
#                 }

#             return {
#                 "response": json.loads(result.stdout),
#                 "error": None,
#                 "metadata": {"source": "Local Port Checker"}
#             }

#         except Exception as e:
#             return {
#                 "response": None,
#                 "error": str(e),
#                 "metadata": {}
#             }
# if __name__ == "__main__":
#     tool = PortCheckerTool()
#     test_payload = {"port": 443}
#     result = tool.run(test_payload)
#     print(json.dumps(result, indent=4))




import subprocess
import json
from mcp.server.fastmcp import FastMCP

def register(mcp: FastMCP):

    @mcp.tool()
    def port_checker(port: int):
        """
        Checks if a local TCP port is listening and identifies owning process
        """

        ps_script = f"""
$port = {port}
$conn = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue
if ($conn) {{
    $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
    (
        [PSCustomObject]@{{
            Port = $port
            Status = "LISTENING"
            PID = $conn.OwningProcess
            ProcessName = $proc.ProcessName
            ProcessId = $proc.Id
            Path = $proc.Path
            StartTime = $proc.StartTime
        }}
    ) | ConvertTo-Json -Depth 3
}} else {{
    (
        [PSCustomObject]@{{
            Port = $port
            Status = "NOT_LISTENING"
        }}
    ) | ConvertTo-Json
}}
"""



        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()
        if not output:
            return {"error": "No output from PowerShell", "stderr": result.stderr}

        try:
            return json.loads(output)
        except Exception as e:
            return {"error": f"JSON parse failed: {e}", "raw": output}
