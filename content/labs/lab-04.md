---
id: lab-04
title: "Lab 4: Multi-Agent Care Pal — Orchestration"
duration_minutes: 50
audience: ["Everyone (builders & engineers go deeper)"]
foundry_capabilities: ["Multi-agent orchestration", "Workflows", "Function tools"]
order: 4
is_active: false
max_points: 300
bonus_quest: true
rails: ["navigator", "builder", "engineer"]
tier: "L300"
---

> 🩺 **Mr. Rajan — Chapter 4**
> Day five, Rajan is steadier. Priya asks two things at once: *"What follow-up appointments does my
> father need, and what diet should he keep?"* Scheduling and education are different jobs — so the
> triage agent hands off to specialist agents and stitches their answers into one reply.

## What you'll learn
One agent doing everything gets brittle. The customer's design uses **five core agents** (Navigation,
Education, Assessment, Follow-Up, Enrollment). You'll turn your triage agent into an **orchestrator**
that delegates the LOW-risk path to specialists and synthesises their results — Foundry's
**connected / multi-agent** pattern.

> Required today: **Education** + **Follow-Up** (plus your triage orchestrator). Navigation /
> Assessment / Enrollment are the bonus.

## Demo (facilitator, 5 min)
Send the compound question on a prepared orchestrator → walk the **trace**: orchestrator → Follow-Up
agent → Education agent → synthesised reply. Point out two specialist calls in one turn.

---

## 🟢 Navigator — portal
1. Create two specialist agents (or clone from `carepal-reference`):
   - **`carepal-<initials>-education`** — reuse your Lab 2 grounded agent (it already cites HealthHub).
   - **`carepal-<initials>-followup`** — Instructions: *"You schedule check-ins, suggest follow-up
     appointment types after discharge, and collect symptom responses. You do not diagnose."*
2. Connect them with the portal's **multi-agent Workflow** (Agents → **Workflows**): set your
   **triage** agent as the entry point and wire **Education** and **Follow-Up** as specialist nodes.
   *(Connected Agents is retired in the new API — **Workflows** is the current no-code multi-agent
   path; your facilitator demos the exact clicks.)*
3. Update the triage Instructions with the orchestration rule:

```text
You are Care Pal's orchestrator. Triage every message first (intent, risk_level, route).
For LOW-risk paths, delegate and then synthesise ONE combined reply:
- education / self-care content   -> Education agent
- follow-up scheduling, check-ins, symptom tracking -> Follow-Up agent
- service navigation / next steps  -> Navigation agent (bonus)
Call only the specialists needed. For medium/high risk, do NOT delegate — route to timely_review or
immediate_escalation as before. Return the same triage JSON; put the synthesised answer in reply and
merge any source_labels / source_urls from the specialists.
```

4. **Chat** → send **`What follow-up appointments does my father need after heart failure, and what
   diet should he keep?`** → confirm the reply covers **both** appointments **and** diet (grounded).
5. Open the **trace** and confirm **both** specialists were called.

## 🟡 Builder — notebook
Open **`lab4_multiagent.ipynb`**: define the agents, expose each specialist as a **function tool** the
orchestrator calls (delegation), run the compound query, and print the call chain.
*(Pattern: azure-ai-projects 2.x → `tools/sample_agent_function_tool.py` &
`sample_workflow_multi_agent.py`.)*

## 🔴 Engineer — SDK
Complete **`lab4_multiagent.py`**: expose the two specialists as function tools, delegate from the
orchestrator, and `assert` that the compound query produces **≥2** specialist tool-calls.

```python
# specialists exposed as function tools; handlers forward each question to a specialist agent
out, trace = run_with_trace(
    orchestrator, PROMPTS["follow_up_and_diet"]["text"],
    functions={"ask_education": ask_education, "ask_followup": ask_followup},
)
specialist_calls = [c for c in trace.tool_calls if c.name in ("ask_education", "ask_followup")]
assert len(specialist_calls) >= 2, [c.name for c in trace.tool_calls]
```
> **Go further (Engineer):** re-implement as a **Workflow agent** (`WorkflowAgentDefinition`) or with
> the **Microsoft Agent Framework** (`FoundryChatClient` + workflows) for code-first orchestration.

---

## ✅ Validation
Paste the orchestrator's reply **and** a screenshot (or `tool_calls` count) from the trace.
Passes when the compound query invoked **≥2 specialist agents** and the reply addresses both
appointments and diet. **(300 pts · badge 🎛️ Orchestrator)**

## 🎁 Bonus (+50)
Add a **third** specialist — **Assessment** (monitors / tracks symptoms) or **Enrollment & Linkage**
(explains programs, checks eligibility) — and show it firing on an appropriate question.

## Stuck?
- Only one specialist fires? Make the routing rule explicit and ensure **both** specialists are
  attached as connected tools on the orchestrator.
- Specialists loop or over-call? Add "Call only the specialists needed" and cap with the routing rule.
