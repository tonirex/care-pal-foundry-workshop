# Care Pal — Microsoft Foundry Workshop (Day One)

### *From Discharge to Recovery: Building Patient-Care Agents with Microsoft Foundry*

A single-day, hands-on workshop where participants build **Care Pal** — a post-discharge
patient-care agent — in **Microsoft Foundry**. It is designed for a *mixed-skill room*:
clinicians and strategy folks stay in the no-code portal, while data scientists and developers
go deeper in notebooks and Python.

> [!TIP]
> **Three rails, one outcome.** Everyone builds the same Care Pal agent across Labs 0→5.
> Pick the rail that matches your comfort with code — you can switch rails between labs.

---

## Pick your rail

| Rail | For | You work in | Setup needed |
|------|-----|-------------|--------------|
| 🟢 **Navigator** | Clinicians, IT/digital leaders, strategy — *no code* | The **Foundry portal** (browser only) | **Nothing** — just a browser + workshop login |
| 🟡 **Builder** | Data scientists, analysts — *low code* | **Jupyter notebooks** (`content/assets/*.ipynb`) | Codespaces *(recommended)* or local Python |
| 🔴 **Engineer** | Developers, SIs — *full code* | **Python scripts** (`content/assets/*.py`) | Codespaces *(recommended)* or local Python |

🟢 **Navigator participants need none of the setup below** — go straight to the
[portal walkthrough](content/labs/PORTAL-TRACK.md).

---

## How the workshop flows

Everyone builds the **same** Care Pal agent across **six labs, done in order (Lab 0 → Lab 5)**. Each lab
builds on the last, so don't skip ahead. **Start at Lab 0** — the morning equaliser everyone does in the
portal — then continue through Labs 1–5.

From Lab 1 on, every lab is **rail-tabbed**: one page with a 🟢 Navigator, 🟡 Builder, and 🔴 Engineer
section. **Pick the rail that fits you and follow just that section** — you can switch rails between labs.

| Lab | Title | What you build |
|-----|-------|----------------|
| [Lab 0](content/labs/lab-00.md) | Hello, Care Pal | Your first safe agent (portal, all rails) |
| [Lab 1](content/labs/lab-01.md) | Triage Agent | Structured 7-key JSON + risk routing |
| [Lab 2](content/labs/lab-02.md) | Knowledge & Grounding | RAG over HealthHub, with citations |
| [Lab 3](content/labs/lab-03.md) | Govern & Observe | Guardrails + evaluation |
| [Lab 4](content/labs/lab-04.md) | Multi-Agent Care Pal | Orchestrator + specialists |
| [Lab 5](content/labs/lab-05.md) | Extend & Deploy | MCP tool + hosted agent (Engineer hands-on, everyone watches) |

**Two ways to read a lab:**
- **🟡 Builder / 🔴 Engineer** — use the rail-tabbed pages above (`lab-0N.md`); open the matching
  notebook (`content/assets/lab1_triage.ipynb`, Run All) or run the script (`python content/assets/lab1_triage.py`).
- **🟢 Navigator (no-code)** — use the same rail-tabbed pages, *or* the picture-heavy **screenshot
  walkthroughs** in the [Portal track](content/labs/PORTAL-TRACK.md) (`lab-0N-portal.md`). Same checkpoints.

**Moving between labs:** every lab page ends with a **🧭 Where next?** footer that links the previous and
next lab (and the matching portal/rail-tabbed version), so you can walk the whole workshop start to finish
without hunting for the next file.

---

## Quick start — 🟡 Builder / 🔴 Engineer

### Option A · GitHub Codespaces (recommended)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tonirex/care-pal-foundry-workshop?quickstart=1)

One click gives everyone an identical x64 Linux environment with Python 3.11, the Azure CLI,
and all dependencies pre-installed (including the Lab 3 evaluators that don't build on every
laptop).

1. **Code → Codespaces → Create codespace on main.** Wait for the post-create `pip install` to finish.
2. **Sign in to Azure** (one time, in the codespace terminal):
   ```bash
   az login --use-device-code
   ```
   Open the URL it prints, enter the code, and pick your **workshop account**.
3. **Create your `.env`:**
   ```bash
   cd content/assets
   cp .env.example .env
   # edit .env: set FOUNDRY_PROJECT_ENDPOINT (from the facilitator) and INITIALS
   ```
4. **Run a lab** — open a notebook (🟡) or run a script (🔴):
   ```bash
   python lab1_triage.py        # 🔴 Engineer
   # or open lab1_triage.ipynb and Run All  # 🟡 Builder
   ```

### Option B · Local machine

<details>
<summary>Windows (PowerShell)</summary>

