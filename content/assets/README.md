# Care Pal — workshop starter assets

Runnable reference code for the **🟡 Builder** (notebooks) and **🔴 Engineer** (scripts) rails.
The 🟢 Navigator rail is portal-only and needs nothing here.

Everything talks to **Microsoft Foundry Agent Service** through one helper —
`common/carepal_common.py` — so each lab file stays short and readable.

> These are **reference solutions you can run as-is** for the facilitator demo. To do a lab as a
> hands-on exercise, blank out the lines marked `# 👉` and retype them. The `# TODO (bonus)` lines
> are genuinely open.

## Layout
```
assets/
  common/carepal_common.py   # the one place that calls the SDK
  lab1_triage.py   lab1_triage.ipynb     # structured triage
  lab2_rag.py      lab2_rag.ipynb        # file-search grounding (HealthHub)
  lab3_eval.py     lab3_eval.ipynb       # guardrails + evaluation
  lab4_multiagent.py lab4_multiagent.ipynb  # connected-agent orchestration
  mcp-appointments/          # Lab 5 Part A — mock appointments MCP server
  hosted-deploy/             # Lab 5 Part B — hosted-agent deploy scaffold (azd / VS Code Toolkit)
  requirements.txt  .env.example
```

## Setup (once)

**Codespaces / macOS / Linux (bash)** — dependencies are already installed in Codespaces, so this
just signs you in and creates your `.env`:
```bash
./setup.sh        # az login --use-device-code + copy .env.example -> .env
```
Or do it by hand:
```bash
pip install -r requirements.txt
az login --use-device-code     # DefaultAzureCredential
cp .env.example .env           # then fill in FOUNDRY_PROJECT_ENDPOINT + INITIALS
```

**Windows (PowerShell):**
```powershell
python -m venv .venv ; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
az login                                            # DefaultAzureCredential
copy .env.example .env                              # then fill in FOUNDRY_PROJECT_ENDPOINT + INITIALS
$env:PYTHONIOENCODING = "utf-8"                      # so emoji output doesn't crash the console
```

`.env`:
| var | meaning |
|-----|---------|
| `FOUNDRY_PROJECT_ENDPOINT` | `https://<account>.services.ai.azure.com/api/projects/<project>` (the shared workshop project) |
| `FOUNDRY_MODEL_NAME` | model deployment name — default `model-router` |
| `INITIALS` | your initials, so your agents are named `carepal-<initials>` in the shared project |

## Run a lab (Engineer rail)
```powershell
# from the assets/ folder, so `common` is importable
python lab1_triage.py
```
Each script creates its agent(s), runs the canned prompts from
`../prompts/test-prompts.json`, **asserts the expected routes**, prints `OK …`, then deletes the
agents it made.

## Notes
- **Lab 2 needs real grounding docs.** Drop the HealthHub PDFs/exports listed in
  `../knowledge/healthhub-discharge-pack/README.md` into that folder before running `lab2_rag.py`,
  or the `healthhub.sg` citation assert won't have anything to cite.
- **Lab 3 evaluation** uses `azure-ai-evaluation`. If the safety evaluator isn't enabled in the
  tenant the script prints `safety_score = N/A` and still checks routing (mirrors the lab).
- **SDK drift:** the helper imports model classes from `azure.ai.agents.models` and falls back to
  `azure.ai.projects.models`, and tries typed structured-output before a dict — so it survives minor
  package-version differences. If an import still fails, check the version pins in `requirements.txt`
  against the reference repos (Foundry-Agent-Lab, agentic-ai-immersion).
- **Security:** never put `../answer-keys/` next to deployed agent code — those are graders, not assets.
