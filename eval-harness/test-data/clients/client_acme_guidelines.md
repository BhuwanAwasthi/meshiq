# Client QA Guidelines — Acme Corporation

**Client ID:** CLIENT-ACME
**Client name:** Acme Corporation
**Service type:** Technical product support (B2C software)
**Match keywords:** Acme, AcmeCloud, Acme account, Acme subscription, order number AC-

## Call handling standards
Agents handling Acme calls must follow these rules. Each is scored pass/fail
by the QA evaluator, and the call receives an overall 1–100 score.

### 1. Opening (mandatory)
- Agent greets the caller and states their own name
- Agent states "Thank you for calling Acme support"
- Agent verifies the customer's identity using account email or order number

### 2. Verification (mandatory)
- Identity MUST be verified before any account details are discussed
- Discussing account specifics before verification is a critical violation

### 3. Tone and conduct
- Professional, empathetic tone throughout
- No interrupting the customer
- No blaming the customer for the customer

### 4. Resolution
- Agent confirms understanding of the issue before proposing a solution
- Agent provides a clear next step or resolution
- Agent offers a ticket/reference number for follow-up

### 5. Closing (mandatory)
- Agent asks "Is there anything else I can help you with?"
- Agent thanks the customer

## Scoring
- Each mandatory item missed = critical (-20 each)
- Tone/conduct issues = moderate (-10 each)
- Missing closing courtesy = minor (-5 each)
- A passing call scores 80+.
