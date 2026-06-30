---
id: lab-02
title: "Lab 2: Knowledge & Grounding — the Education Agent"
duration_minutes: 45
audience: ["Everyone"]
foundry_capabilities: ["Tools & Knowledge", "Web search", "File search / RAG", "Citations"]
order: 2
is_active: false
max_points: 300
bonus_quest: true
rails: ["navigator", "builder", "engineer"]
tier: "L200"
---

> 🩺 **Mr. Rajan — Chapter 2**
> Reassured, the family asks: *"What diet should my father follow after heart failure?"* General
> advice isn't enough in healthcare — it has to be **grounded** in a trusted source they can point
> to. Care Pal answers and cites HealthHub, so the family knows where the guidance comes from.

## What you'll learn
The difference between *information* and *advice* is **provenance**. You'll attach **knowledge** to
your agent — a web-search tool plus a private **file-search (RAG)** index of curated HealthHub
discharge-care documents — and make every education answer carry citations.

## Demo (facilitator, 5 min)
Ask the diet question on the customer's agent → show `source_labels` / `source_urls` populated with
HealthHub links. Then ask something the pack doesn't cover and show it *declines* rather than invents.

---

## 🟢 Navigator — portal
1. Open your `carepal-<initials>` agent → **Tools** → add **Web search**.
2. **Knowledge** (or **Add → Upload files**) → upload the provided **`healthhub-discharge-pack/`**
   (heart / kidney / liver self-care docs). This creates a **file-search** index.
3. Add this paragraph to your Instructions (keep everything from Lab 1):

```text
For education or self-care questions (route "education_navigation"), ground your reply in the
attached HealthHub knowledge base, using web search only to supplement. Populate source_labels with
the article titles you used and source_urls with their healthhub.sg URLs. If the knowledge base does
not support an answer, say you are not sure and suggest the user ask their own care provider —
do NOT invent sources or guess medication interactions.
```

4. **Chat** → send **`What diet should my father follow after heart failure?`** → confirm the reply
   is sensible **and** `source_urls` contains a `healthhub.sg` link. Copy the JSON.

## 🟡 Builder — notebook
Open **`lab2_rag.ipynb`**: create a vector store from the pack, attach a `FileSearchTool`, query the
diet question, and print the citations. *(Web Search is also GA in the new API if you want to ground
on live pages — optional.)*
*(Pattern: azure-ai-projects 2.x → `samples/agents/tools/sample_agent_file_search.py`.)*

## 🔴 Engineer — SDK
Complete **`lab2_rag.py`**: upload the docs, build the index, attach the `FileSearchTool`, and
`assert` that an education query returns ≥1 citation on the `healthhub.sg` host.

```python
vs_id = build_vector_store("healthhub-discharge-pack")   # uploads the pack -> vector store
fs = file_search_tool(vs_id)                             # FileSearchTool(vector_store_ids=[vs_id])
agent = make_triage_agent(instructions=GROUNDING, tools=[fs], structured=True)
out = run_and_parse(agent, text_of("diet_question"))
assert any("healthhub.sg" in u for u in out["source_urls"]), out
```

---

## ✅ Validation
Paste the JSON for **"What diet should my father follow after heart failure?"**
Passes when **`source_urls` is non-empty** *and* at least one URL is on the **`healthhub.sg`** host.
**(300 pts · badge 📚 Librarian)**

## 🎁 Bonus (+50)
Send the un-grounded question **"Can my father take a herbal supplement called LiverTone together
with his heart failure medication?"** Show that your agent **declines / qualifies** and routes to
`timely_review` — with **empty** `source_urls` (no fabricated citations). This is the safe behaviour.

## Stuck?
- No citations? Confirm the knowledge files **finished indexing**, and that your instructions tell
  the agent to *populate* `source_urls` from the knowledge base.
- Citations point somewhere other than HealthHub? Tighten the instruction to prefer the attached
  pack; web search is a supplement, not the primary source.
