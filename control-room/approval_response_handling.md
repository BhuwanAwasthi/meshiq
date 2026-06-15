# Approval card — response handling in Power Automate

These steps go at the END of your existing orchestration flow, after the
Evaluation row is created.

## 1. Condition — does this need human review?
Add a Condition. Post the card if ANY of these is true:
- body('Parse_qa')?['needs_human_review'] is true
- body('Parse_qa')?['overall_score'] is less than your threshold (e.g. 85 for
  Globex, 80 for Acme)
- body('Parse_qa')?['result'] equals 'fail'
(Use the interview equivalents on the interview branch.)

## 2. Post the adaptive card and wait
Action: "Post adaptive card in a chat or channel and wait for a response"
- Post as: Flow bot
- Post in: Chat with Flow bot (or a Group chat / channel for the demo)
- Recipient: the manager's email (yourself for the demo)
- Message: paste approval_card.json, replacing the @{...} bindings with your
  actual Parse JSON / Compose references.

NOTE on arrays: reasoning_trace and citations are arrays. Before the card,
add Compose actions:
  composeReasoning = join(body('Parse_qa')?['reasoning_trace'], '
')
  composeCitations = join(body('Parse_qa')?['citations'], '; ')
Then reference outputs('composeReasoning') / outputs('composeCitations') in
the card.

## 3. Read the decision
The wait action returns the submitted data. The clicked button sets:
  data.decision = "approved" | "rejected"
Reference it as:
  body('Post_adaptive_card_and_wait')?['data']?['decision']
(name matches your action)

## 4. Update Dataverse
Action: Dataverse "Update a row" on the Evaluation table
- Row ID: the Evaluation row created earlier in the flow
- Review Status: outputs of the decision (approved / rejected)
- Reviewer: the manager (or triggerOutputs user)
- Review timestamp: utcNow()

## Demo note
This is your human-in-the-loop. The Globex violation evaluation is the best one
to show: card displays the regulated violations + citations, manager clicks
Reject, Dataverse review status flips to 'rejected'. That full loop is the
Reliability & Safety story.

## Fallback if "wait for response" is awkward on a timer
Use "Post a card" (non-blocking) + a separate automated flow triggered by the
Teams card response, OR pre-stage the card before recording so it's already
sitting in the chat ready to click.
