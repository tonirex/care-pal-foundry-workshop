# Care Pal — Portal-only Track (🟢 Navigator) — Validated Walkthrough

Screenshot-based guides for participants who stay in the **Microsoft Foundry portal** (no SDK/notebooks).
Validated live on a real project (`steng-proj1`, agent `carepal-kc`, gpt-5 auto-deploy).

| # | Lab | What you build | Guide |
|---|-----|----------------|-------|
| 0 | Setup & first agent | Create agent, consent + refusal | [lab-00-portal.md](lab-00-portal.md) |
| 1 | Triage | Structured JSON, route to escalation | [lab-01-portal.md](lab-01-portal.md) |
| 2 | Knowledge & grounding | File-search knowledge + web search, cite healthhub.sg | [lab-02-portal.md](lab-02-portal.md) |
| 3 | Govern & observe | Guardrail, trace, auto-evals | [lab-03-portal.md](lab-03-portal.md) |
| 4 | Multi-agent | Workflows: triage→education→follow-up | [lab-04-portal.md](lab-04-portal.md) |
| 5 | Extend & deploy | MCP tool + hosted agent (demo) | [lab-05-portal.md](lab-05-portal.md) |

**Verified live:** Lab 0 refusal (Safety 100%) · Lab 1 chest-pain → `immediate_escalation` · Lab 2 diet answer cites 5 healthhub.sg URLs · Lab 3 inline trace shows web_search→message + 11 auto-evaluators (Coherence 5/5) · Lab 4 `carepal-multiagent` Sequential (triage→education→follow-up) all nodes ran green; education grounded in healthhub.sg + ntfgh.com.sg · Lab 5 MCP catalog + config form, Publish channels, Call-agent endpoint (azure-ai-projects ≥2.1.0).

Screenshots: `images/lab{0..4}-*.png`.
