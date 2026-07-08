# 🩺 Lab 2 · Knowledge & Grounding — the Education Agent

**⏱️ 45 min**  ·  **👥 Everyone**  ·  **📊 L200**  ·  **🧩 Tools & Knowledge, Web search, File search / RAG, Citations**

**🧭 You are here:** [Lab 0](lab-00.md) · [Lab 1](lab-01.md) · **▸ Lab 2** · [Lab 3](lab-03.md) · [Lab 4](lab-04.md) · [Lab 5](lab-05.md)  ·  🏠 [Workshop home](../../README.md)

---

> 🩺 **Mr. Rajan — Chapter 2**
> Reassured, the family asks: *"What diet should my father follow after heart failure?"* General
> advice isn't enough in healthcare — it has to be **grounded** in a trusted source they can point
> to. Care Pal answers and cites HealthHub, so the family knows where the guidance comes from.

## What you'll learn
The difference between *information* and *advice* is **provenance**. You'll attach **knowledge** to
your agent — a web-search tool plus a private **file-search (RAG)** index of curated HealthHub
discharge-care documents — and make every education answer carry citations.

> **📂 This lab, three ways — pick your rail:**
> 🟢 **Navigator** (portal, screenshots): **[lab-02-portal.md](lab-02-portal.md)** · 🟡 **Builder** (notebook): **[`lab2_rag.ipynb`](../assets/lab2_rag.ipynb)** · 🔴 **Engineer** (script): **[`lab2_rag.py`](../assets/lab2_rag.py)**

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
Open **[`lab2_rag.ipynb`](../assets/lab2_rag.ipynb)** and run it top to bottom — each cell explains the RAG round-trip inline. You
create a **vector store** from the HealthHub pack, attach a `FileSearchTool`, ask the diet question,
and check the reply carries a `healthhub.sg` citation. *(Web Search is also GA in the new API if you
want to ground on live pages — optional.)*

**Under the hood:** `build_vector_store(...)` uploads each file via the OpenAI-compatible client
(`openai.vector_stores.create` + `files.upload_and_poll`); `file_search_tool(vs_id)` wraps it as a
`FileSearchTool`, which you pass in `tools=[...]` on the agent definition so Foundry runs retrieval
automatically at answer time.

📚 **Docs:** [File search tool](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/file-search) ·
[Agent tools overview](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/overview) ·
sample: [`sample_agent_file_search.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_file_search.py)

## 🔴 Engineer — SDK
Run **[`lab2_rag.py`](../assets/lab2_rag.py)** and fill the `# 👉` lines. The goal: build a file-search index over the pack,
attach it to the grounded agent, and `assert` an education query returns ≥1 `healthhub.sg` citation.

**The SDK flow:**
1. **Build the index** — `build_vector_store(...)` creates a vector store and uploads every file
   (`openai.vector_stores.create` → `files.upload_and_poll`); Foundry chunks + embeds them.
2. **Wrap it as a tool** — `file_search_tool(vs_id)` → `FileSearchTool(vector_store_ids=[vs_id])`.
3. **Attach + run** — pass `tools=[fs]` on the `PromptAgentDefinition`; the model calls the retrieval
   tool automatically and returns passages you cite in `source_urls`.

```python
vs_id = build_vector_store("healthhub-discharge-pack")   # uploads the pack -> vector store
fs = file_search_tool(vs_id)                             # FileSearchTool(vector_store_ids=[vs_id])
agent = make_triage_agent(instructions=GROUNDING, tools=[fs], structured=True)
out = run_and_parse(agent, text_of("diet_question"))
assert any("healthhub.sg" in u for u in out["source_urls"]), out
```

📚 **Docs:** [File search tool](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/file-search) ·
[Agent tools overview](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/overview) ·
sample: [`sample_agent_file_search.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_file_search.py)

---

## ✅ Validation
Paste the JSON for **"What diet should my father follow after heart failure?"**
Passes when **`source_urls` is non-empty** *and* at least one URL is on the **`healthhub.sg`** host.

## 🎁 Optional challenge
Send the un-grounded question **"Can my father take a herbal supplement called LiverTone together
with his heart failure medication?"** Show that your agent **declines / qualifies** and routes to
`timely_review` — with **empty** `source_urls` (no fabricated citations). This is the safe behaviour.

## Stuck?
- No citations? Confirm the knowledge files **finished indexing**, and that your instructions tell
  the agent to *populate* `source_urls` from the knowledge base.
- Citations point somewhere other than HealthHub? Tighten the instruction to prefer the attached
  pack; web search is a supplement, not the primary source.

---

### 🧭 Where next?
⬅️ Previous: [Lab 1 · Triage Agent](lab-01.md) — 🏠 [Workshop flow & rails](../../README.md#how-the-workshop-flows) — Next: [Lab 3 · Govern & Observe](lab-03.md) ➡️

> 🟢 **Navigator?** Screenshot walkthrough for this lab: **[lab-02-portal.md](lab-02-portal.md)** · index: [PORTAL-TRACK.md](PORTAL-TRACK.md)
