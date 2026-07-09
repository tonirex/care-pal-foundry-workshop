# Lab 4 (Portal) — Multi-Agent Care Pal: Orchestration 🟢

> **Navigator rail · ~50 min.** One agent can't be great at everything. Split the LOW-risk path into specialists and let a Workflow stitch the answers.

> **You'll use 3 agents.** The **triage** agent is the **`carepal-<initials>`** you already built in Labs 1–3 — don't recreate it. You only build **2 new specialists** below; the workflow chains all three.

## Step 1 — Build the two specialist agents
**Build → Agents → New agent → Build an agent.** In the **Create an agent** dialog, type the **Agent name**, then **Create and open playground**. In the playground, paste the **Instructions** and **Save** (the version bumps to v2). New agents start with **Web search ON by default**:

| New agent | Tools | Instructions |
|---|---|---|
| **`carepal-<initials>-education`** | **Keep Web search** — it's already on by default (no need to add it) | *"You answer post-discharge education/self-care questions. Ground every reply with web search and cite source titles + URLs, preferring healthhub.sg. You do not diagnose."* |
| **`carepal-<initials>-followup`** | **Remove Web search** — on the Web search tool row click the kebab (**⋮**) → **Remove**, so this agent has no tools | *"You schedule check-ins, suggest follow-up appointment types after discharge, and collect symptom responses. You do not diagnose."* |

After this you have three agents: `carepal-<initials>` (triage), `-education`, `-followup`.

## Step 2 — Open Workflows
**Build → Agents → Workflows (Preview)** → **Create**.

![Workflows tab](images/lab4-workflows-tab.png)

**Create** is a **dropdown** (Blank workflow / Sequential / Human in Loop / Group chat) — not a gallery of cards. Pick **Sequential** (triage → education → follow-up). The designer opens with a **Start → Agent → Agent → Agent** chain (it also ships with a few example marketing sticky notes you can ignore or hide via **Hide notes**).

![Workflow templates](images/lab4-templates.png)

## Step 3 — Wire the three agents (in order)
The canvas shows **Start → Agent → Agent → Agent**. Click the **first Agent node** — a **Node settings side panel** ("Agent") opens on the right. Use its **Select an agent** dropdown (it also offers *Create a new agent*), pick the agent, then **Done**. Repeat for each node, left to right:
1. **`carepal-<initials>`** (triage)
2. **`carepal-<initials>-education`**
3. **`carepal-<initials>-followup`**

Then **Save** — a **"Give your workflow a name"** dialog appears (the default name is `sequential-workflow`). Enter **`carepal-multiagent`** and **Save**.

![Sequential designer](images/lab4-built.png)

## Step 4 — Where the orchestration (triage) rule lives
The triage logic is the **first agent's Instructions** — i.e. `carepal-<initials>`, which already carries the routing rules from Labs 1–3. Open the triage agent → the **Instructions** box is exactly where this lives:

![Triage rule in the Instructions box](images/lab4-triage-rule.png)

Sequential simply runs all three nodes in order, so no extra orchestration is needed for today. *(Optional)* to make triage delegate only when needed, append to that same **Instructions** box:

```text
You are Care Pal's orchestrator. Triage every message first. For LOW-risk, delegate then
synthesise ONE reply: education -> Education agent; scheduling/check-ins -> Follow-Up agent.
Call only the specialists needed. Medium/high risk -> do NOT delegate (timely_review /
immediate_escalation). Return the same triage JSON; merge specialist source_labels/source_urls.
```

## Step 5 — Test the compound question
**Preview** → `What follow-up appointments does my father need after heart failure, and what diet should he keep?` → the flow runs all three nodes in order and each returns clean JSON. Open **Traces** → confirm every node ran (green ✔).

![Workflow run — all nodes fired](images/lab4-trace.png)

**Verified live (carepal-multiagent):** triage → education → follow-up all fired — the **Traces** view shows *Conversation · Completed* with a green ✔ on each `InvokeAzureAgent` action (`carepal-demo`, `-education`, `-followup`). Education grounded its diet/appointment guidance with web sources (e.g. `healthhub.sg`, `heart.org`); Follow-Up returned a structured follow-up plan. Both appointments **and** diet were covered in one reply.

> Sequential runs every node each turn — perfect to *show* multi-agent. To delegate only when needed, add the optional triage rule in Step 4 and use connected agents instead.

## ✅ Validation
Paste reply + trace showing ≥2 specialist nodes ran, covering both topics.

## 🎁 Optional challenge
Add a 3rd specialist (Assessment or Enrollment) and show it firing on a fitting question.

---

### 🧭 Where next?
⬅️ Previous: [Lab 3 · Govern & Observe (Portal)](lab-03-portal.md) — 🏠 [Portal track index](PORTAL-TRACK.md) — Next: [Lab 5 · Extend & Deploy (Portal)](lab-05-portal.md) ➡️

> 🟡🔴 On the notebook/SDK rail? See the full rail-tabbed lab: **[lab-04.md](lab-04.md)**.
