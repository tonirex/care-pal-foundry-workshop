"""Lab 2 (Engineer) — Knowledge & Grounding (the Education agent).

Attach a file-search (RAG) index over the curated HealthHub discharge pack so every education
answer carries a healthhub.sg citation. Run:  `python lab2_rag.py`

PREREQ: drop the real HealthHub exports into ../knowledge/healthhub-discharge-pack/ first
(see that folder's README) — otherwise there is nothing to cite.

Reference patterns: Foundry-Agent-Lab -> file-search quickstart;
azure-ai-projects 2.x -> tools/sample_agent_file_search.py.
"""
# %%
import sys
import pathlib
_here = (pathlib.Path(globals()["__file__"]).resolve().parent
         if "__file__" in globals() else pathlib.Path.cwd())
if str(_here) not in sys.path:
    sys.path.insert(0, str(_here))

# %%
import json
from common.carepal_common import (
    make_triage_agent,
    run_and_parse,
    build_vector_store,
    file_search_tool,
    text_of,
    cleanup,
    TRIAGE_INSTRUCTIONS,
)

GROUNDING = TRIAGE_INSTRUCTIONS + """
For education / self-care questions (route "education_navigation"), ground your reply in the attached
HealthHub knowledge base. Put the article titles in source_labels and their healthhub.sg URLs in
source_urls. If the knowledge base does not support an answer, say you are not sure and route to
"timely_review" - do NOT invent sources.
"""

# %%
def main():
    # 👉 Build a vector store from the pack and attach it as a file-search tool.
    vs_id = build_vector_store("healthhub-discharge-pack")
    fs = file_search_tool(vs_id)
    agent = make_triage_agent(
        instructions=GROUNDING,
        tools=[fs],
        structured=True,
    )
    try:
        out = run_and_parse(agent, text_of("diet_question"))
        print(json.dumps(out, indent=2))
        assert out["source_urls"], "expected at least one citation"
        assert any("healthhub.sg" in u for u in out["source_urls"]), out["source_urls"]
        print("Lab 2 passed ✅")

        # TODO (bonus): send the LiverTone question (prompt id 'unsupported_question') and assert
        # source_urls is EMPTY and route == 'timely_review' (the safe, no-fabrication behaviour).
    finally:
        cleanup(agent)


if __name__ == "__main__":
    main()
