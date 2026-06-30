# Admin & Pre-Workshop Logistics — Care Pal Foundry Day

> **Audience:** the operator/admin and lead facilitator. Everything here is done **before**
> participants arrive. Target cohort: **~14 participants**, one shared Foundry project.
> Companion docs: facilitator run-of-show in [`../../foundry-day1-workshop-plan.md`](../../foundry-day1-workshop-plan.md) (§11–§13), participant portal guide in [`../labs/PORTAL-TRACK.md`](../labs/PORTAL-TRACK.md).

## Timeline at a glance

| When | Task | Owner |
|------|------|-------|
| **T‑1 week** | Confirm shared Foundry project + quota; collect ~14 attendee UPNs | Admin |
| **T‑2 days** | Deploy models; run the **RBAC script** (§3); deploy/confirm the MCP server (§5) | Admin |
| **T‑1 day** | Verify knowledge pack (§6); share repo + Codespaces (§7); **dry-run one lab per rail** (§8) | Facilitator |
| **Morning of** | Quick checklist (§9): endpoint on screen, MCP URL reachable, models warm | Operator |
| **After** | Optional teardown (§10) | Admin |

---

## 1. Shared Foundry project

- One **Foundry resource** + one **project** (intended name `ntfgh-carepal-workshop`) on the
  **New Foundry** experience — simplest for a mixed/non-technical room, single quota to manage.
- Add the ~14 participants as **Entra guests** or via a **shared workshop login**.
- Pre-build a read-only **`carepal-reference`** agent participants can clone.
- Enforce the naming convention **`carepal-<initials>`** so the shared project stays legible.

---

## 2. Models (participants can't deploy these)

Deploy **before** the day — `Foundry User` (the participant role) **cannot** create deployments:

- `model-router` and `gpt-5.4-mini`, **Global Standard**.
- Sanity-check **tokens-per-minute** quota for ~14 concurrent users. A 14-person cohort is small,
  so default TPM is usually ample — confirm in the dry-run and raise only if you hit limits.

---

## 3. ⭐ RBAC — assign roles (the key step)

