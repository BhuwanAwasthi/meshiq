# MeshIQ — Power Automate Orchestrator

Power Automate replaces the Azure Function as the orchestrator. It lives in the
same tenant as Dataverse, and the AI Foundry connector authenticates with your
signed-in identity (which the company sandbox accepts), so no API keys, no
client secrets, no Key Vault, no cross-tenant auth.

## Flow structure
1. Trigger: new transcript (file created / manual / later: Teams).
2. AI Foundry connector -> MeshIQ-Router (pass transcript).
3. Parse JSON -> router_parse_schema.json
4. Switch on routing_decision:
   - interview_evaluator -> Foundry connector MeshIQ-Interview-Evaluator
       -> Parse JSON (interview_parse_schema.json)
   - qa_evaluator -> Foundry connector MeshIQ-QA-Evaluator
       -> Parse JSON (qa_parse_schema.json)
   - human_review (default) -> record only, flagged for review
5. Dataverse "Add a new row" -> Recording (router fields)
6. Dataverse "Add a new row" -> Evaluation (evaluator fields,
   lookup bound to the Recording row)

## Schemas in this folder
- router_parse_schema.json
- interview_parse_schema.json
- qa_parse_schema.json

## Why the Function failed (for the README write-up)
The company sandbox has key-based auth disabled (Entra-only). The Function's API
key was rejected (401/403). Power Automate's Foundry connector uses the
interactive/connection identity the sandbox trusts, so it succeeds. Moving
orchestration to Power Automate also removed the cross-tenant Dataverse hop.
