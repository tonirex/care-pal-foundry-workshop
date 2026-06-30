# Care Pal Foundry Day — workshop content

Loadable content for *From Discharge to Recovery: Building Patient-Care Agents with Microsoft Foundry*.
Authored from `../foundry-day1-workshop-plan.md`. Designed to drop into the Fabric-day gamified
platform (Next.js + Supabase) with only a config + validator delta.

```
content/
  config/workshop.yaml                  # platform config (shared project, rails, labs, badges)
  narrative/rajan.md                    # patient story — one chapter per lab
  prompts/test-prompts.json             # SINGLE SOURCE OF TRUTH for canned prompts + expected routes
  labs/lab-00.md ... lab-05.md          # participant-facing, rail-tabbed (navigator/builder/engineer)
  answer-keys/lab-00.json ... lab-05.json   # SERVER-SIDE ONLY validators (never ship to client)
  knowledge/healthhub-discharge-pack/   # RAG source for Lab 2 (content owner curates)
  assets/                               # runnable starter code: notebooks (Builder) + scripts (Engineer)
    common/carepal_common.py            #   one helper that talks to Foundry Agent Service
    lab1_triage.* ... lab4_multiagent.* #   paired .py (Engineer) + .ipynb (Builder)
    mcp-appointments/                   #   Lab 5 Part A — mock appointments MCP server
    hosted-deploy/                      #   Lab 5 Part B — hosted-agent deploy scaffold (azd / VS Code)
```

## Portal-only track
Non-technical participants can stay in the Foundry portal. Screenshot walkthroughs:
**[labs/PORTAL-TRACK.md](labs/PORTAL-TRACK.md)** (`lab-00-portal.md` … `lab-05-portal.md`).

## How the pieces fit
- **Each lab** states one shared **objective** + **validation checkpoint**, then three **rails** to get there.
- **Validators** live in `answer-keys/` and reference `prompts/test-prompts.json` by `prompt_id`.
  Two validator types (see plan §9): **A** paste-the-output (all rails), **B** endpoint harness (engineer/hosted).
- **Enums** (`intent` / `risk_level` / `route`) are defined once in `lab-01.md` and `test-prompts.json` — keep them in sync.

## Security (inherited from the Fabric day)
- `answer-keys/*.json` load **only** inside `app/api/` server routes. Never import in client components,
  return in API responses, or place under `/public/`.
- Run the platform's `validate-keys` script (must exit 0) before go-live.

## Status
Draft v0.2 — labs, answer keys, and **starter assets** (Builder notebooks + Engineer scripts +
mock MCP server + hosted-deploy scaffold) authored and syntax-verified. Pending: per-lab
troubleshooting KB, the curated HealthHub files, and a live end-to-end run against a Foundry tenant.
