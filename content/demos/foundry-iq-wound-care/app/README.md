# Engineer client — Foundry IQ wound-care demo

Optional Python client for the [Foundry IQ wound-care demo](../README.md). It talks to the
`woundcare-iq-agent` you build in the portal and shows the **human-in-the-loop approval** flow for
each Foundry IQ knowledge-base lookup.

> Adapted from Microsoft Learn exercise
> [04 · Integrate an AI agent with Foundry IQ](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/04-integrate-agent-with-foundry-iq.html)
> — the tutorial's two `TODO`s are already completed here, and the prompts/labels are wound-care.

## Prerequisites
- You've completed Parts 1–2 of [../README.md](../README.md) (agent `woundcare-iq-agent` exists with
  the `ks-woundcare` Foundry IQ knowledge base and **no** web search tool).
- Python 3.11+ and the Azure CLI (`az`) installed.
- **To see the approval prompt:** set the agent to *Ask for approval for all tools* using the
  **Foundry Toolkit for VS Code** extension (Prompt Agents → `woundcare-iq-agent` → Tools → select the
  Foundry IQ / Azure AI Search tool → **Require approval before using tools = Ask for approval for all
  tools**). Without this, the client still works — it just won't pause for approval.

## Run
```bash
python -m venv .venv
# Windows:  .venv\Scripts\Activate.ps1      macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
az login
cp .env.example .env      # set PROJECT_ENDPOINT and AGENT_NAME
python agent_client.py
```

## Try
- `How should I care for a small cut or abrasion at home?`  → grounded answer + citation
- `What should someone with a slow-healing wound eat?`      → grounded answer + citation
- `How do I treat a jellyfish sting?`                        → declines (not in the sources)
- `history`  → show the conversation · `quit`  → exit

When prompted `Approve this knowledge-base lookup? (yes/no)`, type `yes` to let the agent query
Foundry IQ, then watch the grounded, cited answer come back.

## Files
| File | Purpose |
|------|---------|
| `agent_client.py` | Completed conversations/responses client with Foundry IQ approval handling |
| `.env.example` | Template for `PROJECT_ENDPOINT` and `AGENT_NAME` |
| `requirements.txt` | `azure-ai-projects`, `azure-identity`, `python-dotenv` |
