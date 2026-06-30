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
- Grant every attendee's workshop identity an RBAC role on the shared project
  (e.g. **Azure AI User**) so their token can create/run agents.
- Share the project endpoint (`https://<account>.services.ai.azure.com/api/projects/<project>`)
  and the model deployment name.
- **For a small cohort (~14): just grant per-attendee role assignments on the one shared
  project** — it's quick and cleanest, no shared service principal needed. (Codespaces org
  secrets / a service principal only become worth it at much larger scale.)

See the plan's **§12 Pre-Workshop Setup** for the full checklist.

---

## What's in here

```
.
├── README.md                       ← you are here
├── .devcontainer/devcontainer.json ← Codespaces / VS Code dev container
├── foundry-day1-workshop-plan.md   ← the full build plan & run-of-show (facilitators)
└── content/
    ├── README.md                   ← content map & how the pieces fit
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

---

> [!IMPORTANT]
> `content/answer-keys/` are **graders**, not participant assets. Keep them out of any deployed
> agent code and never surface them to the room.
