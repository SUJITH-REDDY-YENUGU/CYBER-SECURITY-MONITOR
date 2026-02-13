# ⚙️ Setup Guide

This guide explains how to set up the **Cybersecurity Monitor (MCP-based Agent System)** on your local machine.

---

## ✅ Prerequisites

Make sure you have the following installed:

* **Python 3.11 or higher**
* **pip** (comes with Python)
* **Git**
* A **Groq API key** (for evaluation only)

> ℹ️ The MCP server itself does **not** require any LLM or API key.

---

## 📥 Clone the Repository

```bash
git clone <your-repo-url>
cd CYBER-SECURITY-MONITOR
```

---

## 🐍 Create Virtual Environment (Recommended)

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 📦 Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt` yet, minimum required packages are:

```txt
fastmcp
deepeval
litellm
python-dotenv
pytest
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```
CYBER-SECURITY-MONITOR/
│
├── .env
├── src/
├── evaluation/
└── docs/
```

### `.env` example

```env
GROQ_API_KEY=your_groq_api_key_here
```

⚠️ Notes:

* **No `OPENAI_API_KEY` is required**
* This key is only used by **DeepEval judge models**
* MCP server tools remain deterministic and safe

---

## 📂 Verify Folder Structure

Make sure your structure looks like this:

```
CYBER-SECURITY-MONITOR/
│
├── src/
│   ├── server/
│   │   └── main.py
│   └── client/
│       └── main.py
│
├── evaluation/
│   └── deepeval/
│       └── test_agent_reasoning.py
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

## 🧪 Verify Installation

###  Run the MCP Server
```bash

python src/server/main.py
```


### 1️⃣ Run the MCP Client

```bash

python src/client/main.py
```

You should see:

```
=== FINAL SECURITY REPORT ===
<generated analysis>
```

---

### 2️⃣ Run Evaluation Tests

```bash
pytest evaluation/deepeval/test_agent_reasoning.py
```

Expected output:

```
1 passed in X.XXs
```

This confirms:

* MCP client runs correctly
* DeepEval is configured properly
* Judge model is accessible

---

## 🛠️ Common Issues & Fixes

### ❌ `ModuleNotFoundError: evaluation`

✔ Fix:

```bash
touch evaluation/__init__.py
```

---

### ❌ `ModuleNotFoundError: litellm`

✔ Fix:

```bash
pip install litellm
```

---

### ❌ DeepEval asking for OpenAI key

✔ Fix:

* Ensure **no `OPENAI_API_KEY`** is set
* Use `LiteLLMModel` with `groq/*` models only

---
