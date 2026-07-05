---
id: lab-05
title: "Lab 5: Extend & Deploy — MCP Tool + Hosted Agent"
duration_minutes: 30
audience: ["Engineers hands-on; everyone watches the demo"]
foundry_capabilities: ["MCP tools", "Human-in-the-loop approval", "Hosted agents", "Deployment (azd / VS Code Toolkit)"]
order: 5
is_active: false
max_points: 200
bonus_quest: true
rails: ["engineer"]
tier: "L300"
---

> 🩺 **Mr. Rajan — Chapter 5**
> A week in, Care Pal needs to do something real — check an actual follow-up appointment slot — and
> be reachable at any hour, not just in a playground tab. The team gives it a tool (via MCP) and
> deploys it as a hosted agent.

## Format note (protects the one-day timebox)
This lab is **demo-for-everyone, hands-on for the 🔴 Engineer track.** Navigator/Builder participants
watch, then complete a short reflection card for participation points. Engineers run Parts A & B.

## What you'll learn
Two production muscles: giving an agent a **real tool** through the open **Model Context Protocol
(MCP)** with human approval, and **deploying** Care Pal as a **hosted agent** so it runs as a managed
service instead of a playground session.

---

## Part A — Add a tool via MCP (🔴 hands-on, ~10 min)
Connect the provided mock **appointments MCP** server so Care Pal can look up and *propose* a
follow-up slot — with **human-in-the-loop approval** before it "books".

1. The admin pre-deploys the mock MCP once (no auth, synthetic) — `mcp-appointments/deploy-mcp.ps1`
   prints a public `https://…/mcp` URL. To run it yourself instead: `python mcp-appointments/server.py`
   + a tunnel (README has both paths).
2. Attach it to your agent as an **MCP tool** (portal **Tools → MCP** — the form has no "None" auth, so
   leave Key-based + a throwaway header; or SDK `MCPTool(server_label, server_url, require_approval)`).
3. Set **`require_approval="always"`** so the agent must ask before calling `book_appointment`.
4. Ask: *"Can you arrange my father's heart-failure follow-up next week?"* → approve the call →
   confirm it returns a proposed slot.

*(Pattern: azure-ai-projects 2.x → `samples/agents/tools/sample_agent_mcp.py`.)*

📚 **Docs:** [Model Context Protocol (MCP) tool](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/model-context-protocol) ·
[MCP specification](https://modelcontextprotocol.io/) ·
sample: [`sample_agent_mcp.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_mcp.py)

## Part B — Deploy a hosted agent (🔴 hands-on, ~15 min)
Deploy Care Pal to **Foundry Agent Service** as a hosted agent.

- **Option 1 — VS Code Foundry Toolkit:** sidebar → **Deploy to Microsoft Foundry** → pick the
  shared project → deploy as **Code (Remote)**. *(Ref: VS Code "Create and deploy a hosted agent".)*
- **Option 2 — azd:** from the provided scaffold, `azd up`.

Then call the deployed agent from the **Agent Inspector / Call agent** and confirm it returns a valid
triage JSON. *(Pattern: Foundry-Agent-Lab → `hosted-demo`; agentic-ai-immersion → Deployment / azd.)*

📚 **Docs:** [What is Foundry Agent Service?](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview) ·
[Azure Developer CLI (`azd`)](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/) ·
[`azd up`](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/reference#azd-up)

---

## ✅ Validation
Submit your **hosted agent endpoint or agent ID** (+ key if required). The platform pings it with
**"What diet should my father follow after heart failure?"** and checks the response is **valid triage
JSON** (7 keys) with a `healthhub.sg` citation. **(200 pts · badge 🚀 Deployer)**

> Navigator/Builder reflection card (100 participation pts): *(1)* In your words, what does MCP give
> an agent? *(2)* Why deploy a hosted agent instead of using the playground? *(3)* One Care Pal task
> you'd give a real tool. *(4)* What should always require human approval? *(5)* Rate this session 1–5.

## ⭐ Optional stretch — connect a channel (demo only, if time remains)
**Out of the core timebox — skip with no penalty.** Surface the hosted Care Pal on a **WhatsApp or
Telegram sandbox** so a phone in the room can chat to it, closing the loop to the customer's real
front-end. **(+100 stretch · badge 📲 Channel Pioneer)**

## Stuck?
- MCP tool not appearing? Confirm the server is running and the agent lists it under **Tools**.
- Deploy fails on dependencies? Use **Code (Remote)** so Azure installs from `requirements.txt`.
- Short on time? Stop after Part A — Part B can be the closing facilitator demo.

---

### 🧭 Where next?
⬅️ Previous: [Lab 4 · Multi-Agent Care Pal](lab-04.md) — 🏠 [Workshop flow & rails](../../README.md#how-the-workshop-flows) — 🎉 **You've finished the Care Pal build!**

> 🟢 Navigator screenshot version of this demo: **[lab-05-portal.md](lab-05-portal.md)** · all portal labs: [PORTAL-TRACK.md](PORTAL-TRACK.md)
