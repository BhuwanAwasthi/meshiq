# MeshIQ Dashboard (Creative Apps track — GitHub Copilot)

A unified board that reads the Dataverse evaluation data and shows:
- Candidate rankings against the job description (interview evaluations)
- QA call scores per client, with violations highlighted (qa evaluations)
- Drill-down into any evaluation's step-by-step reasoning trace + citations

Built with GitHub Copilot. See copilot-log.md for the build narrative
(prompts used, what Copilot generated, time saved).

## Stack
React + a charting lib (Recharts/Chart.js). Reads Dataverse via the Web API
(or a thin Power Automate "get rows" endpoint) — same data the Teams agent uses.
