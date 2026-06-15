# MeshIQ Teams Agent (Copilot Studio)

Two capabilities: Q&A over evaluations, and human-in-the-loop approval.

## Build order
1. Create agent in Copilot Studio — SAME environment as Dataverse.
2. Knowledge > add Dataverse tables (Recording, Evaluation, Client, Job).
3. Topic "Evaluation lookup" -> question node -> Call action (Power Automate
   flow that List rows from Dataverse with a filter) -> Message node formats reply.
4. Approval flow:
   - Trigger: Evaluation row pending review (or called from the orchestration flow)
   - Action: "Post adaptive card and wait for a response" to a Teams user
     (use approval_card.json)
   - On response: Update the Evaluation row's Review Status to the chosen
     decision (approved / rejected), set reviewer + timestamp.
5. Publish agent > Channels > Microsoft Teams > add. Test in Teams.

## approval_card.json
Adaptive card with score, recommendation, confidence, reasoning, citations, and
Approve / Reject buttons. The button "data.decision" value flows back into the
flow so you can branch on approved vs rejected.

## Demo tips
- Pre-load a couple of evaluations so Q&A has data to show.
- For the approval demo, trigger the card on the Globex violation evaluation —
  the manager sees the violations, the citations, and clicks Reject (or Approve
  to escalate). One tap writes the decision back to Dataverse.
- The human-in-the-loop step is your biggest Reliability & Safety differentiator
  — make sure the demo lingers on it.

## First-time gotchas
- Wrong environment selected = agent can't see Dataverse. Check top-right selector.
- Adaptive card field refs depend on how your flow passes the evaluation data;
  adjust the @{...} bindings to match your trigger/compose outputs.
- Publish the agent after every change before testing in Teams.
