"""Lab 1 (Engineer) — Triage Agent with structured output.

Make Care Pal return the 7-key triage JSON every turn and route by clinical risk.
Run from the `assets/` folder (so `common` imports):  `python lab1_triage.py`

Reference patterns: Foundry-Agent-Lab -> prompt-agent quickstart (structured output via
PromptAgentDefinition.text); azure-ai-projects 2.x -> sample_agent_structured_output.py.
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
    make_triage_agent,
    run_and_parse,
    text_of,
    route_of,
    REQUIRED_KEYS,
    cleanup,
)

# The three messages we route in this lab (see ../prompts/test-prompts.json).
CASES = ["diet_question", "swelling_worsening", "chest_pain"]

# %%
def main():
    # 👉 Create the triage agent. structured=True enforces the 7-key JSON contract.
    agent = make_triage_agent(structured=True)
    try:
        for pid in CASES:
            out = run_and_parse(agent, text_of(pid))
            missing = set(REQUIRED_KEYS) - set(out)
            assert not missing, f"{pid}: missing keys {missing}"
            assert out["route"] == route_of(pid), f"{pid}: {out['route']} != {route_of(pid)}"
            print(f"OK  {pid:18} -> {out['route']}")
        print("Lab 1 passed ✅")

        # TODO (bonus): add intent 'medication_question' to your instructions and assert that a
        # medication-timing question routes to 'timely_review'. (Earns the Schema Surgeon badge.)
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
