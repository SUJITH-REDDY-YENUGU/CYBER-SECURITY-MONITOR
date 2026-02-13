import asyncio
from dotenv import load_dotenv
from smolagents import MCPClient
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from agents.log_collector import log_collector
from agents.event_reasoner import event_reasoner
from agents.threat_analyst import threat_analyst

load_dotenv()

def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

async def main():
    # MCP client
    client = MCPClient(
        {"url": "http://localhost:8000/sse", "transport": "sse"},
        structured_output=False,
    )
    tools = {tool.name: tool for tool in client.get_tools()}

    # LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0,
    )

    prompt_template = load_prompt(
        "src/client/prompts/threat_analysis.txt"
    )

    # ---- async wrappers (THIS IS THE FIX) ----
    async def collect_logs_node(state):
        return await log_collector(state, tools)

    async def reason_events_node(state):
        return await event_reasoner(state, tools)

    async def analyze_threats_node(state):
        return await threat_analyst(state, llm, prompt_template)

    # Graph
    graph = StateGraph(dict)

    graph.add_node("collect_logs", collect_logs_node)
    graph.add_node("reason_events", reason_events_node)
    graph.add_node("analyze_threats", analyze_threats_node)

    graph.set_entry_point("collect_logs")
    graph.add_edge("collect_logs", "reason_events")
    graph.add_edge("reason_events", "analyze_threats")
    graph.add_edge("analyze_threats", END)

    app = graph.compile()

    result = await app.ainvoke({})

    print("\n=== FINAL SECURITY REPORT ===\n")
    print(result["analysis"])

if __name__ == "__main__":
    asyncio.run(main())










