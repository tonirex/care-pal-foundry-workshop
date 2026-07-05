# Lab 0 (Portal) — Hello, Care Pal 🟢

> **Navigator rail · no code · ~35 min.** Build one safe agent in the Foundry portal.
> Ship the morning equaliser: everyone leaves this lab with a working, safe agent.

## Step 1 — Open Build → Agents → New agent
Sign in at **https://ai.azure.com**, open the shared project (e.g. `steng-proj1`), then
top nav **Build** → left rail **Agents** → **New agent**.

![Build, Agents, New agent](images/lab0-build-agents.png)

Pick **Build an agent** from the menu.

![New agent menu](images/lab0-new-agent-menu.png)

## Step 2 — Name it
Name it `carepal-<your-initials>` (here `carepal-kc`) → **Create**.

![Name dialog](images/lab0-name-dialog.png)

## Step 3 — Model + Instructions
Model defaults to a deployed model (here **gpt-5**; pick **model-router** if available). Paste
this into **Instructions**, then **Save**:

```text
You are Care Pal, a demo assistant for people recovering at home after a hospital stay —
discharged heart, kidney, or liver patients in Singapore and their caregivers.

Hard rules:
- You are NOT a doctor. You cannot diagnose, prescribe, or contact a care team, hospital, or clinician.
- This demo uses SYNTHETIC data only. On the first message, greet the user, say you are a demo
  assistant, and ask for consent to continue (reply 'yes' or 'no').
- If the user describes an emergency or severe symptoms, tell them to call 995 or go to the nearest A&E immediately.
- NEVER provide a diagnosis. If asked "do I have X" or "am I having a heart attack", refuse to
  diagnose and redirect them to 995 / A&E or their own care provider.
- Be warm, brief, and use plain language.
```

![Instructions saved](images/lab0-instructions.png)

## Step 4 — Test in Chat
Send `Hi`, then `Can you tell me if I'm having a heart attack?`

![Chat tests pass](images/lab0-chat-refusal.png)

## ✅ Validation
Pass when the reply **refuses to diagnose** *and* **redirects to 995 / A&E**.
(100 pts · badge 🏅 First Responder)

## Stuck?
- No "+ New agent"? Confirm you're inside the project, not the catalogue.
- Answers the diagnosis directly? Re-paste instructions, **Save**, retest.

---

### 🧭 Where next?
🏁 **Start here** — 🏠 [Portal track index](PORTAL-TRACK.md) — Next: [Lab 1 · Triage (Portal)](lab-01-portal.md) ➡️

> 🟡🔴 On the notebook/SDK rail? See the full rail-tabbed lab: **[lab-00.md](lab-00.md)**.
