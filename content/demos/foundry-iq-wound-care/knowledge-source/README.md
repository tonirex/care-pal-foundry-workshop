# Wound-care knowledge source — Foundry IQ demo

These three Word documents are the **knowledge source** for the
[Foundry IQ wound-care demo](../README.md). Upload them to an Azure Blob Storage container
(`woundcare`) and index them with a Foundry IQ knowledge base (`ks-woundcare`). The agent then
answers wound-care questions **only** from these documents — with citations.

Each `.docx` is curated from a public source article (navigation/marketing removed, structure
preserved) and records its **source URL** inside the document so the agent can cite it.

## Documents

| File | Title | Source URL | Host |
|------|-------|-----------|------|
| `healthhub-wound-care.docx` | Wound Care | https://www.healthhub.sg/health-conditions/wound-care | healthhub.sg |
| `slh-wound-care-treatment.docx` | Wound Care Treatment in Singapore: How to Heal Faster and Avoid Complications | https://www.slh.org.sg/wound-care-treatment-in-singapore-how-to-heal-faster-and-avoid-complications/ | slh.org.sg |
| `slh-managing-chronic-wounds.docx` | Managing Chronic Wounds (Caring for Chronic Wounds) | https://www.slh.org.sg/managing-chronic-wounds/ | slh.org.sg |

## Allow-list hosts (for graded labs' validators, if reused)
`healthhub.sg`, `www.healthhub.sg`, `slh.org.sg`, `www.slh.org.sg`

## Regenerate / edit the documents
The `.docx` are generated from curated content in **`build_docs.py`** (that script is the editable
source of truth). A clinician or content owner can adjust the wording — the exact text that grounds
the agent's answers — and rebuild before go-live:

```bash
pip install python-docx
python build_docs.py      # rewrites the 3 .docx next to this script
```

## What's intentionally NOT covered (drives the "graceful decline" demo)
Burns, insect **stings** and jellyfish stings, and **specific drug dosing** are out of scope — the
source articles hand those off elsewhere. Asking about them is how you show the agent **declines**
instead of inventing an answer or a citation.

> ⚠️ Curated from public Singapore health sources for an **internal workshop demo** — **not medical
> advice**. Verify redistribution terms before any external use.
