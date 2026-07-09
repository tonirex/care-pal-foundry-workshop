"""Lab 4 (Engineer) — Multi-Agent Care Pal: CONCURRENT orchestration (Microsoft Agent Framework).

Instead of chaining agents in a pipeline, this rail fans the caregiver's compound question out to
three specialists that answer **in parallel** with the Microsoft Agent Framework's `ConcurrentBuilder`,
then aggregates their replies:

                  +-> triage     (intent / risk / route -- the safety read)
    question  ----+-> education  (diet / self-care guidance)
                  +-> follow-up  (appointments / check-ins)

- **triage**     classifies the message (intent / risk / route) — the safety read.
- **education**  answers the *diet / self-care* half of the question.
- **follow-up**  answers the *appointments / check-ins* half of the question.

Every participant sees the SAME question and answers independently (no ordering, no shared running
conversation), so you get diverse perspectives in one shot. The framework's default aggregator collects
all three replies into a single AgentResponse — one assistant message per agent. This mirrors the
Microsoft Learn "Concurrent orchestration" exercise, applied to Care Pal.

--- Client-side agents (no permanent Foundry agent) --------------------------------------------
The participants are built with `chat_client.as_agent(...)`, which creates **in-process, client-side**
agents: plain Python objects binding the shared FoundryChatClient to a name + instructions. This rail
never calls `project.agents.create_version(PromptAgentDefinition(...))`, so — unlike Lab 1 — it does
NOT register a versioned Prompt Agent in the Foundry project. The fan-out/aggregate runs locally in the
Agent Framework; each agent.run() is a stateless Responses API call to the model deployment. The only
Foundry resource used is model inference, and the agents vanish when the process exits (nothing to
delete, no cleanup()).

Run:  `python lab4_multiagent_concurrent.py`  (after `az login`)

Lab instructions: ../labs/lab-04.md (all three rails) · portal walkthrough: ../labs/lab-04-portal.md

Docs: Microsoft Agent Framework — https://learn.microsoft.com/en-us/agent-framework/ ·
concurrent orchestration:
https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/concurrent?pivots=programming-language-python
"""
# %%
# --- make `common` importable whether run as a script or a notebook ---
import sys
import pathlib

_here = (pathlib.Path(globals()["__file__"]).resolve().parent
         if "__file__" in globals() else pathlib.Path.cwd())
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
import asyncio
import os
from typing import cast

# Microsoft Agent Framework — concurrent orchestration over a Foundry project.
from agent_framework import AgentResponse, Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import ConcurrentBuilder
from azure.identity import AzureCliCredential

# Reuse the workshop's canned compound prompt (also loads a local .env, if present).
from common.carepal_common import text_of

# --------------------------------------------------------------------- agent instructions
# Plain-language instructions (no forced JSON) so each parallel answer reads cleanly on its own.
TRIAGE_INSTRUCTIONS = """
You are Care Pal's triage agent for discharged heart/kidney/liver patients in Singapore and their
caregivers. You are not a doctor and cannot diagnose. Read the caregiver's message and classify it in
2-3 short lines only:
- intent (e.g. follow_up, self_care_education, symptom_report)
- risk_level: low | medium | high  (chest pain, severe breathlessness, fainting, stroke signs -> high)
- route: education_navigation | timely_review | immediate_escalation | clarification
Do NOT answer the question yourself. You only classify; the education and follow-up specialists answer
in parallel, independently of you. Keep it brief and plain.
"""

EDUCATION_INSTRUCTIONS = """
You are Care Pal's education specialist. For the caregiver's message, give brief, plain-language
self-care and DIET guidance for a discharged heart-failure patient (e.g. low-salt and fluid guidance,
weight monitoring, what to watch for). You are not a doctor and do not diagnose. 2-4 short sentences.
Do NOT cover appointment scheduling — that is the follow-up specialist's job.
"""

FOLLOWUP_INSTRUCTIONS = """
You are Care Pal's follow-up specialist. For the caregiver's message, suggest the follow-up
APPOINTMENTS and check-ins a discharged heart-failure patient typically needs (e.g. cardiology review,
GP/polyclinic follow-up, medication review, nurse symptom check-ins). You do not diagnose. 2-4 short
sentences focused on scheduling and next steps.
"""


# %%
async def main():
    # Create the chat client (authenticate with `az login`; FoundryChatClient talks to your project).
    credential = AzureCliCredential()
    chat_client = FoundryChatClient(
        credential=credential,
        project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
        model=os.getenv("FOUNDRY_MODEL_NAME"),
    )

    # 👉 Create the three participants (name + instructions). `as_agent` builds CLIENT-SIDE agents:
    #    each is just an in-process object binding this chat client to a name + system prompt. Nothing
    #    is registered in the Foundry project (no create_version / PromptAgentDefinition), so there are
    #    NO server-side agent versions to delete afterwards. (See the note at the end of main.)
    triage_agent = chat_client.as_agent(name="triage", instructions=TRIAGE_INSTRUCTIONS)
    education_agent = chat_client.as_agent(name="education", instructions=EDUCATION_INSTRUCTIONS)
    followup_agent = chat_client.as_agent(name="followup", instructions=FOLLOWUP_INSTRUCTIONS)

    # The compound caregiver question (same canned prompt every rail uses).
    question = text_of("follow_up_and_diet")

    # 👉 Build the CONCURRENT orchestration. Every participant receives the SAME question and runs in
    #    parallel (fan-out); the default aggregator fans their replies back into a single AgentResponse
    #    with one assistant message per participant. No ordering, no shared running conversation.
    workflow = ConcurrentBuilder(
        participants=[triage_agent, education_agent, followup_agent],
    ).build()

    # Run the fan-out/aggregate workflow and collect the aggregated result.
    result = await workflow.run(question)
    outputs = result.get_outputs()

    # Display every participant's parallel answer. The default aggregator returns a single
    # AgentResponse (outputs[0]); we iterate defensively over all outputs and their messages.
    print(f"=== Care Pal concurrent fan-out ===\nQ: {question}\n")
    i = 1
    seen: list[str] = []
    for response in cast(list[AgentResponse], outputs):
        for msg in cast(list[Message], response.messages):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
            if name not in seen:
                seen.append(name)
            i += 1

    # Validation: both specialists answered in parallel, so the fan-out covers diet AND appointments.
    specialists = {"education", "followup"}
    assert specialists <= set(seen), f"expected both specialists to run, got {seen}"
    print("\nLab 4 passed ✅")

    # --- Why there is nothing to clean up (client-side agents) ----------------------------------
    # The three participants were created with chat_client.as_agent(...), which registers NOTHING in
    # the Foundry project. Contrast Lab 1's common.create_agent(), which calls
    # project.agents.create_version(PromptAgentDefinition(...)) and persists a versioned Prompt Agent
    # server-side (and therefore needs cleanup() / delete_version). Here each agent is an in-process
    # object; ConcurrentBuilder does the fan-out/aggregate locally and each agent.run() is a stateless
    # Responses API call to the model deployment. The agents exist only for this process — nothing to
    # delete, no server-side footprint beyond model inference.
    #
    # GO FURTHER (Engineer): add `.with_aggregator(...)` to synthesize the three answers into one
    #   caregiver-ready reply, or pass `intermediate_output_from=[...]` to stream each specialist as it
    #   finishes. Or try a Handoff / Magentic pattern for dynamic routing. See the concurrent doc above.


if __name__ == "__main__":
    asyncio.run(main())
