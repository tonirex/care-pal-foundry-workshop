# 🩺 Lab 4 · Multi-Agent Care Pal — Orchestration

**⏱️ 50 min**  ·  **👥 Everyone (builders & engineers go deeper)**  ·  **📊 L300**  ·  **🧩 Multi-agent orchestration, Workflows, Function tools**

**🧭 You are here:** [Lab 0](lab-00.md) · [Lab 1](lab-01.md) · [Lab 2](lab-02.md) · [Lab 3](lab-03.md) · **▸ Lab 4** · [Lab 5](lab-05.md)  ·  🏠 [Workshop home](../../README.md)

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

> **📂 This lab, three ways — pick your rail:**
> 🟢 **Navigator** (portal, screenshots): **[lab-04-portal.md](lab-04-portal.md)** · 🟡 **Builder** (notebook): **[`lab4_multiagent.ipynb`](../assets/lab4_multiagent.ipynb)** · 🔴 **Engineer** (script): **[`lab4_multiagent.py`](../assets/lab4_multiagent.py)**

> Required today: **Education** + **Follow-Up** (plus your triage orchestrator). Navigation /
> Assessment / Enrollment are optional extras.

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
Open **[`lab4_multiagent.ipynb`](../assets/lab4_multiagent.ipynb)** and run it top to bottom — the markdown cells explain the orchestrator
+ two specialists, the function-tool loop, and a "three ways to orchestrate" comparison. It defines the
agents, exposes each specialist as a **function tool** the orchestrator calls (delegation), runs the
compound query, **logs each hand-off**, and prints the synthesised reply and the tool-call chain.

**Under the hood:** the specialists are exposed with `function_tool(...)` (a `FunctionTool` on the
orchestrator's definition). `run_with_trace(...)` runs the model, catches each `function_call` Foundry
emits, invokes the matching specialist, and feeds the result back with `previous_response_id` until the
orchestrator returns one merged JSON.

📚 **Docs:** [Function calling / tools](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/function-calling) ·
[Connected agents (multi-agent)](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/connected-agents) ·
samples: [`sample_agent_function_tool.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_function_tool.py), [`sample_workflow_multi_agent.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_workflow_multi_agent.py)

## 🔴 Engineer — SDK
Run **[`lab4_multiagent.py`](../assets/lab4_multiagent.py)** and fill the `# 👉` lines. The goal: wire
**three agents** into a **sequential pipeline** with the **Microsoft Agent Framework**
(`SequentialBuilder`) so the compound question flows `triage → education → follow-up`, then `assert`
that **both specialists** contributed to the collected outputs.

This rail follows Microsoft Learn's **[Develop a multi-agent solution with Microsoft Agent
Framework](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/08-agent-framework-multi-agents.html)**
(Summarizer → Classifier → Action), applied to Care Pal. It needs the `agent-framework` package
(`pip install -r requirements.txt`) and `az login`.

**The SDK flow:**
1. **Create the chat client** — `FoundryChatClient(project_endpoint=…, model=…, credential=AzureCliCredential())`
   connects the Agent Framework to your Foundry project.
2. **Create three agents** — `chat_client.as_agent(name=…, instructions=…)` for `triage`, `education`
   and `followup`. These are in-process agents (no server-side versions to clean up afterwards).
3. **Build + run the pipeline** — `SequentialBuilder(participants=[…], output_from="all").build()` runs
   the agents **in order over one shared conversation**. `output_from="all"` collects every agent's
   message (not just the last), and `result.get_outputs()` returns them.

```python
# three agents run in order, sharing the conversation; output_from="all" keeps every reply
workflow = SequentialBuilder(
    participants=[triage_agent, education_agent, followup_agent],
    output_from="all",
).build()
result = await workflow.run(text_of("follow_up_and_diet"))
outputs = result.get_outputs()
seen = [m.author_name for r in outputs for m in r.messages]
assert {"education", "followup"} <= set(seen), seen   # both specialists contributed
```
> **Why sequential (not tools)?** No hand-written function-call loop and no orchestrator prompt — the
> builder wires the chain and passes the shared conversation between agents. Each agent sees the prior
> replies and adds its piece: triage classifies, education covers diet, follow-up covers appointments.
> **Go further:** swap `SequentialBuilder` for `ConcurrentBuilder` (specialists answer in parallel, then
> aggregate) or a Handoff / Magentic pattern for dynamic routing.

📚 **Docs:** [Microsoft Agent Framework](https://learn.microsoft.com/en-us/agent-framework/) ·
lab: [08 · multi-agent with Agent Framework](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/08-agent-framework-multi-agents.html) ·
sample: [`sequential_workflow_as_agent.py`](https://github.com/microsoft/agent-framework/blob/main/python/samples/03-workflows/agents/sequential_workflow_as_agent.py)

---

## ✅ Validation
Paste the orchestrator's reply **and** a screenshot (or `tool_calls` count) from the trace.
Passes when the compound query invoked **≥2 specialist agents** and the reply addresses both
appointments and diet.

## 🎁 Optional challenge
Add a **third** specialist — **Assessment** (monitors / tracks symptoms) or **Enrollment & Linkage**
(explains programs, checks eligibility) — and show it firing on an appropriate question.

## Stuck?
- Only one specialist fires? Make the routing rule explicit and ensure **both** specialists are
  attached as connected tools on the orchestrator.
- Specialists loop or over-call? Add "Call only the specialists needed" and cap with the routing rule.

---

### 🧭 Where next?
⬅️ Previous: [Lab 3 · Govern & Observe](lab-03.md) — 🏠 [Workshop flow & rails](../../README.md#how-the-workshop-flows) — Next: [Lab 5 · Extend & Deploy](lab-05.md) ➡️

> 🟢 **Navigator?** Screenshot walkthrough for this lab: **[lab-04-portal.md](lab-04-portal.md)** · index: [PORTAL-TRACK.md](PORTAL-TRACK.md)
