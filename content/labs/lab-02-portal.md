# Lab 2 (Portal) — Knowledge & Grounding: the Education Agent 🟢

> **Navigator rail · ~45 min.** Make every education answer carry a citation. No "advice" without provenance.

## Step 1 — Add the Web search tool
Open `carepal-<initials>` → **Build → Agents**. In the **Tools** panel click **Add** → pick **Web search** (Most popular).

![Tools → Add menu](images/lab2-tools-menu.png)

Choose **Search the web with Bing Search** (No setup required) → **Add**. Web search now shows under Tools with a cost/terms notice. Click **Save**.

![Web search attached](images/lab2-websearch-added.png)

## Step 2 — Tell the agent to ground & cite
Keep all of Lab 1's Instructions, then add:

```text
For education or self-care questions (route "education_navigation"), ground your reply using
web search. Populate source_labels with the article titles you used and source_urls with their
URLs — prefer healthhub.sg. If you cannot find support, say you are not sure and suggest the user
ask their own care provider — do NOT invent sources or guess medication interactions.
```

**Save** (creates a new version).

## Step 3 — Test the diet question
**New chat** → `What diet should my father follow after heart failure? Please cite sources.`
Confirm `route == "education_navigation"` and `source_urls` contains **healthhub.sg** links — and the **Web search** tag on the response:

![Grounded answer with healthhub.sg sources](images/lab2-grounded-answer.png)

## ✅ Validation
Paste the JSON → `source_urls` non-empty **and** ≥1 URL on the **healthhub.sg** host.

## 🎁 Optional challenge
Ask "Can my father take a herbal supplement called LiverTone with his heart-failure meds?" → agent **declines/qualifies**, routes to `timely_review`, **empty** `source_urls` (no fabricated sources).

---

### 🧭 Where next?
⬅️ Previous: [Lab 1 · Triage (Portal)](lab-01-portal.md) — 🏠 [Portal track index](PORTAL-TRACK.md) — Next: [Lab 3 · Govern & Observe (Portal)](lab-03-portal.md) ➡️

> 🟡🔴 On the notebook/SDK rail? See the full rail-tabbed lab: **[lab-02.md](lab-02.md)**.
