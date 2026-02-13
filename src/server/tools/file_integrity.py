# import subprocess
# import json
# import os

# class FileSignatureTool:
#     def __init__(self):
#         self.name = "file_signature_check"
#         self.description = "Read-only digital signature verification for Windows files"

#     def run(self, payload: dict):
#         filepath = payload.get("filepath")

#         if not filepath or not os.path.exists(filepath):
#             return {
#                 "response": None,
#                 "error": "File does not exist",
#                 "metadata": {}
#             }

#         ps_script = f"""
#         $sig = Get-AuthenticodeSignature -FilePath "{filepath}"
#         $result = [PSCustomObject]@{{
#             Path = $sig.Path
#             Status = $sig.Status.ToString()
#             StatusMessage = $sig.StatusMessage
#             SignerCertificate = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Subject }} else {{ $null }}
#             Issuer = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Issuer }} else {{ $null }}
#         }}
#         $result | ConvertTo-Json
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
#                     "error": "Failed to verify digital signature",
#                     "metadata": {"file": filepath}
#                 }

#             signature_info = json.loads(result.stdout)

#             return {
#                 "response": {
#                     "file": signature_info["Path"],
#                     "signature_status": signature_info["Status"],
#                     "status_message": signature_info["StatusMessage"],
#                     "signer": signature_info["SignerCertificate"],
#                     "issuer": signature_info["Issuer"]
#                 },
#                 "error": None,
#                 "metadata": {"source": "Authenticode Signature Verification"}
#             }

#         except Exception as e:
#             return {
#                 "response": None,
#                 "error": str(e),
#                 "metadata": {"source": "Authenticode Signature Verification"}
#             }

# if __name__ == "__main__":
#     tool = FileSignatureTool()
#     test_payload = {"filepath": "C:\\Windows\\System32\\notepad.exe"}
#     result = tool.run(test_payload)
#     print(json.dumps(result, indent=4))





import subprocess
import json
import os
from mcp.server.fastmcp import FastMCP

def register(mcp: FastMCP):

    @mcp.tool()
    def file_signature_check(filepath: str):
        """
        Read-only digital signature verification for Windows files
        """

        if not os.path.exists(filepath):
            return {"error": "File does not exist"}

        ps_script = f"""
        $sig = Get-AuthenticodeSignature -FilePath "{filepath}"
        [PSCustomObject]@{{
            Path = $sig.Path
            Status = $sig.Status.ToString()
            StatusMessage = $sig.StatusMessage
            Signer = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Subject }} else {{ $null }}
            Issuer = if ($sig.SignerCertificate) {{ $sig.SignerCertificate.Issuer }} else {{ $null }}
        }} | ConvertTo-Json
        """

        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return {"error": "Signature verification failed"}

        return json.loads(result.stdout)
