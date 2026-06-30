# Hosted Care Pal — deploy scaffold (Lab 5, Part B)

Deploy Care Pal to **Foundry Agent Service** as a managed **hosted agent** so it runs as a service
instead of a playground session. This folder is **standalone** — `src/agent.py` doesn't import the
workshop `common` package, so it can ship on its own.

## Option 1 — VS Code Microsoft Foundry toolkit (recommended)
1. Install the **Microsoft Foundry** (AI Toolkit) extension in VS Code.
2. Open this `hosted-deploy/` folder.
3. Sidebar → **Deploy to Microsoft Foundry** → choose the shared workshop project →
   deploy as **Code (Remote)** (Azure installs from `src/requirements.txt`).
4. Reference: https://code.visualstudio.com/docs/intelligentapps/hosted-agents

## Option 2 — azd
```powershell
copy .env.example .env      # fill FOUNDRY_PROJECT_ENDPOINT
azd up
```
> `azure.yaml` is a starting point; the toolkit path above is the supported one for hosted agents.

## Run locally first (sanity check)
```powershell
pip install -r src/requirements.txt
az login
copy .env.example .env       # fill FOUNDRY_PROJECT_ENDPOINT
python src/agent.py          # creates the carepal-hosted agent in your project
```

## ✅ Validate (matches the lab)
From the **Agent Inspector / Call agent**, send:
> *What diet should my father follow after heart failure?*

Pass = a valid **triage JSON** (7 keys) comes back. (Grounding/citations come from the knowledge you
attach in the portal — Lab 2 — or by adding a file-search tool to `agent.py`.)

## ⭐ Optional stretch — connect a channel
Out of the core timebox and fully droppable: surface this hosted agent on a **WhatsApp/Telegram
sandbox** so a phone in the room can chat to it. The hard part (a safe, grounded, deployed agent) is
already done — the channel is just the last mile.
