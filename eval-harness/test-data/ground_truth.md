# Ground truth labels — eval harness answer key

This file is the answer key. The eval harness runs each transcript through the
router and the correct evaluator, then compares against these expected values.

## Interviews
| File | Expected type | Expected target (Job ID) | Expected outcome |
|------|---------------|--------------------------|------------------|
| interview_python_strong.txt | interview | JOB-001 (Senior Python Developer) | strong hire (overall 4+/5) |
| interview_python_weak.txt   | interview | JOB-001 (Senior Python Developer) | no hire (overall <=2/5) |

## QA calls
| File | Expected type | Expected target (Client ID) | Expected outcome |
|------|---------------|------------------------------|------------------|
| qa_acme_compliant.txt   | qa_call | CLIENT-ACME   | pass (score 80+) |
| qa_acme_violation.txt   | qa_call | CLIENT-ACME   | fail (no greeting/name, no verification = critical) |
| qa_globex_compliant.txt | qa_call | CLIENT-GLOBEX | pass (score 85+) |
| qa_globex_violation.txt | qa_call | CLIENT-GLOBEX | fail (no debt disclosure, third-party disclosure, threats = critical regulated) |

## What each transcript tests
- python_strong / python_weak: evaluator must discriminate quality against the same JD
- acme vs globex: ROUTER must identify the correct client from keywords in the call
- acme_violation: missing mandatory opening + skipped identity verification
- globex_violation: the hardest case — regulated violations (no disclosure,
  disclosed debt to a third party/roommate, made threats). The evaluator must
  catch all three and weight them as critical.
