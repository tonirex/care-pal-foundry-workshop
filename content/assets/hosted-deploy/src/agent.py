"""Care Pal hosted agent — entry point (Lab 5, Part B).

Standalone on purpose: it does NOT import the workshop `common` package, so this folder can be
deployed by itself via the VS Code **Microsoft Foundry** toolkit
("Deploy to Microsoft Foundry" -> Code (Remote)) or `azd up`.

Targets the current Foundry agents API (azure-ai-projects >= 2.0):
    project.agents.create_version(definition=PromptAgentDefinition(... text=structured output ...))
    project.get_openai_client().responses.create(input=..., extra_body={"agent_reference": ...})

Run locally to create/update the Care Pal triage agent in the target project:
    python agent.py
    # set CAREPAL_SMOKE_TEST=1 to also send one sample message
"""
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    PromptAgentDefinitionTextOptions,
    TextResponseFormatJsonSchema,
)
from azure.identity import DefaultAzureCredential

MODEL = os.environ.get("FOUNDRY_MODEL_NAME") or os.environ.get("MODEL_DEPLOYMENT", "model-router")
AGENT_NAME = os.environ.get("AGENT_NAME", "carepal-hosted")

TRIAGE_INSTRUCTIONS = """\
You are Care Pal, a post-discharge assistant for heart/kidney/liver patients in Singapore and their
caregivers. You are not a doctor, cannot diagnose, and cannot contact a care team.

For EVERY user message, respond ONLY with a JSON object with these keys:
intent, risk_level, route, reply, source_labels, source_urls, clarifying_questions.

Routing by risk:
- red-flag symptoms (chest pain, severe breathlessness, fainting, confusion, stroke signs, self-harm)
  -> route "immediate_escalation"; reply tells the user to call 995 / go to A&E; never diagnose.
- worsening / complex / medication-safety -> route "timely_review".
- stable, general, education or navigation -> route "education_navigation".
- not enough information -> route "clarification" with 1-3 clarifying_questions.
Output JSON only - no text outside the JSON.
"""

TRIAGE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["intent", "risk_level", "route", "reply",
                 "source_labels", "source_urls", "clarifying_questions"],
    "properties": {
        "intent": {"type": "string", "enum": [
            "greeting", "unclear", "self_care_education", "symptom_report",
            "medication_question", "navigation_request", "follow_up", "enrollment_query"]},
        "risk_level": {"type": "string", "enum": ["unclear", "low", "medium", "high"]},
        "route": {"type": "string", "enum": [
            "clarification", "education_navigation", "timely_review", "immediate_escalation"]},
        "reply": {"type": "string"},
        "source_labels": {"type": "array", "items": {"type": "string"}},
        "source_urls": {"type": "array", "items": {"type": "string"}},
        "clarifying_questions": {"type": "array", "items": {"type": "string"}},
    },
}


def get_project():
    endpoint = os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or os.environ.get("PROJECT_ENDPOINT")
    if not endpoint:
        raise RuntimeError("Set FOUNDRY_PROJECT_ENDPOINT (see .env.example).")
    return AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())


def ensure_agent(project=None):
    """Create (version) the Care Pal triage agent with structured output."""
    project = project or get_project()
    agent = project.agents.create_version(
        agent_name=AGENT_NAME,
        definition=PromptAgentDefinition(
            model=MODEL,
            instructions=TRIAGE_INSTRUCTIONS,
            text=PromptAgentDefinitionTextOptions(
                format=TextResponseFormatJsonSchema(name="care_pal_triage", schema=TRIAGE_SCHEMA)
            ),
        ),
    )
    print(f"Created/updated agent {agent.name} (version {agent.version}, id {agent.id})")
    return agent


def smoke_test(project, agent):
    """Optional: send one message and print the structured reply."""
    openai = project.get_openai_client()
    resp = openai.responses.create(
        input="I was just discharged after heart failure. What can I eat?",
        extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
    )
    print("Sample reply:", resp.output_text)


if __name__ == "__main__":
    proj = get_project()
    a = ensure_agent(proj)
    if os.environ.get("CAREPAL_SMOKE_TEST"):
        smoke_test(proj, a)
