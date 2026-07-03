---
id: lab-01
title: "Lab 1: Triage Agent — Understand, Classify, Route"
duration_minutes: 45
audience: ["Everyone"]
foundry_capabilities: ["Instructions design", "Structured outputs", "Model selection"]
order: 1
is_active: false
max_points: 300
bonus_quest: true
rails: ["navigator", "builder", "engineer"]
tier: "L200"
---

> 🩺 **Mr. Rajan — Chapter 1**
> Two days home, Rajan writes: *"I was discharged recently for heart failure."* It's vague — is he
> worried about symptoms, medication, diet? Care Pal can't act safely until it understands the
> **intent**, gauges the **risk**, and decides a **route**. This is where a friendly chatbot becomes
> a triage agent.

## What you'll learn
A reply humans can read isn't enough — software needs a reply it can **act on**. You'll make Care Pal
return **structured JSON** every turn, and design instructions that route a message by clinical risk.

## The triage contract (shared by every rail)
Your agent must return **only** this JSON object:

```jsonc
{
  "intent": "self_care_education",   // greeting | unclear | self_care_education | symptom_report | medication_question | navigation_request | follow_up | enrollment_query
  "risk_level": "low",               // unclear | low | medium | high
  "route": "education_navigation",   // clarification | education_navigation | timely_review | immediate_escalation
  "reply": "…",                      // short, safe, plain-language message to the user
  "source_labels": [],               // filled in Lab 2
  "source_urls": [],                 // filled in Lab 2
  "clarifying_questions": []          // 1–3 questions when route = clarification
}
```

**Routing rules:**
| If the message is… | risk_level | route |
|--------------------|-----------|-------|
| Red-flag (chest pain, severe breathlessness, fainting, confusion, stroke signs, self-harm) | high | `immediate_escalation` |
| Worsening / complex / no improvement / medication-safety | medium | `timely_review` |
| Stable, general, education or navigation question | low | `education_navigation` |
| Not enough info / unclear intent | unclear | `clarification` (+ ask 1–3 questions) |

## Demo (facilitator, 5 min)
Send the verbatim customer line *"I was discharged recently for kidney failure."* → show the JSON
comes back with `route: "clarification"` and good `clarifying_questions`. That single structured
field is what lets downstream software escalate, ground, or hand off.

---

## 🟢 Navigator — portal
1. Open your `carepal-<initials>` agent → **Configure**.
2. Replace the Instructions with the **Triage block**:

```text
You are Care Pal's triage agent for discharged heart/kidney/liver patients in Singapore and their
caregivers. You are not a doctor, cannot diagnose, and cannot contact a care team.

For EVERY user message, respond ONLY with a JSON object with these keys:
intent, risk_level, route, reply, source_labels, source_urls, clarifying_questions.

- intent: greeting | unclear | self_care_education | symptom_report | medication_question |
  navigation_request | follow_up | enrollment_query
- risk_level: unclear | low | medium | high
- route, by risk:
    high / red-flag symptoms (chest pain, severe breathlessness, fainting, confusion, stroke signs,
      self-harm) -> "immediate_escalation"
    worsening or complex symptoms, no improvement, medication-safety questions -> "timely_review"
    stable, general, education or navigation questions -> "education_navigation"
    not enough information or unclear intent -> "clarification"
- reply: short, safe, plain language. Never diagnose. For high risk, tell them to call 995 / go to A&E.
- source_labels / source_urls: empty arrays for now (added in Lab 2).
- clarifying_questions: 1–3 questions when route is "clarification" or key info is missing; else [].
Output JSON only — no text outside the JSON.
```

3. Turn on **Output format → JSON / structured output**. If a schema box is offered, paste
   `content/answer-keys/_schema.json` (your facilitator shares it on screen).
4. **Chat** → send each test message and copy the JSON:
   - `What diet should my father follow after heart failure?`
   - `My father's ankles look a little more swollen than yesterday, but he feels okay otherwise.`
   - `I have crushing chest pain and I can't breathe properly.`

   > 📋 Full set of canonical test cases (with expected `intent` / `risk_level` / `route`):
   > [`content/prompts/test-prompts.json`](../prompts/test-prompts.json)

## 🟡 Builder — notebook
Open **`lab1_triage.ipynb`**. Fill the `instructions=` blank (the Triage block) and keep
`structured=True` — that pins the 7-key JSON via the agent's structured-output schema — then run the
cell that loops the three test messages and prints each `route`.
*(Pattern: azure-ai-projects 2.x → `samples/agents/sample_agent_structured_output.py`.)*

## 🔴 Engineer — SDK
Complete **`lab1_triage.py`**: create the agent with a JSON-schema for structured output, then
`assert` the route for all three inputs. *(Pattern: prompt-agent quickstart + structured output via
`PromptAgentDefinition.text`.)*

```python
# excerpt — fill the TODOs (this is what make_triage_agent(structured=True) does under the hood)
from azure.ai.projects.models import (
    PromptAgentDefinition, PromptAgentDefinitionTextOptions, TextResponseFormatJsonSchema,
)

agent = project.agents.create_version(
    agent_name=f"carepal-{INITIALS}",
    definition=PromptAgentDefinition(
        model=os.environ["FOUNDRY_MODEL_NAME"],          # model-router
        instructions=TRIAGE_INSTRUCTIONS,                # TODO: paste the Triage block
        text=PromptAgentDefinitionTextOptions(           # TODO: pin the 7-key JSON
            format=TextResponseFormatJsonSchema(name="care_pal_triage", schema=TRIAGE_SCHEMA)
        ),
    ),
)
# run via the OpenAI-compatible client; run_and_parse() wraps responses.create(... agent_reference)
for pid in ["diet_question", "swelling_worsening", "chest_pain"]:
    out = run_and_parse(agent, PROMPTS[pid]["text"])
    assert out["route"] == PROMPTS[pid]["expected"]["route"], out
```

---

## ✅ Validation
Paste the JSON your agent returned for **"I have crushing chest pain and I can't breathe properly."**
Passes when **all 7 keys are present** *and* **`route == "immediate_escalation"`**.
You earn points for each of the three messages routed correctly. **(300 pts · badge 🧠 Prompt Engineer)**

## 🎁 Bonus (+50)
Add a new `intent` value — `medication_question` — and show that *"Can my father take his water
pill in the morning instead of at night?"* routes to `timely_review`.

## Stuck?
- Getting prose, not JSON? Ensure **Output format = JSON** is on **and** the instructions say
  "Output JSON only".
- `swelling` keeps going to `immediate_escalation`? Your red-flag list is too broad — swelling alone,
  patient "okay otherwise", is **medium / timely_review**.
