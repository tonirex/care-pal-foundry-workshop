"""Lab 4 (Engineer) — Multi-Agent Care Pal: orchestration via function-tool delegation.

Turn the triage agent into an orchestrator that delegates the LOW-risk compound request to two
specialists (Education + Follow-Up) and synthesises ONE reply.

In the *new* Foundry agents API the classic ConnectedAgentTool is retired. The portal-aligned
ways to do multi-agent are:
  - delegate via FUNCTION TOOLS that call specialist agents  <- this lab (runnable + assertable)
  - Workflow agents (WorkflowAgentDefinition) for declarative graphs
  - the A2A tool (A2APreviewTool) for cross-project / external agents
See the "GO FURTHER" note at the bottom. Run:  `python lab4_multiagent.py`

Reference patterns: azure-ai-projects 2.x -> tools/sample_agent_function_tool.py and
sample_workflow_multi_agent.py; agent-framework -> workflows (code-first option).
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
from common.carepal_common import (
    create_agent,
    make_triage_agent,
    run_with_trace,
    run_text,
    build_vector_store,
    file_search_tool,
    function_tool,
    text_of,
    agent_name,
    cleanup,
    TRIAGE_INSTRUCTIONS,
)

ORCHESTRATOR = TRIAGE_INSTRUCTIONS + """
You are Care Pal's orchestrator. Triage first. For LOW-risk paths, delegate then synthesise ONE reply:
- education / self-care content -> call the `ask_education` tool
- follow-up scheduling, check-ins, symptom tracking -> call the `ask_followup` tool
Call only the specialists needed. For medium/high risk do NOT delegate. Merge any source_labels /
source_urls returned by specialists into your final JSON.
"""

FOLLOWUP = (
    "You schedule check-ins and suggest follow-up appointment types after discharge, and collect "
    "symptom responses. You do not diagnose. Reply briefly and plainly."
)

# A tiny JSON schema shared by both delegation tools.
_QUESTION_SCHEMA = {
    "type": "object",
    "properties": {"question": {"type": "string", "description": "the user's request to forward"}},
    "required": ["question"],
    "additionalProperties": False,
}


# %%
def main():
    vs_id = build_vector_store("healthhub-discharge-pack")
    fs = file_search_tool(vs_id)

    # Two specialists: Education (grounded with file search) + Follow-Up (plain).
    education = make_triage_agent(
        name=agent_name("education"),
        instructions=TRIAGE_INSTRUCTIONS,
        tools=[fs],
        structured=True,
    )
    followup = create_agent(name=agent_name("followup"), instructions=FOLLOWUP, structured=False)

    # 👉 Expose each specialist as a FUNCTION TOOL the orchestrator can call.
    tools = [
        function_tool("ask_education", "Grounded self-care / education answer with citations",
                      _QUESTION_SCHEMA),
        function_tool("ask_followup", "Follow-up scheduling, check-ins and symptom tracking",
                      _QUESTION_SCHEMA),
    ]

    # Handlers: each forwards the question to its specialist agent and returns the text.
    functions = {
        "ask_education": lambda question: run_text(education, question),
        "ask_followup": lambda question: run_text(followup, question),
    }

    orchestrator = make_triage_agent(
        name=agent_name("orchestrator"), instructions=ORCHESTRATOR, tools=tools, structured=True
    )
    # NOTE: if your model rejects structured output + tools together, set structured=False here;
    # extract_json() still tolerates a JSON-in-prose reply.

    try:
        out, trace = run_with_trace(orchestrator, text_of("follow_up_and_diet"), functions=functions)
        called = [c.name for c in trace.tool_calls]
        specialist = [c for c in trace.tool_calls if c.name in ("ask_education", "ask_followup")]
        print("tool calls:", called)
        assert len(specialist) >= 2, f"expected >=2 specialist calls, got {called}"
        print("Lab 4 passed ✅")

        # TODO (bonus): add a third specialist (Assessment or Enrollment & Linkage) and show it firing.
        # GO FURTHER (Engineer): re-implement this as a Workflow agent (WorkflowAgentDefinition,
        # see sample_workflow_multi_agent.py) or with the Microsoft Agent Framework
        # (agent-framework -> FoundryChatClient + workflows) for code-first orchestration.
    finally:
        cleanup(orchestrator, education, followup)


if __name__ == "__main__":
    main()
