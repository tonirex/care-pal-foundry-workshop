# HealthHub Discharge-Care Knowledge Pack — manifest

Lab 2 grounds the Education path in a small, curated set of post-discharge self-care documents.
This folder is the **source** the operator loads into a Foundry **file-search / vector store** index
before the workshop (or attaches via the portal **Knowledge → Upload files**).

> ⚠️ **Content owner action required.** The URLs below mirror the articles the customer's Care Pal
> agent already cites (from the playground screenshots). **Seeded synthetic stand-ins are already in
> `heart/ kidney/ liver/ general/`** so Lab 2/4 grounding works out of the box. Before go-live, the
> content owner should **verify each link**, download the current text over the synthetic file, and
> confirm redistribution is acceptable for an internal workshop. Labs and answer keys only require
> that grounded answers cite a `healthhub.sg` host, not a specific article.

## Allow-list host (used by validators)
`healthhub.sg`, `www.healthhub.sg`

## Heart failure (Mr. Rajan's condition — primary)
| File | Title | Source URL |
|------|-------|-----------|
| heart/heart-failure-fluid-salt.md | Heart Failure — Monitoring Fluid and Salt Intake | https://www.healthhub.sg/health-conditions/heart-failure-monitoring-fluid-and-salt-intake |
| heart/heart-failure-medication.md | Heart Failure — Medication | https://www.healthhub.sg/health-conditions/heart-failure-medication |

## Kidney (used by the verbatim "kidney failure" demo prompt)
| File | Title | Source URL |
|------|-------|-----------|
| kidney/chronic-kidney-disease.md | Chronic Kidney Disease | https://www.healthhub.sg/health-conditions/chronic_kidney_disease_nuh |
| kidney/kidney-failure.md | Kidney Failure in Singapore | https://www.healthhub.sg/health-conditions/kidney-failure |
| kidney/peritoneal-dialysis.md | What is Peritoneal Dialysis | https://www.healthhub.sg/health-conditions/what-is-peritoneal-dialysis |

## Liver (third supported condition)
| File | Title | Source URL |
|------|-------|-----------|
| liver/liver-care-after-discharge.md | Caring for Your Liver After Discharge | https://www.healthhub.sg/ (confirm exact article) |

## General discharge
| File | Title | Source URL |
|------|-------|-----------|
| general/discharge-care-plans.md | Support & Care Programmes — Discharge Care Plans | https://www.healthhub.sg/support-and-care-tools/support-and-care-programmes-stroke-rehabilitation-and-discharge-care-plans |

## Intentionally NOT covered (drives the Lab 2 bonus)
Herbal-supplement / drug-interaction questions (e.g. the `unsupported_question` prompt) are **out of
scope on purpose** — so participants can prove their agent declines instead of fabricating sources.
