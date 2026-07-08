# 🧠 Foundry IQ Spotlight — Grounded Wound-Care Advice (Demo)

> **Not a graded lab.** This is a standalone **facilitator demo** (~15–20 min) you can run any time
> after [Lab 2 · Knowledge & Grounding](../../labs/lab-02.md). It is **not** wired into
> `config/workshop.yaml`, has no points or badge, and no participant validator.

> 🩺 **Mr. Rajan — side story**
> Weeks into his recovery, Priya notices a small sore on her father's foot that isn't healing — Rajan
> is diabetic as well as living with heart failure. She asks Care Pal: *"How should we look after a
> wound that won't heal?"* In healthcare, the answer can't be a confident guess from a chatbot's
> memory or a random web page — it has to come from **trusted, governed sources** the care team
> approves. This demo shows how **Foundry IQ** makes that guarantee.

---

## Why this demo (the one thing to land)

Lab 2 grounds answers with **file-search RAG + optional web search**. This demo goes one step
further and shows **Foundry IQ**: a **managed knowledge base** (backed by Azure AI Search) that the
agent queries as its **single source of truth**.

The teaching contrast is deliberate:

| | Model's own knowledge | Open web search | **Foundry IQ knowledge base** |
|---|---|---|---|
| Where the answer comes from | LLM training data | Whatever a search returns | **Only the documents you curated** |
| Can you audit / govern it? | No | Hard | **Yes — you own every doc** |
| Citations back to a trusted source | No | Sometimes | **Yes, every time** |
| Behaviour when it doesn't know | May confidently make things up | May surface a bad page | **Says "not in my sources" and defers** |

We prove — live — that the agent's wound-care answers come **from the knowledge base and nowhere
else**: not its own LLM knowledge, and not the web.

---

## What you'll build

1. A **Foundry IQ knowledge base** over three curated Singapore wound-care documents (see
   [`knowledge-source/`](knowledge-source/)).
2. An agent whose instructions **force knowledge-base-only grounding** with citations.
3. A quick playground demo that shows grounded answers **with citations**, a graceful **decline**
   when the question is out of scope, and a "**prove it's grounded**" moment.

The **knowledge source** is three `.docx` files already prepared for you in
[`knowledge-source/`](knowledge-source/):

| File | Source | Host |
|------|--------|------|
| `healthhub-wound-care.docx` | HealthHub — *Wound Care* | healthhub.sg |
| `slh-wound-care-treatment.docx` | St Luke's Hospital — *Wound Care Treatment in Singapore* | slh.org.sg |
| `slh-managing-chronic-wounds.docx` | St Luke's Hospital — *Caring for Chronic Wounds* | slh.org.sg |

---

## Prerequisites (facilitator)

- A **Foundry project** with the **New Foundry** experience turned **On** (same as the labs).
- Permission to **create an Azure AI Search resource** and a **Storage account** (Foundry IQ needs
  both). This is beyond *Foundry User* — run this demo from a facilitator/admin identity, not a
  participant login.
- A deployed **embedding model** (e.g. `text-embedding-3-small`) **and** a chat model (the workshop's
  `model-router` / `gpt-5.4-mini` works, or `gpt-5` / `gpt-4o`). Foundry IQ needs an embedding model
  to index the documents — deploy one first if you haven't.
- The three `.docx` files in [`knowledge-source/`](knowledge-source/).

