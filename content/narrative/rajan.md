---
patient_id: HEART-DEMO-01
patient_name: Mr. Rajan Kumar
caregiver_name: Priya (daughter)
condition: Heart failure (post-discharge)
ward: NTFGH Ward 6A
note: All data is synthetic. No real patient is depicted.
---

# Mr. Rajan's Recovery — the thread through every lab

> Use the matching chapter as the opening paragraph of each lab. It gives non-technical
> participants a human reason for the Foundry feature they are about to build.

## Chapter 0 — Going home (Lab 0)
Mr. Rajan Kumar, 64, was discharged from NTFGH Ward 6A on a Tuesday afternoon after a
heart-failure admission. His daughter Priya helps him settle in at home and installs Care Pal
on his phone. That evening Rajan opens it and types a tentative "Hi". Before Care Pal can help
with anything, it has to introduce itself honestly — a demo assistant, not a doctor — and ask
for his consent.

## Chapter 1 — The first real message (Lab 1)
Two days later Rajan writes: *"I was discharged recently for heart failure."* It's vague — is he
worried about symptoms, medication, diet? Care Pal can't act safely until it understands the
**intent**, gauges the **risk**, and decides a **route**. This is the moment a friendly chatbot
becomes a triage agent.

## Chapter 2 — Advice he can trust (Lab 2)
Reassured, Rajan asks: *"What diet should my father follow after heart failure?"* (Priya is
typing now.) General advice isn't enough in healthcare — it has to be **grounded** in a trusted
source they can point to. Care Pal answers and cites HealthHub, so the family knows where the
guidance comes from.

## Chapter 3 — 2am (Lab 3)
On day four, at 2am, a message arrives: *"I have crushing chest pain and I can't breathe
properly."* This is exactly what Care Pal must **never** try to answer itself. The guardrails
fire, the agent escalates, and every step is captured in a trace the care team can audit in the
morning.

## Chapter 4 — Different needs, different help (Lab 4)
By day five Rajan is steadier. Priya asks two things at once: *"What follow-up appointments does
my father need, and what diet should he keep?"* Scheduling and education are different jobs — so
the triage agent hands off to specialist agents (Follow-Up and Education) and stitches their
answers into one reply.

## Chapter 5 — Always on (Lab 5)
A week in, Care Pal needs to do something real — check an actual follow-up appointment slot — and
it needs to be reachable at any hour, not just in a playground tab. The team gives it a tool
(via MCP) and deploys it as a hosted agent. *(And, only if there's time, they connect it to a
phone so Rajan can chat to it the way he really would.)*
