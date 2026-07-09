"""Care Pal workshop — shared helpers (Builder + Engineer rails).

One place that talks to Microsoft Foundry Agent Service (the *new* agents API,
``azure-ai-projects >= 2.0``) so the lab files stay short. Standardises on the
current Foundry flow:

    project.agents.create_version(definition=PromptAgentDefinition(...))   # define + version
    openai = project.get_openai_client()                                  # OpenAI-compatible client
    openai.responses.create(input=..., extra_body={"agent_reference": ...})  # run, read .output_text

This is the same backend the Foundry portal drives, so a Navigator's portal agent
and an Engineer's SDK agent are the *same* object.

Env (.env or shell):
    FOUNDRY_PROJECT_ENDPOINT   https://<account>.services.ai.azure.com/api/projects/<project>
    FOUNDRY_MODEL_NAME         model deployment name (default: model-router)
    INITIALS                   your initials -> agents named carepal-<initials>
Auth: run `az login` first (DefaultAzureCredential).
"""
from __future__ import annotations

import functools
import json
import os
import pathlib
import re
from dataclasses import dataclass, field

try:  # optional: load a local .env if python-dotenv is installed
    from dotenv import load_dotenv

    load_dotenv()
except Exception:  # pragma: no cover
    pass

# --------------------------------------------------------------------------- paths
HERE = pathlib.Path(__file__).resolve()
ASSETS = HERE.parents[1]          # .../content/assets
CONTENT = HERE.parents[2]         # .../content
KNOWLEDGE = CONTENT / "knowledge"

# --------------------------------------------------------------------------- config
# Accept the current FOUNDRY_* names (official samples) and the older names for resilience.
MODEL = os.environ.get("FOUNDRY_MODEL_NAME") or os.environ.get("MODEL_DEPLOYMENT", "model-router")
INITIALS = os.environ.get("INITIALS", "xx")


def _endpoint() -> str:
    ep = os.environ.get("FOUNDRY_PROJECT_ENDPOINT") or os.environ.get("PROJECT_ENDPOINT")
    if not ep:
        raise RuntimeError(
            "Set FOUNDRY_PROJECT_ENDPOINT in your environment or .env (see .env.example)."
        )
    return ep


def agent_name(suffix: str = "") -> str:
    base = f"carepal-{INITIALS}"
    return f"{base}-{suffix}" if suffix else base


