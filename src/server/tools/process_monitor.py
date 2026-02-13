# import subprocess
# import json

# class ProcessMonitorTool:
#     def __init__(self):
#         self.name = "process_monitor"
#         self.description = "Lists top CPU-consuming processes with path and digital signature status"

#     def run(self, payload: dict):
#         limit = payload.get("limit", 10)

#         ps_script = f"""
#         $procs = Get-Process |
#             Sort-Object CPU -Descending |
#             Select-Object -First {limit} Name, Id, CPU, Path

#         $results = foreach ($p in $procs) {{
#             $sig = $null
#             if ($p.Path) {{
#                 $sig = Get-AuthenticodeSignature -FilePath $p.Path -ErrorAction SilentlyContinue
#             }}

#             [PSCustomObject]@{{
#                 Name = $p.Name
#                 PID = $p.Id
#                 CPU = $p.CPU
#                 Path = $p.Path
#                 SignatureStatus = if ($sig) {{ $sig.Status.ToString() }} else {{ "Unknown" }}
#                 Signer = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Subject }} else {{ $null }}
#             }}
#         }}

#         $results | ConvertTo-Json
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
#                     "error": "Failed to retrieve process data",
#                     "metadata": {}
#                 }

#             processes = json.loads(result.stdout)

#             if isinstance(processes, dict):
#                 processes = [processes]

#             return {
#                 "response": processes,
#                 "error": None,
#                 "metadata": {
#                     "source": "Process Monitor",
#                     "count": len(processes)
#                 }
#             }

#         except Exception as e:
#             return {
#                 "response": [],
#                 "error": str(e),
#                 "metadata": {}
#             }
# if __name__ == "__main__":
#     tool = ProcessMonitorTool()
#     test_payload = {"limit": 1}
#     result = tool.run(test_payload)
#     print(json.dumps(result, indent=4))



import subprocess
import json
from mcp.server.fastmcp import FastMCP

def register(mcp: FastMCP):

    @mcp.tool()
    def process_monitor(limit: int = 10):
        """
        Lists top CPU-consuming processes with signature status
        """

        ps_script = f"""
        $procs = Get-Process |
            Sort-Object CPU -Descending |
            Select-Object -First {limit} Name, Id, CPU, Path

        $results = foreach ($p in $procs) {{
            $sig = $null
            if ($p.Path) {{
                $sig = Get-AuthenticodeSignature -FilePath $p.Path -ErrorAction SilentlyContinue
            }}
            [PSCustomObject]@{{
                Name = $p.Name
                PID = $p.Id
                CPU = $p.CPU
                Path = $p.Path
                SignatureStatus = if ($sig) {{ $sig.Status.ToString() }} else {{ "Unknown" }}
                Signer = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Subject }} else {{ $null }}
            }}
        }}
        $results | ConvertTo-Json
        """

        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {"error": "Failed to retrieve process data"}

        processes = json.loads(result.stdout)
        if isinstance(processes, dict):
            processes = [processes]

        return {
            "processes": processes,
            "count": len(processes)
        }