Validated against the official [Foundry RBAC docs](https://learn.microsoft.com/azure/foundry/concepts/rbac-foundry).
The Foundry roles were **renamed** (e.g. *Azure AI User → Foundry User*); IDs are unchanged, so the
scripts use **role IDs** to survive the rename rollout.

**Who gets what:**

| Identity | Role | Role ID | Why |
|----------|------|---------|-----|
| Each of the ~14 participants | **Foundry User** | `53ca6127-db72-4b80-b1b0-d745d6d5456d` | Build + run agents, file search, eval, inference (data plane) |
| Lead facilitator | **Foundry Project Manager** | `eadc314b-1a2d-4efa-be10-5d325db5065e` | Can **Publish** the Lab 5 Part B hosted agent (Foundry User can't) |
| Project's managed identity | **Foundry User** | `53ca6127-…` | Lets the project call Foundry features (per docs "minimum assignments") |

> **What Foundry User *cannot* do** (all handled centrally): **deploy models** (§2),
> **create connections** (§4), and **publish agents** (Lab 5 Part B → facilitator demo). Everything
> else across Labs 0–5 is a *data action* it permits. Full per-lab matrix: plan **§12a**.

**Run it** — sign in as someone with **Owner** or **User Access Administrator** on the resource:

```bash
az login
# 1) discover the Foundry resource (account) ID:
az cognitiveservices account show -n <foundry-account> -g <rg> --query id -o tsv
# 2) put your ~14 UPNs in attendees.txt (copy attendees.example.txt), then:
./assign-foundry-rbac.sh "<paste-resource-id>" attendees.txt facilitator@contoso.com
#   PowerShell:  ./assign-foundry-rbac.ps1 -ResourceId "<id>" -Facilitator facilitator@contoso.com
```

**Verify** a participant can build:

```bash
az role assignment list --assignee alice@contoso.com --scope <resource-id> -o table
```

Scripts in this folder: [`assign-foundry-rbac.ps1`](assign-foundry-rbac.ps1) ·
[`assign-foundry-rbac.sh`](assign-foundry-rbac.sh) · [`attendees.example.txt`](attendees.example.txt).

---

## 4. Connections (optional — admin only)

`Foundry User` can't create connections, so if a lab needs one, **you** create it (or skip):

- **Lab 2 web search** uses Bing with *"no setup required"* → **no connection needed**. ✅
- **Lab 3 full *Traces* tab** (history across runs) needs an **Application Insights** connection on
  the project. It's **optional** — the inline single-run trace works without it. Pre-create the
  App Insights connection only if you want the full traces history during the eval lab.

---

## 5. Mock appointments MCP server (Lab 5 Part A)

A no-auth synthetic appointments tool, deployed once and shared as a URL.

- **Already live (demo instance):**
  `https://carepal-appointments.delightfulpond-b7635e07.southeastasia.azurecontainerapps.io/mcp`
  (RG `rg-carepal-mcp`, southeastasia, no auth).
- **Redeploy / fresh deploy:** from [`../assets/mcp-appointments/`](../assets/mcp-appointments/) run
  `az login` then `./deploy-mcp.ps1` (or `bash deploy-mcp.sh`). Builds from source on ACR — no local
  Docker — and prints the `/mcp` URL.
- **Cost:** 0.5 vCPU / 1 GiB, min 1 replica ≈ **$6 for two weeks**, ~$15 worst-case. Teardown:
  `az group delete -n rg-carepal-mcp --yes`.
- **Foundry MCP form has no "None" auth** → choose **Key-based** and paste a throwaway header
  (`x-demo: workshop`); the server ignores it.
- **Share the `/mcp` URL** with the room (slide / chat) before Lab 5.

---

## 6. Knowledge pack (Lab 2 / Lab 4 grounding)

- `../knowledge/healthhub-discharge-pack/` currently holds **synthetic** HealthHub stand-in docs so
  the RAG/citation labs work out of the box.
- ⚠️ **Before go-live:** have a content owner **verify or replace** these with licensed HealthHub
  exports. They are clearly marked `status: synthetic-workshop-sample` in each file's frontmatter.

---

## 7. Code rails — repo & Codespaces (🟡 Builder / 🔴 Engineer)

- Repo: **github.com/tonirex/care-pal-foundry-workshop** (private). Add participants who take the
  Builder/Engineer rails as repo collaborators (or fork into the customer org).
- They open **Code → Codespaces** → identical x64 env, deps pre-installed (incl. Lab 3 evaluators).
- In the Codespace they run `az login --use-device-code`, then `cd content/assets && cp .env.example
  .env` and set `FOUNDRY_PROJECT_ENDPOINT` (share it) + their `INITIALS`.
- 🟢 **Navigator participants need none of this** — browser + project login only.

---

## 8. Dry-run (T‑1 day) — do not skip

Run **one lab per rail** end-to-end in the real tenant to catch drift:

- 🟢 Navigator: build Lab 0 agent in the portal; confirm the refusal + a triage answer.
- 🟡/🔴 Builder/Engineer: in a Codespace, `python content/assets/lab1_triage.py` → expect 3/3 routes;
  `lab2_rag.py` → expect a `healthhub.sg` citation.
- Confirm portal feature names haven't drifted: **structured output**, **Workflows (multi-agent)**,
  **content-safety guardrails**, **evaluators**.

---

## 9. Morning-of checklist

- [ ] Project **endpoint** on a slide; MCP **`/mcp`** URL reachable.
- [ ] Models warm (send one test prompt).
- [ ] RBAC spot-check: one participant can open the project and create an agent.
- [ ] `carepal-reference` agent present; naming convention on a slide.
- [ ] Facilitator account confirmed as **Foundry Project Manager** (for the Lab 5B publish demo).

---

## 10. Teardown (after the workshop)

- Tear down the MCP server: `az group delete -n rg-carepal-mcp --yes`.
- (Optional) remove participant role assignments and the shared project.

---

### Reference — role IDs (use IDs, not names, during the rename rollout)

| Role | ID |
|------|----|
| Foundry User | `53ca6127-db72-4b80-b1b0-d745d6d5456d` |
| Foundry Project Manager | `eadc314b-1a2d-4efa-be10-5d325db5065e` |
| Foundry Account Owner | `e47c6f54-e4a2-4754-9501-8e0985b135e1` |
| Foundry Owner | `c883944f-8b7b-4483-af10-35834be79c4a` |
