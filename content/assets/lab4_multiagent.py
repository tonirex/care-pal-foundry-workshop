"""Lab 4 (Engineer) — Multi-Agent Care Pal: SEQUENTIAL orchestration (Microsoft Agent Framework).

Instead of one orchestrator that delegates via function tools, this rail wires three agents into a
**sequential pipeline** with the Microsoft Agent Framework's `SequentialBuilder`. The caregiver's
compound question flows through the chain, and each agent adds its piece to the shared conversation:

    triage  ->  education  ->  follow-up

- **triage**     classifies the message (intent / risk / route) — the safety gate.
- **education**  answers the *diet / self-care* half of the question.
- **follow-up**  answers the *appointments / check-ins* half of the question.

`output_from="all"` collects every participant's message, so you SEE the whole pipeline (not just the
last reply). This mirrors the Microsoft Learn exercise "Develop a multi-agent solution with Microsoft
Agent Framework" (Summarizer -> Classifier -> Action), applied to Care Pal.

Run:  `python lab4_multiagent.py`  (after `az login`)

Lab instructions: ../labs/lab-04.md (all three rails) · portal walkthrough: ../labs/lab-04-portal.md

Docs: Microsoft Agent Framework — https://learn.microsoft.com/en-us/agent-framework/ ·
sequential orchestration sample:
https://github.com/microsoft/agent-framework/blob/main/python/samples/03-workflows/agents/sequential_workflow_as_agent.py
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

# Microsoft Agent Framework — sequential orchestration over a Foundry project.
from agent_framework import Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential

# Reuse the workshop's canned compound prompt (also loads a local .env, if present).
from common.carepal_common import text_of

# --------------------------------------------------------------------- agent instructions
# Plain-language instructions (no forced JSON) so the pipeline reads cleanly stage by stage.
TRIAGE_INSTRUCTIONS = """
You are Care Pal's triage agent for discharged heart/kidney/liver patients in Singapore and their
caregivers. You are not a doctor and cannot diagnose. Read the caregiver's message and classify it in
2-3 short lines only:
- intent (e.g. follow_up, self_care_education, symptom_report)
- risk_level: low | medium | high  (chest pain, severe breathlessness, fainting, stroke signs -> high)
- route: education_navigation | timely_review | immediate_escalation | clarification
Do NOT answer the question yourself — the specialists after you will. Keep it brief and plain.
"""

EDUCATION_INSTRUCTIONS = """
You are Care Pal's education specialist. Using the triage read above, give brief, plain-language
self-care and DIET guidance for a discharged heart-failure patient (e.g. low-salt and fluid guidance,
weight monitoring, what to watch for). You are not a doctor and do not diagnose. 2-4 short sentences.
Do NOT cover appointment scheduling — that is the follow-up specialist's job.
"""

FOLLOWUP_INSTRUCTIONS = """
You are Care Pal's follow-up specialist. Using the conversation above, suggest the follow-up
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

    # 👉 Create the three participants (name + instructions). These are in-process agents — no
    #    server-side versions to clean up afterwards.
    triage_agent = chat_client.as_agent(name="triage", instructions=TRIAGE_INSTRUCTIONS)
    education_agent = chat_client.as_agent(name="education", instructions=EDUCATION_INSTRUCTIONS)
    followup_agent = chat_client.as_agent(name="followup", instructions=FOLLOWUP_INSTRUCTIONS)

    # The compound caregiver question (same canned prompt every rail uses).
    question = text_of("follow_up_and_diet")

    # 👉 Build the sequential orchestration. Participants run in the order given; output_from="all"
    #    collects each participant's message so you can see the whole pipeline, not just the last reply.
    workflow = SequentialBuilder(
        participants=[triage_agent, education_agent, followup_agent],
        output_from="all",
    ).build()

    # Run the pipeline and collect the outputs from every agent.
    result = await workflow.run(question)
    outputs = result.get_outputs()

    # Display each stage of the pipeline.
    print(f"=== Care Pal sequential pipeline ===\nQ: {question}\n")
    i = 1
    seen: list[str] = []
    for response in outputs:
        for msg in cast(list[Message], response.messages):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n{i:02d} [{name}]\n{msg.text}")
            if name not in seen:
                seen.append(name)
            i += 1

    # Validation: both specialists contributed, so the reply covers appointments AND diet.
    specialists = {"education", "followup"}
    assert specialists <= set(seen), f"expected both specialists to run, got {seen}"
    print("\nLab 4 passed ✅")

    # TODO (bonus): add a fourth participant — Assessment (symptom tracking) or Enrollment & Linkage
    #   (programs / eligibility) — and show it firing in the pipeline.
    # GO FURTHER (Engineer): swap SequentialBuilder for ConcurrentBuilder (specialists answer in
    #   parallel, then aggregate) or a Handoff/Magentic pattern for dynamic routing. See the
    #   agent-framework orchestrations samples.


if __name__ == "__main__":
    asyncio.run(main())
