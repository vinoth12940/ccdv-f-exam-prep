"""2.5 Understanding Requirements (3.4%) and Systems Life Cycle (2.8%)

D2 Applications & Integration · 33.1% of the exam.

These two skills are judgement, not code. Work the scenario below — the
exam phrases items exactly this way.

**Scenario.** A claims team wants an assistant that drafts denial-letter
explanations. Legal requires every letter to cite the specific policy
clause. Security requires that no PII leaves the company's cloud region.
Volume is ~3,000 letters per night, reviewed by humans the next morning.

**Derive the requirements:**

Type · Requirement — Drives
Functional · Cite the governing clause in every letter
    Retrieval of clause text into context; a validator that rejects
    uncited output
Functional · Human review before a letter is sent
    HITL approval gate; the system never sends directly
Functional · Deterministic, auditable output format
    Structured output + schema validation
Infrastructure · No PII outside the region
    Region-pinned inference; PII redaction before the call
Infrastructure · 3,000/night, read next morning
    Batch API — nobody is waiting, so pay half

The constraint that most shapes the architecture is the regional one: it
governs which endpoint you may call at all, before any model-quality
question is on the table.

**Life cycle.** The phase most people under-plan is Maintain. For a Claude
system that specifically means: re-running your eval suite when a new model
version ships, keeping the pin until those evals pass, versioning prompt
changes like code, and monitoring output-validation failure rates as a
production signal that model behaviour has shifted.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""
