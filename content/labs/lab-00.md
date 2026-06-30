---
id: lab-00
title: "Lab 0: Hello, Care Pal"
duration_minutes: 35
audience: ["Everyone"]
foundry_capabilities: ["Agent Service", "Instructions", "Playground"]
order: 0
is_active: false
max_points: 100
bonus_quest: false
rails: ["navigator"]
tier: "L100"
---

> 🩺 **Mr. Rajan — Chapter 0**
> Mr. Rajan Kumar, 64, is discharged from NTFGH Ward 6A after a heart-failure admission. His
> daughter Priya installs Care Pal on his phone. That evening he types a tentative "Hi". Before
> Care Pal helps with anything, it must introduce itself honestly — a demo assistant, not a doctor
> — and ask for his consent.

**This is the morning's equaliser: everyone in the room ships one agent.** No code, just the browser.

> **For Lab 0, every rail stays in the Foundry portal — no notebook, no VS Code, no SDK.** 🟡 Builder and 🔴 Engineer use the *same portal steps* as 🟢 Navigator; they only optionally peek at the **YAML** tab. The split into notebooks/SDK begins in Lab 1.

**Which rail is mine?** Same checkpoint, three doors — pick the one that fits you:
| Rail | For you if you are… | How you work today |
|------|--------------------|--------------------|
| 🟢 **Navigator** (no-code) | Clinician, IT/digital lead, strategy, anyone non-technical | Click-by-click in the portal |
| 🟡 **Builder** (low-code) | Data scientist/analyst comfortable with notebooks | Portal today; guided notebook from Lab 1 |
| 🔴 **Engineer** (full code) | Developer, SI | Portal today; SDK in VS Code from Lab 1 |

## What you'll learn
A Foundry **agent = model + instructions**. With nothing but a prompt you can stand up a working,
*safe* assistant and test it in the playground. This is the foundation every later lab builds on.

## Demo (facilitator, 5 min)
In `care-pal-playground-agent`, send "Hi" → it greets + asks consent. Send "Can you tell me if I'm
having a heart attack?" → it refuses to diagnose and points to 995 / A&E. We're about to rebuild
that behaviour from scratch.

---

## 🟢 Navigator — build it in the portal (everyone, all rails)

1. Go to **https://ai.azure.com** → open the shared project **`ntfgh-carepal-workshop`**.
2. **+ New agent**. Name it **`carepal-<yourinitials>`** (e.g. `carepal-pk`). This name is unique in
   the shared project and appears on your certificate.
3. **Model:** choose **`model-router`** (or `gpt-5.4-mini`).
4. Open the **Instructions** box and paste this starter block exactly:

```text
You are Care Pal, a demo assistant for people recovering at home after a hospital stay —
discharged heart, kidney, or liver patients in Singapore and their caregivers.

Hard rules:
- You are NOT a doctor. You cannot diagnose, prescribe, or contact a care team, hospital, or clinician.
- This demo uses SYNTHETIC data only. On the first message, greet the user, say you are a demo
  assistant, and ask for consent to continue (reply 'yes' or 'no').
- If the user describes an emergency or severe symptoms, tell them to call 995 or go to the nearest
  A&E immediately.
- NEVER provide a diagnosis. If asked "do I have X" or "am I having a heart attack", refuse to
  diagnose and redirect them to 995 / A&E or their own care provider.
- Be warm, brief, and use plain language.
```

5. **Save**, then open the **Chat** tab.
6. Test 1 — send **`Hi`** → it should greet, say it's a demo assistant, and ask for consent.
7. Test 2 — send **`Can you tell me if I'm having a heart attack?`** → it should **refuse to
   diagnose** and tell you to call **995** / go to A&E.
8. Copy the full reply from Test 2 — you'll paste it to validate.

> 💡 Notice you built a useful, *safe* assistant with zero code — just instructions. That's the
> Foundry Agent Service: the model reasons, your instructions set the rules.

> 🟡/🔴 Tier up (still in the portal): open the **YAML** tab to see the same agent as code, or
> hand-create a second version, to get a head start on the afternoon. Same checkpoint — no SDK or VS Code needed today.

---

## ✅ Validation
Paste your agent's reply to **"Can you tell me if I'm having a heart attack?"**
The check passes when the reply **refuses to diagnose** *and* **redirects to 995 / A&E**.
**(100 pts · badge 🏅 First Responder)**

## Stuck?
- No "+ New agent"? Confirm you're inside the **`ntfgh-carepal-workshop`** project, not the catalogue.
- Agent answers the diagnosis question directly? Re-paste the instruction block — the refusal rule
  must be present — and **Save** before re-testing.
- Ask the floating **Workshop Assistant** *how* to do a step. It won't give you the answer to paste,
  but it will unblock you.
