# Lab 5 (Portal) — Extend & Deploy: MCP Tool + Hosted Agent 🟢🔴

> **Demo for everyone · hands-on for Engineers · ~30 min.** Give Care Pal a real tool, then run it as a managed service.

## Part A — Add a tool via MCP
> **Pre-deployed by the admin.** The mock **appointments MCP** is hosted once on Azure Container Apps
> (no authentication, synthetic data) and the link is shared in this guide — see *Setup* below. There's
> nothing to start; you just paste the URL. *(Admin: `mcp-appointments/deploy-mcp.ps1`.)*
>
> **MCP server URL (live):** `https://carepal-appointments.delightfulpond-b7635e07.southeastasia.azurecontainerapps.io/mcp`

1. On `carepal-<initials>` → **Tools → Add → Browse all tools**.

![Tool catalog](images/lab5-tool-catalog.png)

2. Open the **Custom** tab → **Model Context Protocol (MCP)** → **Create**.

![Custom: OpenAPI / MCP / A2A](images/lab5-custom-mcp.png)

3. Fill **Name** (`appointments`), paste the shared **Remote MCP Server endpoint** (the `/mcp` URL above),
   and set **Authentication** to **Unauthenticated** — the mock server needs no auth, so the Credential
   fields disappear. **Connect**. *(The dropdown also offers Key-based / OAuth Identity Passthrough /
   Microsoft Entra; older builds had no "None" option, which is why earlier runs used a throwaway key.)*

![MCP config form](images/lab5-mcp-form.png)

4. On the **appointments** tool row, click the kebab (**⋮**) → **Configure**. Under **Approval setting for
   tools in this MCP server**, keep **Never auto-approve tools** (the default — it means the agent must ask
   before *every* MCP call, i.e. approval "always"). **Apply**, then **Save** the agent. Now chat:
   `Can you arrange my father's heart-failure follow-up next week?` → give a patient ref and confirm the
   slot → the agent calls the MCP tools (`list_slots`, then `book_appointment`) and pauses each time for
   **Approve / Deny** (the Approve split-button also offers *Approve once* / *Always approve this tool* /
   *Always approve all tools*):

![MCP approval prompt — book_appointment](images/lab5-mcp-approval.png)

Approve → it returns a booking ref like `MOCK-CAR-20260713-0930` (synthetic).

> Human-in-the-loop: any "booking/medication" action should always require approval.

> 🧑‍💼 **Setup (admin, before the workshop).** Deploy the mock MCP once and share the `/mcp` URL above:
> ```powershell
> az login
> cd content/assets/mcp-appointments
> ./deploy-mcp.ps1            # public, no-auth Container App; prints the /mcp endpoint
> ```
> Builds from source (no Docker needed), stays up all day, synthetic data. See `mcp-appointments/README.md`.
>
> 💰 **Cost.** 0.5 vCPU / 1 GiB, min 1 replica (stays warm). The monthly free grant (180k vCPU-s, 360k GiB-s, 2M requests) covers most of it: **~$6 for two weeks** at workshop traffic, ~$15 worst-case if always active. Delete after with `az group delete -n rg-carepal-mcp`.

## Part B — Publish / deploy the hosted agent
Top-right **Publish** opens a menu: **Active version** (promote a saved version), **Set up routine**,
**Preview web app**, **Teams & Microsoft 365 Copilot**, and **Details**.

![Publish menu](images/lab5-publish.png)

**Preview web app** opens a standalone, shareable chat site for the agent — it greets you by name and has
*New chat* / *Share* / *Code*. This is the quickest way to try the hosted agent; it opened and answered
correctly (valid triage JSON + healthhub.sg citations) when verified live during this workshop.

> ⚠️ **Demo-only for the other channels — two reasons.**
> 1. **No Teams license:** the workshop tenant has no Teams / Microsoft 365 license, so the *Teams &
>    Microsoft 365 Copilot* channel can be published but **not tested end-to-end**. Use the **Preview web
>    app** channel to actually try the agent.
> 2. **RBAC:** promoting to shared channels or standing up a full hosted deployment needs the **Foundry
>    Project Manager** role; the **Foundry User** role participants hold can build, run, and open the
>    Preview web app, but production publishing is done by the facilitator from a Project Manager / Owner
>    account.

Engineers can deploy as code via **VS Code Foundry Toolkit** (Code Remote) or **azd up**.

## Validation — call the deployed agent
**Call agent** tab gives the **Project endpoint** + ready SDK snippet (`azure-ai-projects>=2.1.0`, the current API). Ping with the diet question and confirm valid 7-key triage JSON + healthhub.sg citation.

![Call agent endpoint + SDK](images/lab5-call-agent.png)

## ✅ Validation
Submit your endpoint/agent ID.

> **Navigator/Builder reflection:** (1) What does MCP give an agent? (2) Why deploy vs playground? (3) One Care Pal task you'd give a real tool. (4) What should always need approval? (5) Rate 1–5.

## ⭐ Optional stretch — connect a channel (demo only)
Out of timebox — skip with no penalty. Surface hosted Care Pal on a WhatsApp/Telegram sandbox.

---

### 🧭 Where next?
⬅️ Previous: [Lab 4 · Multi-Agent (Portal)](lab-04-portal.md) — 🏠 [Portal track index](PORTAL-TRACK.md) — 🎉 **You've finished the Care Pal build!**

> 🟡🔴 On the notebook/SDK rail? See the full rail-tabbed lab: **[lab-05.md](lab-05.md)**.
