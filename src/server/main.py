from mcp.server.fastmcp import FastMCP

from tools import event_id_mapper
from tools import event_log_scanner
from tools import file_integrity
from tools import port_checker
from tools import process_monitor
# from tools import rag_retriever  # later

# fastmcp inspect looks for this variable
mcp = FastMCP("CybersecurityMonitor")

# Register all tools
event_id_mapper.register(mcp)
event_log_scanner.register(mcp)
file_integrity.register(mcp)
port_checker.register(mcp)
process_monitor.register(mcp)
# rag_retriever.register(mcp)

if __name__ == "__main__":
    mcp.run(transport="sse")
