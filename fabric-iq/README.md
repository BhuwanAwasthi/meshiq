# MeshIQ — Fabric IQ (second IQ layer)

MeshIQ uses two complementary IQ layers:
- **Foundry IQ** = document grounding ("what is the rule?") — used at evaluation time.
- **Fabric IQ**  = entity reasoning ("what is the pattern?") — used for analytics.

Microsoft positions Fabric IQ as the shared context layer that grounds
Foundry-built agents, so pairing the two is a legitimate "Best Use of IQ" story.

## What is implemented

1. **Zero-copy Dataverse → Fabric link.** The four operational tables (Recording,
   Evaluation, Client, Job) are mirrored into Microsoft Fabric (OneLake) with no
   ETL and stay in sync automatically. Operational data stays in Dataverse.
2. **Analytics report over the mirrored data.** A Power BI report on the Fabric
   Lakehouse surfaces cross-cutting patterns the per-document Foundry IQ layer
   structurally cannot answer, e.g.:
   - failed QA evaluations by client (which client breaches most, and which rules)
   - candidate scores by role (interview outcomes against each JD)
   - recordings parked in human_review

This demonstrates the second IQ layer end to end: data flows from the live
pipeline into Dataverse, mirrors into Fabric zero-copy, and is reasoned over for
cross-entity insight.

## Setup (as built)

### Step 1 — Fabric capacity
app.fabric.microsoft.com (same tenant as Dataverse), start a trial or use capacity.

### Step 2 — Link Dataverse to Fabric (zero-copy)
make.powerapps.com > environment > Analyze > Link to Microsoft Fabric.
- If "environment isn't configured for use with Fabric": enable Fabric linking
  on the environment (admin), then retry.
- The four tables appear in the Fabric Lakehouse and stay in sync.

### Step 3 — Build the report
On the Lakehouse, build a Power BI report:
- Bar: count of Evaluations where result = fail, grouped by detected_target (client)
- Bar: average overall_score grouped by role (interview evaluations)
- Table: recordings where status = needs_review

## Next step (documented, not yet built): the ontology graph

A full Fabric IQ ontology would model the entities + relationships
(Recording --produces--> Evaluation; Evaluation --scored_against--> Client|Job)
and allow a Fabric Data Agent to answer the same questions in natural language.
The ontology tooling is in preview; the link + report above already deliver the
two-IQ capability, and the ontology is the natural enhancement.

## For the README / submission (accurate wording)

"MeshIQ uses two complementary IQ layers. Foundry IQ grounds each evaluation in
the correct rulebook with citations. Fabric IQ links the evaluation entities into
Microsoft Fabric via zero-copy Dataverse integration and reasons over them with an
analytics report — surfacing per-client violation trends and candidate scores by
role that document retrieval alone cannot. A full Fabric IQ ontology graph is the
documented next step."
