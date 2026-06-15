# MeshIQ Eval Harness

Measures pipeline accuracy on the same Power Automate path used in production.

## How to run (no separate flow needed)
1. Run each of the 6 labeled transcripts through your normal orchestration flow
   (upload/trigger each one). They land in Dataverse as Recording + Evaluation rows.
2. Export the relevant columns from Dataverse to results.csv with headers:
   file,recording_type,detected_target,routing_decision,overall_score,recommendation
   - "file" must match the transcript file name in ground_truth.csv
   - For QA rows, recommendation = result (pass/fail)
   - For interview rows, recommendation = recommendation (hire/no_hire/etc)
3. Score it:
   python score_eval.py ground_truth.csv results.csv

## What it reports
- Routing (type) accuracy  — interview vs qa_call correct
- Target ID accuracy       — correct client/job identified (the router's hard job)
- Outcome accuracy         — pass/fail or hire/no-hire matches expectation

## Files
- score_eval.py       the scorer
- ground_truth.csv    the answer key (6 transcripts)
- results_sample.csv  example results so you can see the script run
- results.csv         YOU create this from the Dataverse export

## For the README / submission
Paste the summary block into your project README under "Evaluation". Example:
    Routing accuracy:    100% (6/6)
    Target ID accuracy:  100% (6/6)
    Outcome accuracy:    100% (6/6)
Then note the test set composition (2 interviews, 4 QA across 2 clients,
including a regulated multi-violation hard case) and that the harness runs the
production pipeline, not a separate rig.

## Honesty note
If a real run misses one (e.g. a borderline route), KEEP the real number and add
a line on what failed and why. A genuine 83% with analysis is more credible to
judges than a suspicious 100%, and it demonstrates real evaluation rigor.