# --------------------------------------------------------------------- source of truth
def _load_json(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


PROMPTS: dict = _load_json(CONTENT / "prompts" / "test-prompts.json")["prompts"]
TRIAGE_SCHEMA: dict = _load_json(CONTENT / "answer-keys" / "_schema.json")["schema"]


def text_of(prompt_id: str) -> str:
    """The verbatim user message for a canned prompt id."""
    return PROMPTS[prompt_id]["text"]


def route_of(prompt_id: str) -> str | None:
    """The expected `route` for a canned prompt id (None if not asserted)."""
    return PROMPTS[prompt_id]["expected"].get("route")


# --------------------------------------------------------------------- evaluation set
EVAL_DATASET = ASSETS / "carepal-eval-dataset.jsonl"


def _route_from_context(ctx: str | None) -> str | None:
    """Pull the expected route token out of a dataset `context` field.

    Accepts the jsonl form ("route=immediate_escalation; risk=high") and the
    csv form (a bare token like "immediate_escalation").
    """
    if not ctx:
        return None
    match = re.search(r"route=([a-z_]+)", ctx)
    return match.group(1) if match else (ctx.strip() or None)


def load_eval_dataset(path=None) -> list:
    """Load the Care Pal eval set as rows of {query, ground_truth, route}.

    Defaults to ``carepal-eval-dataset.jsonl`` in assets/; pass a .csv to use that form
    instead. This is the *same* 10-case set the portal rail uploads, so every rail scores
    against identical prompts. Pure file read — no Azure needed to enumerate the cases.
    """
    p = pathlib.Path(path) if path else EVAL_DATASET
    if not p.is_absolute() and not p.exists():
        p = ASSETS / p
    rows: list = []
    if p.suffix.lower() == ".csv":
        import csv as _csv

        with open(p, encoding="utf-8", newline="") as fh:
            for d in _csv.DictReader(fh):
                rows.append(
                    {
                        "query": d["query"],
                        "ground_truth": d.get("ground_truth", ""),
                        "route": _route_from_context(d.get("context")),
                    }
                )
    else:
        with open(p, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                rows.append(
                    {
                        "query": d["query"],
                        "ground_truth": d.get("ground_truth", ""),
                        "route": _route_from_context(d.get("context")),
                    }
                )
    if not rows:
        raise RuntimeError(f"No rows loaded from {p}")
    return rows


REQUIRED_KEYS = [
    "intent",
    "risk_level",
    "route",
    "reply",
    "source_labels",
    "source_urls",
    "clarifying_questions",
]

# The triage instruction block (kept identical to content/labs/lab-01.md).
TRIAGE_INSTRUCTIONS = """\
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
- source_labels / source_urls: empty arrays unless you grounded the answer in a real source.
- clarifying_questions: 1-3 questions when route is "clarification" or key info is missing; else [].
Output JSON only - no text outside the JSON.
"""


# --------------------------------------------------------------------- SDK plumbing (new API)
@functools.lru_cache(maxsize=1)
def get_project():
    """Authenticated AIProjectClient for the shared workshop project (cached).

    `allow_preview=True` enables preview surfaces (e.g. Workflow agents used in the
    Lab 4 "go further" note); it is harmless for the GA features the labs rely on.
    """
    from azure.ai.projects import AIProjectClient
    from azure.identity import DefaultAzureCredential

    try:
        return AIProjectClient(
            endpoint=_endpoint(), credential=DefaultAzureCredential(), allow_preview=True
        )
    except TypeError:  # older 2.x without allow_preview kwarg
        return AIProjectClient(endpoint=_endpoint(), credential=DefaultAzureCredential())


@functools.lru_cache(maxsize=1)
def get_openai():
    """OpenAI-compatible client for conversations + responses (new API)."""
    return get_project().get_openai_client()


def _models():
    """The new agents model classes (azure-ai-projects >= 2.0)."""
    import azure.ai.projects.models as m

    return m


# --------------------------------------------------------------------- agents
def triage_text_format():
    """`PromptAgentDefinition.text` that pins the 7-key triage JSON (structured output).

    In the new API, structured output lives on the agent definition via
    PromptAgentDefinitionTextOptions(format=TextResponseFormatJsonSchema(...)).
    """
    m = _models()
    return m.PromptAgentDefinitionTextOptions(
        format=m.TextResponseFormatJsonSchema(name="care_pal_triage", schema=TRIAGE_SCHEMA)
    )


def create_agent(name, instructions, tools=None, structured=False, description=None):
    """Create (version) a Prompt agent in the shared project; returns the agent version object."""
    m = _models()
    kwargs = dict(model=MODEL, instructions=instructions)
    if tools:
        kwargs["tools"] = list(tools)
    if structured:
        kwargs["text"] = triage_text_format()
    definition = m.PromptAgentDefinition(**kwargs)
    create_kwargs = dict(agent_name=name, definition=definition)
    if description:
        create_kwargs["description"] = description
    return get_project().agents.create_version(**create_kwargs)


def make_triage_agent(name=None, instructions=None, tools=None, structured=True):
    """Create the Care Pal triage agent (structured output on by default)."""
    return create_agent(
        name=name or agent_name(),
        instructions=instructions or TRIAGE_INSTRUCTIONS,
        tools=tools,
        structured=structured,
    )


def agent_reference(agent) -> dict:
    """The `agent_reference` payload that binds a response to an agent (goes in extra_body)."""
    return {"name": agent.name, "type": "agent_reference"}


# --------------------------------------------------------------------- run + parse
def run_text(agent, text: str) -> str:
    """Single-turn: send `text` to `agent`, return the assistant's output text."""
    resp = get_openai().responses.create(
        input=text,
        extra_body={"agent_reference": agent_reference(agent)},
    )
    return resp.output_text


_JSON_RE = re.compile(r"\{.*\}", re.S)


def extract_json(text: str) -> dict:
    """Parse the triage JSON from an assistant reply (tolerates stray prose)."""
    try:
        return json.loads(text)
    except Exception:
        match = _JSON_RE.search(text or "")
        if not match:
            raise ValueError(f"No JSON object found in reply: {text!r}")
        return json.loads(match.group(0))


def run_and_parse(agent, text: str) -> dict:
    """Send `text` to `agent`, return the parsed triage JSON object."""
    return extract_json(run_text(agent, text))


@dataclass
class ToolCall:
    name: str


@dataclass
class Trace:
    tool_calls: list = field(default_factory=list)
    response: object = None


def run_with_trace(agent, text: str, functions=None):
    """Run with a manual function-tool loop and capture which tools fired.

    `functions` maps a FunctionTool name -> a Python callable. Server-side tools
    (File Search, or MCP with require_approval="never") run automatically and need
    no handler. Returns (parsed_json, Trace) where Trace.tool_calls lists the
    function tools the agent invoked — handy for asserting delegation in Lab 4.
    """
    functions = functions or {}
    openai = get_openai()
    ref = {"agent_reference": agent_reference(agent)}
    response = openai.responses.create(input=text, extra_body=ref)
    calls: list = []
    for _ in range(6):  # cap the tool-call loop
        fcalls = [it for it in response.output if getattr(it, "type", None) == "function_call"]
        if not fcalls:
            break
        outputs = []
        for it in fcalls:
            calls.append(ToolCall(name=it.name))
            handler = functions.get(it.name)
            try:
                args = json.loads(it.arguments or "{}")
            except Exception:
                args = {}
            result = handler(**args) if handler else {"error": f"no handler for {it.name}"}
            if not isinstance(result, str):
                result = json.dumps(result)
            outputs.append(
                {"type": "function_call_output", "call_id": it.call_id, "output": result}
            )
        response = openai.responses.create(
            input=outputs, previous_response_id=response.id, extra_body=ref
        )
    out = extract_json(response.output_text)
    return out, Trace(tool_calls=calls, response=response)


# --------------------------------------------------------------------- tools
def file_search_tool(vector_store_id):
    """A FileSearchTool bound to one vector store (pass directly in `tools=[...]`)."""
    return _models().FileSearchTool(vector_store_ids=[vector_store_id])


def function_tool(name, description, parameters, strict=True):
    """A FunctionTool the model can call; you execute it in run_with_trace's `functions`."""
    return _models().FunctionTool(
        name=name, description=description, parameters=parameters, strict=strict
    )


def mcp_tool(server_label, server_url, require_approval="never", allowed_tools=None):
    """An MCPTool the agent can call (Lab 5). `require_approval="never"` avoids approval friction."""
    m = _models()
    kwargs = dict(server_label=server_label, server_url=server_url, require_approval=require_approval)
    if allowed_tools:
        kwargs["allowed_tools"] = allowed_tools
    return m.MCPTool(**kwargs)


# --------------------------------------------------------------------- file search (RAG)
def build_vector_store(folder, name=None, reuse=True) -> str:
    """Index every file under `folder` into a vector store; return its id.

    `folder` may be relative to content/knowledge (e.g. "healthhub-discharge-pack").
    Uses the OpenAI-compatible client (new API): openai.vector_stores.*

    When ``reuse=True`` (default) and a vector store with the same ``name`` already
    exists (and has indexed files), that store's id is returned instead of uploading
    everything again. Re-indexing the whole pack takes ~1 min, so reuse keeps repeat
    lab runs fast and avoids creating a new store on every run. Pass ``reuse=False``
    to force a fresh rebuild.
    """
    openai = get_openai()
    store_name = name or agent_name("pack")
    if reuse:
        try:
            for vs in openai.vector_stores.list():
                counts = getattr(vs, "file_counts", None)
                completed = getattr(counts, "completed", 0) if counts else 0
                if getattr(vs, "name", None) == store_name and completed:
                    return vs.id
        except Exception:  # listing is best-effort; fall through to a fresh build
            pass
    path = pathlib.Path(folder)
    if not path.is_absolute() and not path.exists():
        path = KNOWLEDGE / folder
    files = sorted(p for p in path.rglob("*") if p.is_file())
    if not files:
        raise RuntimeError(f"No files to index under {path}. Add the HealthHub docs first.")
    vs = openai.vector_stores.create(name=store_name)
    for fp in files:
        with open(fp, "rb") as fh:
            openai.vector_stores.files.upload_and_poll(vector_store_id=vs.id, file=fh)
    return vs.id


# --------------------------------------------------------------------- housekeeping
def cleanup(*agents):
    """Best-effort delete of the agent versions created during a lab run.

    Accepts agent objects returned by create_version / make_triage_agent.
    """
    api = get_project().agents
    for a in agents:
        if a is None:
            continue
        try:
            api.delete_version(agent_name=a.name, agent_version=a.version)
        except Exception:
            pass