```powershell
cd content\assets
python -m venv .venv ; .venv\Scripts\Activate.ps1
pip install -r requirements.txt
az login
copy .env.example .env   # then fill FOUNDRY_PROJECT_ENDPOINT + INITIALS
$env:PYTHONIOENCODING = "utf-8"   # so emoji output doesn't crash the console
python lab1_triage.py
```
</details>

<details>
<summary>macOS / Linux (bash)</summary>

```bash
cd content/assets
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
az login
cp .env.example .env   # then fill FOUNDRY_PROJECT_ENDPOINT + INITIALS
python lab1_triage.py
```
</details>

> [!NOTE]
> On **Windows on ARM64**, `azure-ai-evaluation` / `pandas` may not install (no ARM64 wheels).
> The labs degrade gracefully (Lab 3 prints `safety_score = N/A`), but Codespaces avoids this entirely.

---

## Access & authentication (read before the day)

The Builder/Engineer rails call a **shared Foundry project** via `DefaultAzureCredential`, so
each participant must be signed in to Azure **and** have access to that project.

**Participant** (covered above): `az login --use-device-code`, then set `FOUNDRY_PROJECT_ENDPOINT` in `.env`.

**Facilitator / admin — do this *before* the workshop:**
- Grant each attendee's workshop identity the **Foundry User** role (formerly *Azure AI User*;
  role ID `53ca6127-db72-4b80-b1b0-d745d6d5456d`) on the shared Foundry resource, so their token
  can build and run agents. **For a ~14-person cohort, per-attendee assignments are trivial — no
  shared service principal needed.**
- **Pre-deploy the models** (`model-router` + `gpt-5.4-mini`). Foundry User *cannot* deploy models
  (that's *Manage models*), so participants reuse the central deployments.
- **Pre-create any required connections** (e.g. an App Insights connection if you want the full Lab 3
  *Traces* tab). Foundry User can't create connections — but the labs are designed so this isn't
  needed: Lab 2 web search is "no setup required" and cross-run tracing is optional.
- Share the project endpoint (`https://<account>.services.ai.azure.com/api/projects/<project>`)
  and the model deployment name.

> [!WARNING]
> **Foundry User can't *Publish* agents.** Lab 5 Part B (hosted publish) needs **Foundry Project
> Manager** at the Foundry resource scope, so it is **facilitator-demo-only** (also untestable
> without a Teams/M365 license). Everything else in Labs 0–5 is a *data action* that Foundry User
> permits. See the plan's **§12** RBAC table.

See the plan's **§12 Pre-Workshop Setup** — or the step-by-step
**[admin & logistics page](content/admin/ADMIN-SETUP.md)** (with a ready-to-run RBAC script) — for the
full checklist.

---

## What's in here

```
.
├── README.md                       ← you are here
├── .devcontainer/devcontainer.json ← Codespaces / VS Code dev container
├── foundry-day1-workshop-plan.md   ← the full build plan & run-of-show (facilitators)
└── content/
    ├── README.md                   ← content map & how the pieces fit
    ├── admin/ADMIN-SETUP.md         ← ⭐ admin & pre-workshop logistics (RBAC script, models, MCP)
    ├── labs/                        ← participant-facing labs (rail-tabbed) + PORTAL-TRACK.md (🟢)
    ├── assets/                      ← runnable code: notebooks (🟡) + scripts (🔴)
    │   ├── common/carepal_common.py ←   the one helper that calls Foundry Agent Service
    │   ├── lab1_triage.* … lab4_multiagent.*
    │   ├── mcp-appointments/        ←   Lab 5 Part A — mock appointments MCP server (deployed to ACA)
    │   └── hosted-deploy/           ←   Lab 5 Part B — hosted-agent deploy scaffold
    ├── knowledge/                   ← RAG grounding docs for Lab 2/4 (HealthHub pack)
    ├── prompts/test-prompts.json    ← single source of truth for canned prompts + expected routes
    ├── narrative/rajan.md           ← the patient story, one chapter per lab
    └── answer-keys/                 ← SERVER-SIDE validators — never ship to participants
```

## Where to go next

- 🟢 **Navigator:** [content/labs/PORTAL-TRACK.md](content/labs/PORTAL-TRACK.md)
- 🟡 **Builder:** open `content/assets/lab1_triage.ipynb`
- 🔴 **Engineer:** [content/assets/README.md](content/assets/README.md)
- 🧭 **Facilitators:** [foundry-day1-workshop-plan.md](foundry-day1-workshop-plan.md) · [content/README.md](content/README.md)
- 🛠️ **Admin / operator:** [content/admin/ADMIN-SETUP.md](content/admin/ADMIN-SETUP.md) — RBAC, models, MCP, dry-run

---

> [!IMPORTANT]
> `content/answer-keys/` are **graders**, not participant assets. Keep them out of any deployed
> agent code and never surface them to the room.
