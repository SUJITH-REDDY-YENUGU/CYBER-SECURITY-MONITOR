## 🛡️ Cybersecurity Monitor (MCP-based Agent System)

A modular **cybersecurity monitoring system** built using the **Model Context Protocol (MCP)**, featuring an agent-based client for security reasoning and a robust evaluation layer using **DeepEval**.

This project demonstrates how to build **tool-grounded AI agents** that analyze real system signals instead of hallucinating security events.

---

## ✨ Key Features

* 🔌 **MCP Server** exposing deterministic security tools
* 🧠 **Agent-based MCP Client** for SOC-style reasoning
* 📊 **LLM-as-a-Judge evaluation** using DeepEval
* 🚫 No LLM usage in the tool layer (safe-by-design)
* 🧪 Pytest-based automated evaluation
* 🔍 Hallucination and reasoning-quality detection

---

## 🏗️ Architecture Overview

```
MCP Client (Agents & Prompts)
        │
        │  MCP calls
        ▼
MCP Server (Security Tools)
        │
        ▼
Final Security Report
        │
        ▼
DeepEval (Reasoning Evaluation)
```

📄 Full details: [`docs/architecture.md`](docs/architecture.md)

---

## 📁 Project Structure

```
CYBER-SECURITY-MONITOR/
│
├── src/
│   ├── server/          # MCP Server (FastMCP)
│   │   ├── tools/       # Security tools
│   │   ├── utils/       # Helper utilities
│   │   └── main.py
│   │
│   └── client/          # MCP Client
│       ├── agents/      # Agent logic
│       ├── prompts/     # Prompt templates
│       └── main.py
│
├── evaluation/
│   └── deepeval/        # DeepEval tests & rubrics
│
├── docs/
│   ├── architecture.md
│   ├── setup.md
│   └── usage.md
│
├── .env
├── requirements.txt
└── README.md
```

---

## 🧠 How It Works

1. **MCP Server**

   * Exposes security tools (event logs, process checks, etc.)
   * Returns structured, deterministic data

2. **MCP Client**

   * Invokes MCP tools
   * Performs reasoning using prompt-driven agents
   * Generates a final security report

3. **Evaluation**

   * DeepEval runs the client
   * Evaluates reasoning quality using LLM-based judges
   * Detects hallucinations and weak conclusions

---

## 🧪 Evaluation Metrics

The system currently evaluates:

* **HallucinationMetric**
* **AnswerRelevancyMetric**
* **Custom GEval rubric** for security judgment quality

All evaluation runs are:

* Reproducible
* Non-intrusive to agent execution

---

## ⚙️ Tech Stack

* **Python 3.11**
* **Model Context Protocol (MCP)**
* **FastMCP**
* **DeepEval**
* **LiteLLM (Groq backend)**
* **pytest**

---

## 🚀 Getting Started

See:

* 📦 Installation: [`docs/setup.md`](docs/setup.md)
* ▶️ Running the system: [`docs/usage.md`](docs/usage.md)

---

## 🎯 Use Cases

* SOC agent prototyping
* Tool-grounded AI research
* AI hallucination evaluation
* Secure LLM system design
* MCP experimentation

---

## 🔒 Design Philosophy

> *“LLMs should reason — not invent.”*

This project enforces:

* Deterministic tool outputs
* Explicit reasoning chains
* Automated evaluation of AI behavior

---

## 📌 Status

* ✅ MCP Server implemented
* ✅ MCP Client implemented
* ✅ DeepEval integration working
* 🔄 Extensible for more tools and agents

---

## 📄 License

This project is provided for educational and research purposes.

---