> This demo maps step-for-step onto Microsoft Learn exercise
> **[04 · Integrate an AI agent with Foundry IQ](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/04-integrate-agent-with-foundry-iq.html)**.
> The only changes are the **domain** (Contoso camping products → Singapore wound care), the
> **documents** (`contoso-products.zip` PDFs → our three wound-care `.docx`), and — importantly — an
> **extra step to remove the default Web search tool** so grounding is provably knowledge-base-only.
> A full mapping table is at the [end of this page](#what-changed-vs-the-microsoft-learn-tutorial).

---

## Part 1 · Create the knowledge base (Foundry IQ)

### 1a. Create the agent
1. In the [Foundry portal](https://ai.azure.com), open your project and confirm the **New Foundry**
   toggle is **On**.
2. **Build → Agents → Create agent**. Name it `woundcare-iq-agent` (facilitators sharing a project may
   prefix their initials, e.g. `woundcare-iq-<initials>`). It deploys a default chat model.

### 1b. Give it grounded instructions
In the agent's **Instructions**, paste the following. This is the heart of the demo — it forbids the
model from answering out of its own head or the web:

```text
You are Care Pal's wound-care information assistant for patients and caregivers in Singapore.

Answer ONLY using information retrieved from the connected Foundry IQ knowledge base of curated
wound-care documents. Treat that knowledge base as your single source of truth.

- ALWAYS search the knowledge base before answering any wound-care question.
- Base every statement strictly on the retrieved passages. Do NOT use your own general medical
  knowledge, prior training, or any outside/web information to fill gaps.
- Always cite your sources: give the document title and its healthhub.sg or slh.org.sg source URL.
- If the knowledge base does not contain the answer, say clearly that you do not have that
  information in your wound-care sources, and advise the person to consult their own care provider
  or a wound clinician. Do NOT guess, and do NOT invent sources.
- You are a demo assistant, not a doctor. For severe bleeding, signs of serious infection, or other
  emergencies, tell the person to seek urgent medical care.
```

Select **Save**.

### 1c. Connect Foundry IQ to an AI Search resource
1. In the **Knowledge** section, expand **Add → Connect to Foundry IQ**.
2. Choose **Connect to an AI Search resource → Create new resource** and create it with defaults:
   - **Resource name**: a globally unique name (e.g. `srch-woundcare-<unique>`)
   - **Subscription / Resource group / Region**: same as your project
   - **Pricing tier**: **Free** if available, otherwise **Basic**

### 1d. Upload the wound-care documents to Blob Storage
1. Open the [Azure portal](https://portal.azure.com) in a new tab → search **Storage accounts** →
   **Create** with defaults (same subscription/resource group/region, Standard, LRS). Name it
   something unique like `stwoundcare<unique>`.
2. Open the storage account → **Upload** → create a new container named **`woundcare`**.
3. Upload the **three `.docx` files** from [`knowledge-source/`](knowledge-source/):
   `healthhub-wound-care.docx`, `slh-wound-care-treatment.docx`, `slh-managing-chronic-wounds.docx`.
4. Navigate to your **search service** → **Security + networking → Keys** → set **API Access control**
   to **Both**, confirm, and leave this tab open.

### 1e. Create the knowledge base
1. Back in the Foundry tab, refresh, confirm you're on the **Knowledge** page, then
   **Create a knowledge base** → choose **Azure Blob Storage** as the knowledge source → **Connect**.
2. Configure the knowledge source:
   - **Name**: `ks-woundcare`
   - **Description**: `Curated Singapore wound-care guidance (HealthHub + St Luke's Hospital)`
   - **Storage account name**: your storage account
   - **Container name**: `woundcare`
   - **Authentication type**: **API Key**
   - **Content extraction mode**: **minimal**
   - **Embedding model**: your deployed embedding model (e.g. `text-embedding-3-small`)
   - **Chat completions model**: your deployed chat model (e.g. `gpt-5` / the workshop model)
3. **Create**. On the knowledge-base page, pick your chat model from the **Chat completions model**
   dropdown, then **Save knowledge base**. Refresh until the source status is **active**.
4. Return to the **Knowledge** page → **Manage** (next to the *Connection* dropdown) → **Connected
   resources** → select your search-service row → **Authentication** → **Key authentication → Edit
   authentication**. Paste a key from the Azure portal **Keys** tab and **Save**.

Foundry IQ is now wired up. ✅

---

## Part 2 · Make it grounded-only (remove Web search) ⚠️

> **This is the step the base tutorial doesn't have — and the one that makes the demo honest.**

When you create an agent in the portal, Foundry adds a **Web search** tool **by default**. If you
leave it on, you can't prove an answer came from your documents rather than the open web.

1. On the agent's page, look at the **Tools** panel.
2. If a **Web search** (Bing) tool is present, **remove it** (⋯ menu → **Remove**).
3. Confirm the **only** knowledge/tool attached is your **Foundry IQ** knowledge base
   (`ks-woundcare`).
4. **Save.**

Now the agent has exactly one way to find facts: your wound-care knowledge base.

---

## Part 3 · Demo it in the playground

Open the agent's **playground** and make sure the **Foundry IQ** knowledge (connection +
`ks-woundcare`) is selected.

### 3a. Grounded answers (should cite a source)
Ask these — each is answered by the documents, so the agent should reply **and cite** a `healthhub.sg`
or `slh.org.sg` source:

- `How should I care for a small cut or abrasion at home?`
- `What should someone with a slow-healing wound eat to help it heal?`
- `What are the three tips for taking care of a chronic wound?`
- `When should we see a doctor about my father's wound?`

Point out in each response: **specific guidance from the docs** + a **citation** back to the source
document. This is *advice with provenance*, not a chatbot opinion.

### 3b. Graceful decline (out of scope → no making things up)
Ask something the knowledge base **doesn't** cover. The agent should say it doesn't have that in its
sources and suggest a care provider — **without inventing** an answer or a citation:

- `How do I treat a jellyfish sting?`  *(the docs explicitly hand stings off to a separate article)*
- `What antibiotic and dosage should I take for an infected wound?`  *(no dosing in the docs)*

### 3c. 🔬 Prove it's grounded (the money moment)
This shows the good answers really came from the knowledge base — not the model's memory or the web.

1. Ask a question you **know** the model could answer from general training, e.g.
   `What foods are high in zinc?` → it answers **and cites** the St Luke's chronic-wounds doc.
2. Now **temporarily detach** the `ks-woundcare` knowledge base from the agent (Knowledge → remove),
   **Save**, and ask the **same question again**.
3. With no knowledge base and no web search, the agent now **can't answer from its sources** and
   defers — even though the base LLM obviously "knows" about zinc. That gap is the proof: the earlier
   answer came from **your governed documents**, exactly what Foundry IQ guarantees.
4. **Re-attach** `ks-woundcare` and **Save** to restore the demo.

> **✅ Validated behaviour.** This flow was tested end-to-end against Azure AI Search using
> *these exact documents* (chunked, embedded with `text-embedding-3-small`, hybrid + semantic
> retrieval). In-scope questions — wound healing, infection signs, chronic-wound care — returned
> specific guidance **with citations** to `healthhub.sg` / `slh.org.sg`. Out-of-scope questions
> (`ibuprofen dosage`, `jellyfish sting`, even `What is the capital of France?`) **all returned the
> grounded decline** instead of a model-knowledge answer — which is the whole point.

---

## Part 4 · (Optional, 🔴 Engineer) Drive it from code

For the engineer rail, a small runnable client lives in [`app/`](app/). It connects to the agent by
name and, following the base tutorial, requires **human approval** before each Foundry IQ lookup so
you can *see* the knowledge-base call happen.

```bash
cd content/demos/foundry-iq-wound-care/app
python -m venv .venv
# Windows:  .venv\Scripts\Activate.ps1     macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
az login
cp .env.example .env    # set PROJECT_ENDPOINT and AGENT_NAME (woundcare-iq-agent)
python agent_client.py
```

To exercise the approval flow, first set the agent to **ask for approval for all tools** using the
**Foundry Toolkit for VS Code** extension (Prompt Agents → your agent → Tools → *Ask for approval for
all tools*). Then in the client, type a wound-care question, approve the lookup when prompted, and
watch the grounded, cited answer come back. Type `history` to review the conversation, `quit` to exit.

See [`app/README.md`](app/README.md) for details.

---

## What changed vs the Microsoft Learn tutorial

Base exercise:
**[04 · Integrate an AI agent with Foundry IQ](https://microsoftlearning.github.io/mslearn-ai-agents/Instructions/Exercises/04-integrate-agent-with-foundry-iq.html)**.

| Tutorial step | This demo |
|---|---|
| Domain: Contoso outdoor/camping products | **Singapore wound care** (Care Pal side story) |
| Data: `contoso-products.zip` (3 PDFs) | **3 curated `.docx`** in [`knowledge-source/`](knowledge-source/) |
| Container `contosoproducts`, KB `ks-contosoproducts` | Container **`woundcare`**, KB **`ks-woundcare`** |
| Agent `product-expert-agent` | Agent **`woundcare-iq-agent`** |
| Instructions: "search the knowledge base… cite sources" | **Stricter**: KB is the *only* source; **no LLM/general knowledge, no web**; decline + defer when unknown |
| Web search tool left as-is (portal default) | **Removed** — the added Part 2, so grounding is provably KB-only |
| Test queries about tents/backpacks | **Wound-care queries** + an **out-of-scope decline** + a **"prove it's grounded"** step |
| `agent_client.py` (fill 2 TODOs) | Same flow, **completed & adapted** in [`app/`](app/) (wound-care prompts) |

Everything else — creating the project, the AI Search resource, the Blob Storage source, the
knowledge base, the key-auth wiring, and the optional MCP-approval client — follows the tutorial.

---

## Talking points

- **Provenance beats fluency.** A grounded "here's what the guideline says, and here's the link"
  beats a confident-but-unsourced answer every time in healthcare.
- **You govern the corpus.** Swap, update, or remove a document and the agent's answers change with
  it — no retraining, no prompt surgery.
- **Safe failure.** "I don't have that in my sources, please ask your care provider" is the *correct*
  answer when the knowledge base is silent.

## Teardown

To avoid ongoing cost after the demo, delete the **Azure AI Search** resource and the **Storage
account** you created (or the whole demo resource group). The agent and knowledge base can be
deleted from the Foundry portal.

---

> ⚠️ **Content note.** The three documents are curated from public Singapore health sources
> (HealthHub, St Luke's Hospital) for an **internal workshop demo** and are **not medical advice**.
> Each file records its source URL. Verify redistribution terms before any external use.

### 🧭 Where next?
🏠 [Workshop flow & rails](../../../README.md#how-the-workshop-flows) ·
📚 [Lab 2 · Knowledge & Grounding](../../labs/lab-02.md) ·
🧠 [What is Foundry IQ?](https://learn.microsoft.com/azure/foundry/agents/concepts/what-is-foundry-iq) ·
🔗 [Connect an agent to a knowledge base](https://learn.microsoft.com/azure/foundry/agents/how-to/foundry-iq-connect)
