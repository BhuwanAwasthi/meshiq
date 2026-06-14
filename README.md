# MeshIQ — Multi-Agent Recording Evaluation Platform

**One line:** MeshIQ automatically ingests any meeting or call recording, figures out what it is, routes it to the right specialist AI evaluator, and scores it against the correct rulebook — interviews against a job description, support/QA calls against the specific client's guidelines — with grounded citations and a human-in-the-loop approval step in Microsoft Teams.

> Submitted to **Agents League Hackathon 2026** — Reasoning Agents, Enterprise Agents, and Creative Apps tracks.

---

## The problem

In any BPO, recruiting team, or contact center, recordings pile up faster than humans can review them. A QA supervisor manually reviews calls for compliance; a recruiter re-watches interviews to score candidates. The work is slow, inconsistent between reviewers, and creates audit risk. Worse, the *rules differ per context* — every client has its own QA standards, every role its own bar — so a single rigid checklist doesn't work.

**MeshIQ removes the manual triage and first-pass evaluation entirely**, while keeping a human in control of the final decision.

---

## What makes it different

Most submissions are a single agent answering questions. MeshIQ is a **multi-agent system with an orchestrator** that *understands the input before acting on it*:

- A **Router Agent** classifies each recording (interview vs QA call) and identifies its target (which role, or which client) — then dispatches to the right specialist. No fixed pipeline; the system decides.
- Two **Specialist Evaluators** each apply a different, dynamically-retrieved rulebook and produce a visible step-by-step reasoning trace with citations.
- A **human-in-the-loop approval** in Teams gates every action — nothing is finalized without a person clicking Approve/Reject.
- **Confidence-based escalation** — when the router or an evaluator is unsure, it refuses to guess and routes to human review instead.

---

## Architecture

![MeshIQ architecture](architecture/diagram.png)

**Flow:** recording/transcript arrives → **Router Agent** (Microsoft Foundry) classifies + identifies target → **Power Automate** orchestrates the dispatch → correct **Specialist Evaluator** (Foundry) scores against the rulebook retrieved from **Foundry IQ** → results written to **Dataverse** → **adaptive card** posted to **Teams** for human approval → decision written back to Dataverse.

| Layer | Technology |
|---|---|
| Agents (router + 2 evaluators) | Microsoft Foundry |
| Grounded rulebook retrieval | **Foundry IQ** (Azure AI Search index over JDs + client guidelines) |
| Orchestration | Power Automate (AI Foundry connector + Dataverse connector) |
| Data + audit trail | Dataverse |
| Human-in-the-loop | Teams adaptive cards (via Power Automate) |
| Conversational Q&A | Copilot Studio agent |
| Dashboard | React, built with GitHub Copilot |

---

## IQ integration (Foundry IQ)

Every compliance and competency finding is **grounded and cited**. The rulebooks (client QA guidelines and job descriptions) are indexed into a single Foundry IQ knowledge layer with metadata tags. At evaluation time, the specialist evaluator retrieves **only the relevant rulebook** for the target the router identified — Globex's regulated collections rules for a Globex call, the Senior Python Developer rubric for that interview — and cites the specific rule behind each finding.

This is a deliberately *deeper* use of Foundry IQ than generic "cited answers": the grounding is **dynamic and per-target**, and it scales to any number of clients or roles just by adding a tagged document — no re-architecting.

*(Planned second IQ: Fabric IQ knowledge graph over the Dataverse evaluation entities, enabling cross-cutting questions like "which agents have the most critical violations across all clients." See Roadmap.)*

---

## Responsible AI & reliability

- **Human-in-the-loop:** every evaluation that fails, scores low, or is low-confidence triggers a Teams approval card; the human decision is recorded.
- **Confidence thresholds:** router and evaluators output a confidence score; below threshold → `human_review`, never a silent guess.
- **Grounded, cited findings:** no compliance verdict without a citation to the source rule — reduces hallucination and makes every decision auditable.
- **Model pinning:** the underlying model deployment is version-pinned to avoid silent behavior drift between runs.
- **Full audit trail:** every recording and evaluation, including the reasoning trace and the human decision, is persisted in Dataverse.

---

## Demo

▶️ **Video:** [PASTE YOUR DEMO VIDEO LINK]

The demo runs a regulated collections call with stacked violations (missing debt-collection disclosure, disclosure of account details to a third party, and threats) through the live pipeline. Watch the router identify the client, the evaluator catch all three regulated breaches with citations, and the approval card land in Teams for a one-click decision.

---

## Evaluation

Tested on a labeled set of 6 synthetic transcripts (2 interviews against one JD; 4 QA calls across 2 clients, including a regulated multi-violation hard case). The harness runs the **production pipeline**, not a separate rig.

| Metric | Result |
|---|---|
| Routing (type) accuracy | [PASTE] |
| Target identification accuracy | [PASTE] |
| Outcome accuracy (pass/fail, hire/no-hire) | [PASTE] |

Scoring script and answer key in [`/eval-harness`](eval-harness/).

---

## Engineering notes (real constraints, real decisions)

Built across a multi-tenant setup (Foundry in one tenant, Dataverse in another). Two constraints shaped the architecture, and routing around them cleanly is part of the story:

1. **Foundry agents were Entra-only (API keys disabled)** in the sandbox, so a direct Azure Function call was rejected (401). **Resolution:** moved orchestration to Power Automate, whose AI Foundry connector authenticates with the trusted identity — which also collapsed the cross-tenant Dataverse hop since Power Automate and Dataverse share a tenant.
2. **Copilot Studio publishing required a license** not available. **Resolution:** delivered the Teams human-in-the-loop via Power Automate adaptive cards (no license needed); the conversational agent runs in Copilot Studio. The approval capability — the part that matters — is fully functional either way.

---

## Repository structure

```
meshiq/
├── README.md
├── architecture/           architecture diagram
├── router-agent/           router system prompt
├── interview-evaluator/    interview evaluator system prompt
├── qa-evaluator/           QA evaluator system prompt
├── flow/                   Power Automate orchestration (parse schemas, notes)
├── control-room/           Teams adaptive card + approval handling
├── eval-harness/           scoring script + answer key + results
├── dashboard/              React dashboard (GitHub Copilot)
└── docs/                   rulebooks + test data
```

## Roadmap

- **Fabric IQ** knowledge graph over evaluations for cross-client trend analysis (second IQ layer).
- **Live Teams auto-ingestion** via Graph change notifications (currently: drop-transcript trigger).
- Bulk historical re-evaluation and per-agent coaching reports.

---

*Built for Agents League Hackathon 2026.*
