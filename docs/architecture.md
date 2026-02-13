# Architecture

This project implements a modular **cybersecurity monitoring system** using the
Model Context Protocol (MCP) for tool execution, an agent-based client for reasoning,
and DeepEval for post-hoc evaluation of agent behavior.

The system is intentionally split into **three layers**:
1. Tool execution (MCP Server)
2. Reasoning & report generation (MCP Client)
3. Evaluation & testing (DeepEval)

---

## High-Level Flow

```

┌──────────────────────────────┐
│        MCP CLIENT            │
│  (Agent & Reasoning Layer)   │
│                              │
│  - Agents                    │
│  - Prompt templates          │
│  - Orchestration logic       │
└───────────────┬──────────────┘
│ MCP calls
▼
┌──────────────────────────────┐
│        MCP SERVER            │
│   (Security Tool Layer)      │
│                              │
│  - Event log scanning        │
│  - Process / port monitoring │
│  - File integrity checks     │
│  - Utility helpers           │
└───────────────┬──────────────┘
│ Structured results
▼
┌──────────────────────────────┐
│     FINAL SECURITY REPORT    │
│  (Human-readable output)    │
└───────────────┬──────────────┘
│
▼
┌──────────────────────────────┐
│      DEEPEVAL TESTS          │
│  (LLM-as-a-Judge Layer)      │
│                              │
│  - Hallucination detection   │
│  - Reasoning quality checks  │
│  - Evidence grounding        │
└──────────────────────────────┘

```

---

## Component Breakdown

### 1. MCP Server (`src/server`)

**Purpose:**  
Provide deterministic, auditable cybersecurity signals.

**Responsibilities:**
- Execute security-related tools
- Collect system and event data
- Return structured results to the client

**Key characteristics:**
- No LLM usage
- No reasoning or interpretation
- Safe, tool-only execution

**Structure:**
```

src/server/
├── tools/        # MCP-exposed security tools
├── utils/        # Helper utilities
└── main.py       # FastMCP server entrypoint

```

---

### 2. MCP Client (`src/client`)

**Purpose:**  
Act as a SOC-style agent that reasons over MCP tool outputs.

**Responsibilities:**
- Invoke MCP tools when needed
- Aggregate security signals
- Perform reasoning using prompt-driven agents
- Generate a final security report

**What happens here:**
- Tool results → reasoning → conclusions
- This is where LLM-based analysis lives

**Structure:**
```

src/client/
├── agents/       # Agent logic and workflows
├── prompts/      # Prompt templates
└── main.py       # Client entrypoint

```

---

### 3. Evaluation Layer (`evaluation/deepeval`)

**Purpose:**  
Evaluate *how well* the agent reasoned — not to control runtime behavior.

**Responsibilities:**
- Run the client
- Capture the final security report
- Evaluate reasoning using DeepEval metrics

**Key design choice:**
- Evaluation is **offline**
- Does not interfere with agent execution
- Uses an LLM only as a judge

**Metrics currently used:**
- Hallucination detection
- Relevancy to provided context
- Evidence-grounded security judgment

**Structure:**
```

evaluation/deepeval/
├── test_agent_reasoning.py
├── rubrics.py
└── **init**.py

```

---

## Design Principles

- **Separation of concerns**
  - Tools ≠ reasoning ≠ evaluation

- **Tool-grounded reasoning**
  - Agent conclusions must reflect MCP outputs

- **Deterministic tools**
  - Server layer remains predictable and auditable

- **LLM-as-a-judge**
  - Evaluation validates quality, not correctness of tools

- **Test-driven agent development**
  - Reasoning quality is enforced via pytest + DeepEval

---
