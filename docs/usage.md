# ▶️ Usage Guide

This document explains how to **run**, **use**, and **evaluate** the Cybersecurity Monitor system.

---

## 🧠 Overview

The system works in three stages:

1. **MCP Server** exposes deterministic security tools
2. **MCP Client (Agent)** calls tools and generates a security report
3. **Evaluation (DeepEval)** judges the reasoning quality of the report

---

## 1️⃣ Running the MCP Server

The MCP server exposes security tools such as:

* Event log scanning
* Process and port inspection
* File integrity checks

### Start the MCP Server

```bash
python src/server/main.py
```

Expected output:

```
🚀 MCP Server started
📡 Tools registered successfully
```

> ℹ️ Keep this terminal **running** while using the client.

---

## 2️⃣ Running the MCP Client (Security Agent)

The client acts as a **SOC-style AI agent**.
It:

* Connects to the MCP server
* Calls tools
* Produces a final security report

### Run the Client

Open a new terminal (server should still be running):

```bash
python src/client/main.py
```

Expected output:

```
=== FINAL SECURITY REPORT ===
<Event analysis>
<Detected risks>
<Recommendations>
<Uncertainty notes>
```

### What the Client Does

* Collects system signals via MCP tools
* Avoids hallucinating unavailable data
* Clearly states uncertainty if evidence is missing
* Produces human-readable SOC-style output

---

## 3️⃣ Understanding the Security Report

A typical report contains:

* **Event Analysis** – What was observed
* **Risk Assessment** – Potential threats
* **Recommendations** – Practical next steps
* **Uncertainty Handling** – Explicit limitations

This design ensures the agent remains:

* Evidence-grounded
* Explainable
* Auditable

---

## 4️⃣ Running Evaluation (DeepEval)

Evaluation checks **reasoning quality**, not just correctness.

### Run Evaluation Test

```bash
pytest evaluation/deepeval/test_agent_reasoning.py
```

### Metrics Used

* **HallucinationMetric**
  Ensures no fabricated events or evidence

* *(Optional / extendable)*
  Answer relevancy and judgment quality metrics

### Successful Output

```
1 passed in X.XXs
```

This confirms:

* Agent output is grounded
* Reasoning is consistent
* No hallucinations detected

---

## 5️⃣ When to Use Evaluation

Use evaluation when:

* Changing prompts
* Adding new MCP tools
* Modifying agent logic
* Preparing for demos, exams, or benchmarks

You **do not** need to run evaluation for normal usage.

---

## 6️⃣ Typical Workflow

```text
Start MCP Server
      ↓
Run MCP Client
      ↓
Review Security Report
      ↓
(Optional) Run DeepEval
```

---

## 7️⃣ Notes & Best Practices

* MCP tools should stay **deterministic**
* LLMs are only used for:

  * Report synthesis
  * Evaluation (judge models)
* Avoid adding LLMs inside MCP tools
* Keep `.env` keys only for evaluation models

---

## ✅ Summary

* `src/server/main.py` → exposes security tools
* `src/client/main.py` → generates security report
* `evaluation/` → validates agent reasoning

The system is:

* Modular
* Testable
* Production-aligned
* Research-ready

---

