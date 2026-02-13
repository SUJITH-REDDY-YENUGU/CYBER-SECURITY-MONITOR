from mcp.server.fastmcp import FastMCP

def register(mcp: FastMCP):

    @mcp.tool()
    def event_id_mapper(event_id: int):
        """
        Maps Windows Security Event IDs to human-readable meanings
        """

        mapping = {
            # Authentication
            4624: "Successful logon",
            4625: "Failed logon (possible brute-force attempt)",
            4634: "Logoff",
            4647: "User initiated logoff",
            4648: "Logon with explicit credentials",
            4675: "SIDs were filtered",

            # Privilege / Account abuse
            4672: "Special privileges assigned to new logon (admin-level access)",
            4719: "System audit policy changed",
            4720: "User account created",
            4722: "User account enabled",
            4726: "User account deleted",
            4732: "User added to a local security group",
            4733: "User removed from a local security group",

            # Process / execution
            4688: "New process created (possible malware execution)",
            4689: "Process terminated",
            4697: "Service installed",

            # Credential access
            5379: "Credential Manager credentials were read",
            4776: "Credential validation attempt",

            # Persistence
            4698: "Scheduled task created",
            4699: "Scheduled task deleted",
            4700: "Scheduled task enabled",
            4701: "Scheduled task disabled",

            # Remote access
            4778: "RDP session reconnected",
            4779: "RDP session disconnected",

            # File / registry
            4663: "Object access attempt",
            4657: "Registry value modified",

            # High risk
            1102: "Security event log cleared (HIGH RISK)"
        }

        return {
            "event_id": event_id,
            "meaning": mapping.get(event_id, "Unknown or uncommon Event ID")
        }










# class EventIDMapperTool:
#     def __init__(self):
#         self.name = "event_id_mapper"
#         self.description = "Maps Windows Security Event IDs to human-readable meanings"

#     def run(self, payload: dict):
#         event_id = payload.get("event_id")

#         mapping = {
#             # --- Authentication ---
#             4624: "Successful logon",
#             4625: "Failed logon (possible brute-force attempt)",
#             4634: "Logoff",
#             4647: "User initiated logoff",
#             4648: "Logon with explicit credentials",
#             4675: "SIDs were filtered",

#             # --- Privilege / Account Abuse ---
#             4672: "Special privileges assigned to new logon (admin-level access)",
#             4719: "System audit policy was changed",
#             4732: "User added to a local security group",
#             4733: "User removed from a local security group",
#             4720: "User account created",
#             4722: "User account enabled",
#             4726: "User account deleted",

#             # --- Process / Execution ---
#             4688: "New process created (possible malware execution)",
#             4689: "Process terminated",
#             4697: "Service installed on the system",

#             # --- Credential Access ---
#             5379: "Credential Manager credentials were read",
#             4776: "Domain controller attempted to validate credentials",

#             # --- Scheduled Tasks / Persistence ---
#             4698: "Scheduled task created",
#             4699: "Scheduled task deleted",
#             4700: "Scheduled task enabled",
#             4701: "Scheduled task disabled",

#             # --- Network / Remote Access ---
#             4778: "Remote Desktop session reconnected",
#             4779: "Remote Desktop session disconnected",

#             # --- File / Object Access ---
#             4663: "An attempt was made to access an object",
#             4657: "Registry value modified",

#             # --- Policy / Security Changes ---
#             4715: "Audit policy changed",
#             1102: "Security event log was cleared (HIGH RISK)"
#         }

#         meaning = mapping.get(event_id, "Unknown or less common Event ID")

#         return {
#             "response": {
#                 "event_id": event_id,
#                 "meaning": meaning
#             },
#             "error": None,
#             "metadata": {
#                 "source": "Windows Security Event ID Reference"
#             }
#         }

