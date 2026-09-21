# CCDV-F — The Complete Study Guide

**Claude Certified Developer – Foundations · Exam code CCDV-F · Blueprint v1.0 (July 2026)**

This is the tutor. The notebooks are the lab. Read a section here, then run the
matching notebook, then come back and answer the self-check questions from
memory. That loop — explanation, hands-on, recall — is what makes this stick.
Reading alone will not get you to 720.

Every section below is tied to a specific notebook and a specific blueprint
skill with its official weight. Nothing here is exam content: the questions,
answer options, and scenarios are confidential under the NDA you accept before
the exam starts. Everything here is written against the published blueprint and
against the current Claude platform documentation.

---

## How to use this guide

Work in **weight order**, which is the order both this guide and the notebooks
already use. Section 1 of this guide pairs with `notebooks/01_...`, section 2
with `notebooks/02_...`, and so on down to section 8. The numbering is not the
blueprint's domain numbering — it is descending exam weight, because that is
the order that protects your score.

Here is the mapping, and it is worth internalising before you start:

| Guide § | Notebook | Blueprint domain | Weight | Approx. items of 53 |
|---|---|---|---|---|
| 1 | `01_domain2_applications_and_integration` | D2 Applications and Integration | 33.1% | ~18 |
| 2 | `02_domain5_model_selection_and_optimization` | D5 Model Selection and Optimization | 16.8% | ~9 |
| 3 | `03_domain1_agents_and_workflows` | D1 Agents and Workflows | 14.7% | ~8 |
| 4 | `04_domain6_prompt_and_context_engineering` | D6 Prompt and Context Engineering | 11.0% | ~6 |
| 5 | `05_domain8_tools_and_mcps` | D8 Tools and MCPs | 10.6% | ~6 |
| 6 | `06_domain7_security_and_safety` | D7 Security and Safety | 8.1% | ~4 |
| 7 | `07_domain3_claude_code` | D3 Claude Code | 3.1% | ~2 |
| 8 | `08_domain4_eval_testing_and_debugging` | D4 Eval, Testing, and Debugging | 2.6% | ~1 |

Look at the top two rows. **Domain 2 and Domain 5 together are half the exam.**
If you are short on time, that is where the time goes. The bottom two rows are
three items combined — worth understanding, not worth a weekend.

---

## Part 0 — What the exam actually is

Two facts from the official guide shape every study decision you make.

**It is criterion-referenced.** You are measured against a fixed standard that
subject-matter experts set by describing what a minimally qualified candidate
knows. You are not graded on a curve against other candidates. There is no
"beat the median" play and no comfort in a hard exam day — either you
demonstrate the competencies or you don't.

**The cut score is 720 on a 100–1,000 scale, across 53 items in 120 minutes.**
That is a shade over two minutes per item, which is generous for a
multiple-choice exam but not generous for one built from scenarios. Most items
will describe a situation — a team with a requirement, a system misbehaving, a
cost problem — and ask which approach fits. You cannot pattern-match your way
through those from a flashcard deck. You have to actually understand the
tradeoff being tested.

A few more mechanics worth holding:

- **Item format** is multiple-choice and multiple-response. Each item tells you
  how many responses to select. Read that line; a multiple-response item scored
  as all-or-nothing is an easy place to lose a point you knew.
- **Score reporting** is pass/fail plus a scaled score, plus percent-correct by
  domain. The domain percentages are diagnostic only — your pass/fail comes from
  the total scaled score. So a weak Domain 4 (2.6%) cannot sink you, and a weak
  Domain 2 (33.1%) almost certainly will.
- **Validity is 12 months.** This is a deliberately short-lived credential
  because the platform moves fast. Renewal is a free, non-proctored assessment
  if you do it on time; let it lapse and you retake the full exam at full fee.
- **Retakes** wait 14 days after a first failure, 30 after a second, 90 after a
  third, capped at four attempts per rolling twelve months, fee each time.

### The candidate the exam is written for

The blueprint describes a minimally qualified candidate as someone with one to
five years of software engineering and at least six months of hands-on work
with Claude or a comparable LLM system. They are proficient in Python and/or
TypeScript, fluent with REST APIs and CLI tools, and comfortable with LLM
fundamentals, agents, context management, and MCP.

Read that profile as a hint about item style. The exam is not testing whether
you can recite that `max_tokens` caps output length. It is testing whether,
handed a business requirement, you pick the architecture that meets it. That is
why roughly a fifth of Domain 2 — Understanding Requirements (3.4%), Systems
Life Cycle (2.8%), and Software Engineering Foundations (7.4%) together are
13.6% of the whole exam — is ordinary senior-engineer judgement with Claude
sprinkled on top. Do not skip those skills because they feel unglamorous. They
are worth more than Domains 1 and 4 combined.

### On recall posts and third-party practice questions

You will find posts where someone recounts what they remember from the exam, and
practice banks written against the public blueprint. Use both for calibration
and neither as a syllabus. A recall post reports what felt hard or novel to one
person on one day — its silence about a topic is not evidence that topic is
absent. And treat any claim that a practice set "matches the real exam" as a
warning rather than a recommendation: exam content is confidential and
non-disclosable, and material that close to the live bank is a problem for
whoever sourced it. The blueprint is the syllabus. Understanding is what passes.

---

## Part 0.5 — What changed in the API, and why it is on the exam

The notebooks were originally written against an earlier Claude API surface.
Eight cells used patterns that the current models now reject outright. **They
have been fixed** — every notebook runs end to end against `claude-sonnet-5`
today, verified by executing all eight top to bottom.

Do not skip this part just because the code works. Domain 5 explicitly tests
"breaking behaviour changes across model releases," and this is that phenomenon
in your own repository. It is also the reason three of the patterns you may have
learned elsewhere are now wrong answers.

### 1. Assistant prefill was removed

The old trick of seeding Claude's reply by appending an `assistant` message as
the last entry — `{"role": "assistant", "content": "{"}` — now returns:

```
400 invalid_request_error: This model does not support assistant message prefill.
```

It fails on `claude-sonnet-5`, `claude-opus-5`, and the whole 4.6-and-later
family.

**What replaced it: structured outputs.** Rather than nudging the model toward
JSON, the API constrains generation so the response must satisfy your schema.
Two forms, and the notebooks now demonstrate both:

- `client.messages.parse(..., output_format=YourPydanticModel)` returns a
  validated object in `response.parsed_output`. See `extract_claim_json` and
  `decide_claim` in notebook 01.
- `client.messages.create(..., output_config={"format": {"type": "json_schema",
  "schema": {...}}})` takes raw JSON Schema. See `plan_subtasks` in notebook 03,
  `check_coverage` in notebook 04, and `get_verdict` in notebook 08.

Watch the naming: on `create()` it is `output_config={"format": ...}`. A bare
top-level `output_format` on `create()` is the deprecated spelling. (The
`parse()` helper does take `output_format=` — that is the SDK helper's own
argument, not the deprecated wire parameter.)

Worth knowing precisely, because it changes what your validation code is for:
**structured outputs enforce the schema constraints too, not just the JSON
shape.** Field patterns, enums, and numeric bounds are all honoured. I confirmed
this by asking for a claim id of `x9` against a `^[A-Z]{3}-\d{3}$` pattern — the
model returned `UNK-009` rather than violating the schema. So a validation loop
is no longer defending against malformed output; it defends against what a
schema cannot express — cross-field rules, business invariants, checks against
your own data. Notebook 01's `decide_claim` now demonstrates exactly that.

**Exam relevance.** Output Handling (2.6%) and Claude API Mechanics (6.8%). If
an item asks how to guarantee parseable, schema-valid output, the answer is a
schema constraint — not a prefill, and not a politely-worded prompt.

### 2. Sampling parameters were removed

`temperature`, `top_p`, and `top_k` are gone on the current models. In
`anthropic` 1.7.0 the SDK does not even accept the keyword — you get a
`TypeError` before a request is sent.

**What to understand instead.** Non-determinism has not gone away; it is still a
real property of these models and still testable. What changed is that you no
longer tune it with a dial. Depth and spend are controlled with
`output_config.effort`; output shape is controlled with structured outputs.

Notebook 02's `sample_repeatedly` now demonstrates something more useful than a
temperature sweep: **how much variation you get depends on how constrained the
output is.** An open-ended generation varies on essentially every run; a
one-word classification is stable in practice. "Stable in practice" is not a
contract, so a test asserting exact equality is still wrong — but knowing which
of your calls are volatile and which are not is real engineering information.

If an item offers "raise the temperature" as an option, it is a distractor on
current models. Note it was already a distractor in the official sample question
on prompt injection, for an entirely different reason.

### 3. `budget_tokens` extended thinking was removed

```python
thinking={"type": "enabled", "budget_tokens": 2000}   # 400 on current models
```

Returns `"thinking.type.enabled" is not supported for this model`.

**What replaced it: adaptive thinking.** Use `thinking={"type": "adaptive"}` and
let the model decide when and how deeply to think. Depth and overall spend are
steered separately through `output_config={"effort": ...}` with levels `low`,
`medium`, `high`, `xhigh`, `max` (default `high`). Notebook 02's
`answer_at_effort` now runs the same reasoning puzzle at two effort levels so
you can see the token difference.

This is the most important API change for Domain 5, because LLM Fundamentals
(5.2%) names "extended thinking, adaptive thinking, effort levels" as testable
content. The fixed-token-budget model is the *old* concept; adaptive thinking
plus effort is what replaced it.

Two details that are easy to get wrong:

- On Claude Opus 5, thinking is **on by default** — omitting the `thinking`
  parameter runs adaptive. That differs from Opus 4.8/4.7, where omitting it
  meant no thinking at all.
- **`effort` is model-gated.** Haiku 4.5 rejects it with a 400. This is why
  notebook 01's `ClaudeConfig` — whose production profile pins Haiku — carries
  no effort field.

### 4. What was *not* affected

Two things that look like prefill but are fine, so you do not over-correct:

- **Few-shot examples using assistant turns.** In notebook 04, the
  `{"role": "assistant", "content": "APPROVE"}` messages are followed by further
  user turns. An assistant message that is not the last entry is an ordinary
  conversation turn, not a prefill. Verified still working.
- **Appending the model's own reply to history.** `messages.append({"role":
  "assistant", "content": response.content})` in the agent loops is how
  stateless multi-turn conversation works. Correct and required.

Also `claude-haiku-4-5-20251001`, the dated ID the notebooks pin, resolves fine
on a live account. Model-version pinning is a Configuration Management (4.1%)
practice, and the notebook is demonstrating it deliberately.

### 5. Current model facts to study from

| Model | ID | Context | Input $/1M | Output $/1M |
|---|---|---|---|---|
| Claude Opus 5 | `claude-opus-5` | 1M | $5.00 | $25.00 |
| Claude Sonnet 5 | `claude-sonnet-5` | 1M | $2.00 | $10.00 |
| Claude Haiku 4.5 | `claude-haiku-4-5` | 200K | $1.00 | $5.00 |

Learn the shape rather than the digits: Sonnet is roughly 2.5× cheaper than
Opus, Haiku roughly 2× cheaper again, and Haiku is the only one of the three
with a 200K rather than 1M context window. That context-window difference is an
architectural constraint, not trivia — it is why a long-document workload cannot
simply be downgraded to Haiku to save money.

## Part 1 — Domain 2: Applications and Integration (33.1%)

→ **Lab: `notebooks/01_domain2_applications_and_integration.ipynb`**

A third of the exam. If you only deeply learn one domain, learn this one. Six
skills sit under it, and they are not evenly weighted:

| Skill | Weight |
|---|---|
| Claude Application Design | 8.6% |
| Software Engineering Foundations | 7.4% |
| Claude API Mechanics | 6.8% |
| Configuration Management | 4.1% |
| Understanding Requirements | 3.4% |
| Systems Life Cycle | 2.8% |

Notice what is at the top. It is not API mechanics. **Design decisions outrank
API trivia**, and general software engineering outranks Claude specifics. This
domain is testing an engineer who happens to work with Claude, not a person who
has memorised the Messages API.

### 2.1 Claude API Mechanics (6.8%)

*Lab: notebook 01, § 2.1*

The single most important mental model, and the one most likely to appear in
disguise: **`response.content` is a list of typed blocks, not a string.**

A response can contain `text` blocks, `tool_use` blocks, `thinking` blocks, and
more, in any order and any combination. Code that reaches for
`response.content[0].text` works right up until the model thinks before it
speaks or calls a tool first, and then it throws an `AttributeError` in
production. The correct accessor filters by type:

```python
def extract_text(response) -> str:
    return "".join(b.text for b in response.content if b.type == "text")
```

The notebook's `describe_response` and `extract_text` exist entirely to drill
this. Run them, then deliberately break one by indexing position zero, so you
feel the failure.

**`system` is a separate parameter, not a message.** Instructions about *how
Claude should behave* — the persistent role, the output contract, the
constraints — go in `system`. The conversation goes in `messages`. Putting
persistent instructions in a user message works less reliably and re-sends them
as conversational content on every turn. This same distinction reappears in
Domain 6 as "system versus user placement," so you are learning it twice for
two different slices of the exam.

**Streaming delivers incremental events so a UI can render as tokens arrive.**
Learn this one as a trap: *streaming does not reduce cost.* You pay for exactly
the same tokens. It improves perceived latency in an interactive interface, and
it avoids HTTP timeouts on long generations, and that is all. When a scenario
says "we need to reduce cost on a chat feature," streaming is the wrong answer;
caching or a smaller model is the right one.

**Realtime versus batch is a pure latency-tolerance decision.** The Message
Batches API processes large asynchronous workloads within a 24-hour window at
50% off both input and output tokens. The decision rule is one question: *does a
human sit waiting for this response?* If yes, realtime. If it can land within 24
hours, batch, every time, for half the cost. The official sample question in the
exam guide tests exactly this with 10,000 overnight documents — and the
distractors are instructive. Sending synchronous requests in parallel does not
reduce per-token cost. Lowering `max_tokens` does not address the batch tradeoff.
Downsizing the model blindly trades quality you were not asked to trade.

One practical detail the notebook demonstrates and the exam may probe: batch
results come back in **any order**. Key them by `custom_id`, never by position.

**Multi-format input.** The blueprint lists vision under API mechanics. Images
go in as `image` content blocks (base64 or URL); PDFs go in as `document`
blocks. Citations can be enabled per document block, which splits the response
into text blocks carrying a `citations` array. The Files API lets you upload
once and reference by `file_id` across many requests rather than re-uploading.

**Third-party vendors.** The blueprint explicitly mentions "invoking Claude
through third-party vendors." Claude is available through Amazon Bedrock,
Google Vertex AI, and Microsoft Foundry in addition to the first-party API. The
things to hold: each has a dedicated client class rather than a `base_url`
override, model IDs differ by platform (Bedrock prefixes with `anthropic.`,
Vertex uses `@` for dated snapshots), authentication differs (Vertex uses GCP
ADC, no Anthropic key), and **feature availability is not uniform** — some
capabilities are first-party only. That last point is the likely exam angle: a
scenario where a team on a cloud marketplace needs a feature their platform
doesn't carry.

### 2.2 Software Engineering Foundations (7.4%)

*Lab: notebook 01, § 2.2*

The second-heaviest skill in the heaviest domain, and the one candidates most
often under-prepare because it looks like it isn't about Claude. It largely
isn't. It is REST, JSON, async, version control, SDLC integration, code review,
and refactoring — applied to a system that happens to call an LLM.

**Async matters here for a concrete reason.** LLM calls are slow and
I/O-bound. A loop that awaits ten sequential calls takes ten times one call; the
same ten dispatched concurrently take roughly as long as the slowest. The
notebook's `compare_sequential_and_concurrent` measures this. Understand *why*
the speedup exists — you are overlapping network waits, not parallelising
compute — because a scenario may ask about throughput versus rate limits, and
the answer changes once you are rate-limited rather than latency-bound.

**Error typing and retry strategy is the other half.** Not all failures deserve
a retry. The discipline:

- **Retry with exponential backoff**: `429` rate limits, `5xx` server errors,
  connection and timeout errors. These are transient.
- **Do not retry**: `400` bad request, `401` authentication, `403` permission,
  `404` not found. Retrying a malformed request just produces the same error
  more expensively.

The official SDK already retries 408/409/429/5xx twice by default with backoff.
The exam-relevant insight is knowing *which* class an error falls into and why a
blanket `except APIError: retry` is a bug — it turns a permanent
misconfiguration into an expensive loop. Catch a most-specific-first chain
instead.

Worth noting for the same skill: SDK timeouts default to ten minutes, and
because timeouts are themselves retried, worst-case wall-clock is
`timeout × (max_retries + 1)`.

### 2.3 Claude Application Design (8.6%)

*Lab: notebook 01, § 2.3*

The heaviest single skill on the exam. It covers how Claude interprets
instructions across interfaces, content boundaries, schema design, session
hygiene, and plugin management.

**Instructions land differently across surfaces.** The same sentence behaves
differently in Claude Code, in the Desktop app, on claude.ai, through the raw
API, and through an SDK. The API is stateless and carries exactly what you send.
Claude Code carries a project's `CLAUDE.md`, its settings, its skills. A prompt
that relies on ambient project context works in one surface and silently
under-performs in another. Designing for a surface means knowing what that
surface supplies for free and what you must supply yourself.

**Content boundaries are a design concern, not only a security one.** When you
put untrusted content — a user-submitted document, a scraped page, a tool
result — into a prompt, mark it as data. Wrap it in delimiters, label it
explicitly as untrusted, and state that instructions inside it are not to be
followed. This reappears with force in Domain 7, but the exam tests it here as
*design*: the point is that the boundary is drawn at design time, in the shape
of the prompt, not patched in later.

**Schema design and defensive parsing.** Do not trust that the model returned
what you asked for. Define the contract — the notebook uses a Pydantic model
with field patterns and bounds — validate against it, and have a repair path.
The notebook's `decide_claim` demonstrates the key refinement: when validation
fails, send the *specific* validation error back to the model. A bare retry
usually reproduces the same mistake; telling the model exactly what was wrong is
what makes the second attempt useful.

That cell now uses `client.messages.parse()`, which means the schema — including
field patterns and numeric bounds — is guaranteed before your code sees the
object. Read the loop for what it defends against *now*: the business rule that
a low-confidence answer must be `REVIEW`, which no schema can express. That is
the durable lesson, and Part 0.5 explains why it moved.

**Session hygiene** means deciding what carries across turns and what does not.
The API is stateless — you resend history every request — so growing history is
growing cost and growing drift. Domain 6 covers the mechanics of pruning and
compaction; here the question is the policy: what *should* persist.

### 2.4 Configuration Management (4.1%)

*Lab: notebook 01, § 2.4*

CLAUDE.md files, settings.json, model version pinning, prompt versioning,
plugin dependencies.

**Pin your model version.** "Latest" is not a configuration; it is a promise to
be surprised. Model releases can change behaviour in ways that break a prompt
tuned against the previous one — the blueprint calls this out explicitly under
Domain 5 as "breaking behavior changes across model releases." Pinning an exact
model ID makes your system reproducible and makes upgrades a deliberate,
testable event rather than something that happens to you on a Tuesday.

**Version your prompts the same way you version code.** A prompt is production
configuration. It belongs in version control, it should be reviewable in a diff,
and a change to it should be traceable to a deployment. The notebook's
`RunConfig` dataclass models this: model, max_tokens, and a
`system_prompt_version` travelling together as one recorded unit, so that when
output quality moves you can say which change moved it.

The dataclass used to carry a `temperature` field; sampling parameters no longer
exist on current models, so it is gone (Part 0.5). Note also what was *not* put
in its place: `effort` is model-gated and this config pins Haiku 4.5, which
rejects it — a small but real lesson about configuration shapes that have to
span models of different capability.

### 2.5 Understanding Requirements (3.4%) and Systems Life Cycle (2.8%)

*Lab: notebook 01, § 2.5*

Together 6.2% — more than Domain 4 and Domain 3 combined. These are the "read
the scenario properly" skills, and they are almost entirely about translating a
stated business need into a technical constraint.

The move to practise: for any scenario, separate the **functional** requirement
(what it must do) from the **infrastructure** requirement (what it must run on,
within what limits) and from the **quality attributes** (how fast, how cheap,
how reliable, how private). Most exam scenarios bury the deciding constraint in
one clause — "results are not needed until the following morning," "the data
cannot leave our VPC," "this is on the checkout path." Find that clause and the
answer usually follows.

Systems Life Cycle is the ordinary discipline of developing, implementing,
operating, and maintaining a system, applied to one with a non-deterministic
component. The wrinkle worth holding: an LLM system's behaviour can change
without your code changing — through a model update, a prompt edit, or drift in
the input distribution. That makes **monitoring and evaluation operational
concerns, not just pre-launch gates**, and it makes model pinning part of your
release process rather than a nicety.

### Self-check — Domain 2

Answer these out loud before moving on. If you hesitate, re-run the notebook.

1. Why is `response.content[0].text` a latent bug, and what breaks it first?
2. A chat feature is too expensive. Why is streaming not the fix, and what are?
3. 10,000 documents, needed by morning, cost-sensitive. Which API, and why are
   the three obvious alternatives wrong?
4. Which HTTP status codes do you retry, which do you not, and why does the
   distinction matter more than the retry itself?
5. Your model provider ships a new version. Name three things in your system
   that should have made that a non-event.
6. What does `system` give you that the same text in a user message does not?

---

## Part 2 — Domain 5: Model Selection and Optimization (16.8%)

→ **Lab: `notebooks/02_domain5_model_selection_and_optimization.ipynb`**

The second-heaviest domain, and the one where the platform has changed most
since these notebooks were written. Four skills:

| Skill | Weight |
|---|---|
| Technical Fundamentals | 6.1% |
| LLM Fundamentals | 5.2% |
| Cost and Token Management | 2.8% |
| Model Selection and Tradeoffs | 2.7% |

The ordering is counter-intuitive again: the two "fundamentals" skills are 11.3%
of the exam between them, while the skill actually named "Model Selection" is
2.7%. Do not spend your Domain 5 study time only on the Opus/Sonnet/Haiku
comparison table.

### 5.1 LLM Fundamentals (5.2%)

*Lab: notebook 02, § 5.1*

The blueprint lists three clusters here: basic LLM behaviour, model options, and
fundamental prompting techniques.

**Tokens and context windows.** A token is roughly a word-piece; cost and limits
are both denominated in tokens, not characters or words. The context window is
the total budget for input plus output on a single request — 1M tokens on Opus 5
and Sonnet 5, 200K on Haiku 4.5. Two practical consequences: you cannot fit
"everything" and must decide what earns its place, and the window is shared, so
a long input eats into room for the answer.

Count tokens before you spend them. The `messages.count_tokens` endpoint gives
you the real number for a given model — do not estimate with a generic
tokeniser, because the tokenisation differs by model and an estimate that is
20% off is 20% off your cost projection. The notebook's `count_input_tokens` and
`enforce_token_budget` demonstrate the guard-before-you-call pattern.

**Non-determinism.** The same prompt can produce different outputs on different
calls. This is a property of how the model samples the next token, and it is
architecturally significant: it is why you cannot write an exact-match unit test
against model output, why an eval needs multiple samples to be meaningful, and
why "it worked when I tried it" is not evidence. Domain 4 builds directly on
this.

What has changed: you no longer control it with a `temperature` parameter. That
was removed (Part 0.5, item 2). Non-determinism is a fact you design around, not
a dial you turn.

**Model options — this is the part the blueprint names explicitly.** Four things
are listed, and all four are current platform features worth knowing by name:

- **Extended thinking / adaptive thinking.** The model reasons before answering.
  The modern form is `thinking={"type": "adaptive"}` — the model decides when and
  how much to think. The older fixed `budget_tokens` form is removed on current
  models. On Opus 5, adaptive thinking is on by default.
- **Effort levels.** `output_config={"effort": "low"|"medium"|"high"|"xhigh"|"max"}`,
  default `high`. This is the primary lever for trading thoroughness against
  token spend *within a single model*. Low effort suits subagents and simple
  tasks; high and above suit coding and long-horizon agentic work.
- **Fast mode.** The same model served at higher output tokens per second, at
  premium pricing. It is a latency lever, not a quality or cost lever.
- **Thinking display.** Whether reasoning is returned to you as a summary or
  omitted. Critically: **display does not change whether thinking happens or
  what it costs.** Thinking is billed the same either way.

That last point is a textbook exam trap. "Turn off thinking display to reduce
cost" is wrong; you would want lower `effort`.

**Zero-shot, single-shot, multi-shot.** Zero-shot is instructions only.
Single-shot adds one worked example. Multi-shot adds several. Examples are the
most reliable way to pin down an output format or a judgement boundary that
prose struggles to describe — but they cost input tokens on every call, which is
precisely why they are a good candidate for prompt caching.

### 5.2 Technical Fundamentals (6.1%)

*Lab: notebook 02, § 5.4*

The largest skill in this domain, and the vaguest-sounding: "foundational
technical concepts supporting AI application development, including basic
engineering practices (integrating with SDKs that wrap REST APIs, websockets)."

Read that as: **understand that the SDK is a convenience layer over an HTTP
API, and be able to reason at either level.** The notebook's `raw_rest_call`
makes the same request with `requests` that the SDK makes for you — same
endpoint, same `x-api-key` and `anthropic-version` headers, same JSON body. Run
it side by side with the SDK call until the equivalence is obvious.

Why this matters beyond trivia: when something goes wrong, the failure surfaces
at the HTTP layer. A `429` with a `retry-after` header, a `400` with a message
naming the offending parameter, a request ID you can quote in a support ticket
— these are all HTTP-level facts that the SDK wraps but does not hide. A
developer who only knows the SDK's happy path cannot debug the unhappy one.

The blueprint's mention of **websockets** points at the streaming/realtime
distinction: streaming over HTTP delivers server-sent incremental events, which
is what the Messages API does; a websocket is a bidirectional persistent
connection, which is a different shape and appropriate to different problems.

Two SDK behaviours worth knowing because they bite silently: retries are
automatic (default 2, on 408/409/429/5xx and connection errors), and the default
timeout is ten minutes. Neither is visible in your code, and both affect what
"the request failed" actually means.

### 5.3 Cost and Token Management (2.8%)

*Lab: notebook 02, § 5.2*

Token budgeting, cost modelling, and caching. Small weight, high practical
value, and the caching material is the part most likely to appear.

**Prompt caching is a prefix match.** That single sentence explains almost every
caching question. The request renders in a fixed order — `tools`, then `system`,
then `messages` — and the cache matches from the start of that rendering. **Any
byte change anywhere in the prefix invalidates everything after it.**

The design rule follows directly: put stable content first and volatile content
last. A frozen system prompt and a deterministically-ordered tool list at the
front; timestamps, per-request IDs, and the actual varying question at the back.

The economics: a cache write costs about 1.25× normal input tokens, a cache read
about 0.1×. So caching pays off from the second read onward, and the notebook's
`cache_breakeven` makes that arithmetic concrete. Default TTL is five minutes;
a one-hour TTL is available.

**The diagnostic to remember:** `usage.cache_read_input_tokens`. If it is zero
across requests you believe share a prefix, something is silently invalidating
it. The usual culprits are a `datetime.now()` in the system prompt, a
non-deterministically ordered `json.dumps()`, or a tool list that varies between
calls. There is also a minimum cacheable prefix — model-dependent, in the range
of roughly 512 to 4096 tokens — below which nothing caches and no error is
raised.

**Cost modelling** is just arithmetic done before the bill arrives: tokens in ×
input rate, plus tokens out × output rate, times request volume. What makes it
an exam skill is knowing which lever to pull. Ordered from free to costly:
caching first (no quality tradeoff), then batch where latency allows (50% off,
no quality tradeoff), then input-token hygiene, then effort level, then model
tier. Model downgrade is the *last* lever because it is the only one that
trades quality.

And judge cost per *completed task*, not per request. A cheaper model that needs
three attempts to get a usable answer is not cheaper.

### 5.4 Model Selection and Tradeoffs (2.7%)

*Lab: notebook 02, § 5.3*

Opus versus Sonnet versus Haiku, the quality/latency/cost triangle, and breaking
behaviour changes across releases.

The honest version of the tradeoff: **Opus** for the hardest reasoning and
long-horizon agentic work; **Sonnet** as the balanced default for most
production workloads; **Haiku** for simple, high-volume, latency-sensitive tasks
like classification or routing. The notebook's `recommend_model` encodes
decision criteria rather than a lookup table, which is the right instinct —
exam items describe workloads, not model names.

Two refinements that matter more than the tier table:

**Haiku's 200K context window is a hard constraint, not a preference.** Opus 5
and Sonnet 5 carry 1M. If the workload involves long documents or long agent
histories, the cheap tier may not be an option at all.

**Try lower effort on a better model before you downgrade the model.** A
capable model at `low` or `medium` effort often matches a weaker model at high
effort, and it keeps you in one cache namespace. Caches are model-scoped, so a
multi-model cascade forfeits cache reuse across its members — a real cost that
naive cascades ignore.

**Breaking behaviour changes** is the blueprint's own phrase, and Part 0.5 of
this guide is a live worked example: prefill, sampling parameters, and
`budget_tokens` all disappeared between the version these notebooks target and
the current one. That is exactly the phenomenon the skill is testing. The
defence is model pinning plus an eval suite you re-run on upgrade — which is why
Configuration Management and Domain 4 exist.

### Self-check — Domain 5

1. What is the difference between adaptive thinking and effort level? Which one
   would you change to reduce spend?
2. Does hiding thinking output reduce cost? Why or why not?
3. Your cache hit rate is zero. Name three things to check, in order.
4. Rank the cost levers from "free" to "trades quality."
5. When is Haiku not an option regardless of budget?
6. Why does a multi-model cost cascade sometimes cost more than one model?

---

## Part 3 — Domain 1: Agents and Workflows (14.7%)

→ **Lab: `notebooks/03_domain1_agents_and_workflows.ipynb`**

| Skill | Weight |
|---|---|
| Agent Construction with Claude | 5.3% |
| Agent Patterns and Frameworks | 4.9% |
| Agent Architecture | 4.5% |

Evenly weighted, which tells you the domain is tested as a whole rather than
through one favoured sub-topic.

### 1.1 Agent Architecture (4.5%)

*Lab: notebook 03, § 1.1*

**The decision this domain is built on: workflow or agent?**

A **workflow** has steps you determined in advance. Classify, then extract, then
summarise — the control flow lives in your code, the model fills in the
judgement at each step. It is predictable, debuggable, cheap, and testable. The
notebook's `claim_intake_workflow` is three sequential calls with your `if`
statements between them.

An **agent** decides its own steps. You give it tools and a goal; it loops,
choosing what to call and when to stop. It is flexible and it handles tasks you
could not fully specify in advance — at the cost of unpredictability, more
tokens, higher latency, and much harder debugging.

The test to apply, and the one exam scenarios are built around: **can you write
down the steps in advance?** If yes, it is a workflow, and using an agent is
over-engineering. If the steps genuinely depend on what is discovered along the
way, it is an agent.

Four criteria are worth checking before you commit to an agent:

- **Complexity** — is the task multi-step and hard to fully specify?
- **Value** — does the outcome justify higher cost and latency?
- **Viability** — is the model actually capable at this task?
- **Cost of error** — can mistakes be caught and recovered (tests, review,
  rollback)?

A "no" on any of them argues for a simpler tier.

**Manager/supervisor hierarchies and subagents.** A supervisor decomposes a task
and dispatches subtasks to subagents, each running in its own context. The point
that matters is **context isolation**: a subagent that reads fifty files returns
a summary, and the fifty files never enter the supervisor's context. That keeps
the main thread's context clean and is the primary reason the pattern exists —
not parallelism, though you get that too. This links straight to Context
Engineering in Domain 6.

### 1.2 Agent Construction with Claude (5.3%)

*Lab: notebook 03, § 1.2*

**The tool-use loop is the whole mechanism.** Learn this cycle until you can
draw it:

1. Send `messages` plus `tools`.
2. Response comes back with `stop_reason == "tool_use"` and one or more
   `tool_use` blocks.
3. Append the assistant message (the **full** `response.content`, not just text)
   to history.
4. Execute each tool, collect results.
5. Append **one** user message containing **all** the `tool_result` blocks.
6. Repeat until `stop_reason` is `end_turn`.

Two details in there are exam-grade:

**Parallel tool calls.** One assistant message may contain several `tool_use`
blocks. Execute them concurrently, then return all their `tool_result` blocks in
a *single* user message. Splitting them across multiple messages silently trains
the model to stop making parallel calls — a performance bug with no error
message.

**Tool errors belong in the `tool_result`, not in an exception.** When a tool
fails, return a `tool_result` with `is_error: true` and a description of what
went wrong. Do not drop the block and do not raise past the loop. The model can
read the error and adapt — retry with different arguments, try another tool,
or tell the user. Crashing the loop denies it that chance. The notebook's
`run_agent_with_error_handling` is the reference implementation.

**The four ways to build an agent**, which the blueprint gestures at with
"Claude Agent SDK, custom agent loops and harnesses, managed agent deployment
models (self-hosted vs. Anthropic-hosted)". Two independent questions separate
them: *who writes the harness* (the loop and context management) and *who owns
the deployment*.

| Approach | You write | Harness | Deployment | Built-in tools |
|---|---|---|---|---|
| **Manual loop** (Messages API) | the whole loop | you | you | none — yours only |
| **Tool Runner** (`client.beta.messages.tool_runner`) | just the tool functions | SDK | you | none — yours only |
| **Managed Agents** (REST, beta) | agent config + tool results | Anthropic | **Anthropic** | hosted sandbox: bash, files, code exec |
| **Claude Agent SDK** (separate product) | a prompt + options | SDK (Claude Code harness) | you | Read/Write/Edit/Bash/Glob/Grep/WebSearch |

Three things to hold from that table:

- **Only Managed Agents supplies managed deployment.** The other three all leave
  hosting to you. This is the self-hosted versus Anthropic-hosted distinction
  the blueprint names.
- **Tool Runner ≠ Claude Agent SDK.** They sound alike and are different
  packages. Tool Runner is a helper inside the regular Anthropic SDK that loops
  over tools *you* define. The Claude Agent SDK (`claude-agent-sdk` /
  `@anthropic-ai/claude-agent-sdk`) is Claude Code packaged as a library, with
  built-in file and shell tools, subagents, permissions, sessions, and hooks. It
  is Python and TypeScript only.
- **Start simple.** Most tasks are a single call or a workflow. Reach for an
  agent only when the task genuinely requires model-driven exploration.

### 1.3 Agent Patterns and Frameworks (4.9%)

*Lab: notebook 03, § 1.3*

The blueprint names tool-use loops, sub-agents, memory, and context-window
management as patterns, and Strands, LangGraph, and PydanticAI as examples of
agentic abstraction frameworks.

You do not need to have shipped LangGraph to answer these. You need to know what
category of problem such a framework solves: they provide graph or state-machine
structure over the loop, so that control flow, retries, branching, and
persistence are declared rather than hand-written. The tradeoff is the usual one
— structure and conventions in exchange for indirection and a dependency.

**Memory** as a pattern means state that survives beyond one context window. The
platform has a memory tool for this. Distinguish it from the two adjacent
context techniques, which is a distinction worth getting crisp because all three
sound similar:

- **Context editing** *clears* old content — for example dropping stale tool
  results from the history before the model sees them.
- **Compaction** *summarises* earlier context into a compact form when the
  conversation approaches a threshold.
- **Memory** *persists* selected information outside the conversation entirely,
  to be read back later.

Clear, summarise, persist. Three different answers to "the context is filling
up," appropriate to different situations.

### 1.4 Hooks (also Domain 7, 1.0%)

*Lab: notebook 03, § 1.4*

Hooks are the answer to a specific question: *how do you get deterministic
control over a non-deterministic system?*

A hook fires on a lifecycle event — before a tool runs, after a response, at
session start — and executes your code. Because it is your code, it always runs
and always behaves the same way. The notebook's `pre_tool_use_hook` blocks a
payment above a threshold before the tool executes.

The principle to carry into the exam: **if something absolutely must not happen,
a prompt instruction is not sufficient.** Prompts are probabilistic guidance;
they can be argued with, confused, or injected around. A hook is a deterministic
gate. When a scenario says "must never," look for the hook or the code-level
control, not the better-worded system prompt.

### 1.5 Managed versus self-hosted (part of 5.3%)

*Lab: notebook 03, § 1.5*

Self-hosted means you run the loop and the compute: maximum control, maximum
operational burden, and your infrastructure boundary. Anthropic-hosted (Managed
Agents) means Anthropic runs the loop and provisions a per-session container
where tools execute: far less to operate, persisted and versioned agent configs,
sessions that can run long, built-in scheduling — in exchange for running on
someone else's infrastructure.

The deciding questions in a scenario are usually about data residency and
control, not convenience. If the constraint is "the data cannot leave our
environment," that answers it.

### Self-check — Domain 1

1. State the workflow-versus-agent test in one sentence.
2. Why must all `tool_result` blocks for one turn go in a single user message?
3. A tool throws. What exactly do you send back, and why not just raise?
4. Name the four ways to build an agent and say which one supplies deployment.
5. A requirement says a destructive action must *never* happen unapproved. Where
   does that control live, and why not in the system prompt?
6. Clear, summarise, persist — match each to context editing, compaction, memory.

---

## Part 4 — Domain 6: Prompt and Context Engineering (11.0%)

→ **Lab: `notebooks/04_domain6_prompt_and_context_engineering.ipynb`**

| Skill | Weight |
|---|---|
| Prompt Engineering | 4.6% |
| Context Engineering | 3.8% |
| Output Handling | 2.6% |

### 6.1 Prompt Engineering (4.6%)

*Lab: notebook 04, § 6.1*

The blueprint lists instruction clarity, few-shot examples, system versus user
placement, output constraints, placement across components, iterative
refinement, prompt adjustment, and input sanitisation.

**Placement is the highest-value idea here**, and it is the one the exam can
test cleanly. Persistent behaviour goes in `system`. The specific request goes
in the user turn. Examples go where they establish the pattern before the real
input. The notebook's `prompt_everything_in_user` versus
`prompt_with_system_split` is a direct A/B — run both and read the difference.

Why the split works: the system prompt is a stable, privileged instruction
channel. It is also, not incidentally, the stable prefix that prompt caching
wants (Domain 5). Good placement and good caching are the same design decision
viewed from two angles.

**Few-shot examples** pin down what prose cannot. If you need a specific output
format, a consistent tone, or a judgement boundary ("this counts as REVIEW, that
counts as DENY"), two or three examples do more than a paragraph of description.
The notebook's `zero_shot` versus `multi_shot` shows the effect. Note that these
examples use assistant turns that are *followed by* further user turns — that is
an ordinary conversation, not a prefill, and it still works (Part 0.5, item 4).

**Output constraints** means telling the model the shape of the answer, not
hoping for it: "Respond with exactly one word: APPROVE, DENY, or REVIEW. Never
explain." Combined with a low `max_tokens`, this is both a quality control and a
cost control. On current models the strongest form of this is structured
outputs, which constrains the response at the API level rather than by
instruction.

**Input sanitisation** is where this domain touches Domain 7. Before untrusted
text enters a prompt, neutralise its ability to act like instructions: strip or
escape delimiters that mimic your prompt structure, cap length, and wrap the
content in an explicit "this is data" boundary. The notebook's `sanitise` and
`build_prompt` are the pattern. It is necessary and — as Domain 7 will drive
home — not sufficient on its own.

### 6.2 Context Engineering (3.8%)

*Lab: notebook 04, § 6.2*

Context window management, prevention of drift and bloat through tool-output
pruning and compaction, and context isolation through subagents.

**The core problem:** the API is stateless, so every turn you resend the entire
history. A long agent run accumulates tool results, and those tool results are
usually the bulk of the tokens. Left alone, the history grows until cost is
painful, latency is bad, and the model's attention is diluted across a lot of
stale material — **context drift**, where the model starts responding to
something from twenty turns ago rather than the current task.

Three techniques, matching the three from Domain 1:

- **Pruning.** Replace superseded tool results with a short placeholder. The
  notebook's `prune_tool_results` does exactly this, and `measure` shows the
  size drop. The signal survives; the bulk does not.
- **Compaction.** Summarise earlier turns into a condensed form. Available
  server-side on current models, where the API summarises automatically as
  context approaches a threshold. One critical implementation detail: you must
  append the full `response.content` back to your messages, because the
  compaction blocks in the response are what the API uses to replace the
  compacted history next turn. Extracting only the text silently loses the
  compaction state.
- **Isolation.** Give the context-heavy work to a subagent. It reads everything,
  returns a summary, and the raw material never touches the main context. This
  is the cleanest technique of the three because it prevents the bloat rather
  than cleaning it up.

### 6.3 Output Handling (2.6%)

*Lab: notebook 04, § 6.3*

"Structured output patterns, response validation, defensive parsing, and
**skepticism toward confident output**." That last phrase is the whole skill in
four words, and it is unusually direct about what is being tested.

Three layers, and you want all three:

1. **Structural validation.** Is it well-formed and does it match the schema?
   This is what structured outputs and Pydantic give you. The strongest version
   is `output_config={"format": ...}`, which constrains generation rather than
   checking after the fact.
2. **Semantic validation.** The notebook's `verify_semantically` — is the
   content *right*, not merely well-shaped? A perfectly valid JSON object can
   assert a claim amount that appears nowhere in the source document.
3. **Coverage checks.** `check_coverage` — did it handle everything it was
   given, or did it quietly drop three of the ten items?

The exam-relevant instinct: **fluent, confident, well-formatted output is not
evidence of correctness.** A model will produce a beautifully structured wrong
answer with no signal that anything is off. Validation is not paranoia; it is
the only thing standing between you and a silent error.

### Self-check — Domain 6

1. Why does putting persistent instructions in `system` help caching too?
2. What is context drift, and which three techniques address it?
3. When compacting server-side, what must you append to history, and what breaks
   if you only append the text?
4. Name the three layers of output validation and give a failure each one
   catches that the others miss.
5. Why is input sanitisation necessary but not sufficient?

---

## Part 5 — Domain 8: Tools and MCPs (10.6%)

→ **Lab: `notebooks/05_domain8_tools_and_mcps.ipynb`**

| Skill | Weight |
|---|---|
| Tool Implementation | 4.4% |
| Agentic Customization | 4.1% |
| MCP Server Development | 2.1% |

Note that **Agentic Customization — choosing between mechanisms — is worth
almost as much as building tools**, and twice as much as writing MCP servers.
The exam cares more about your judgement than your implementation.

### 8.1 Tool Implementation (4.4%)

*Lab: notebook 05, § 8.1*

**The tool description is a prompt.** This is the idea to leave with. The model
never sees your function body; it sees the name, the description, and the input
schema, and it decides from those alone whether and how to call the tool. A
vague description produces a tool that is called at the wrong times with the
wrong arguments, and the fix is in the description, not the code.

Write descriptions that say *when to use this and when not to*, not just what it
does. "Search claims by keyword. Use when the user describes a claim but does
not know its ID. Do not use when you already have a claim ID — use `get_claim`
instead." The notebook's `search_claims` / `get_claim` pair and the `which_tool`
exercise exist to make the ambiguity visible: two tools with overlapping
descriptions produce unreliable selection.

**Client-side versus server-side tools.** A client-side (custom) tool is one you
define and execute: the model emits a `tool_use` block, your code runs the
function, you send back a `tool_result`. A server-side tool runs on Anthropic's
infrastructure — web search, web fetch, code execution — you declare it in
`tools` and the results come back as content blocks in the same response, with
no execution loop on your side.

The distinction to hold for the exam: **with a server-side tool you do not write
an execution loop, and you do not control the execution environment.** With a
client-side tool you control everything and own everything, including the
security boundary.

One non-obvious behaviour: server-tool errors do not raise. A failed web search
returns HTTP 200 with a result block whose content is an error object. Code that
assumes success and indexes into the content will break confusingly.

**Approval patterns.** Some tool calls should not run unattended. The pattern is
to gate execution behind a check — a policy rule, a threshold, a human decision
— between the model's request and your execution. This is the same idea as hooks
in Domain 1 and approval gates in Domain 7, arriving from a third direction.
When three domains converge on one concept, it is worth over-learning.

**Tool set construction.** More tools is not better. Every tool definition costs
input tokens on every request, and overlapping tools degrade selection accuracy.
Keep the set small, make the boundaries crisp, and if the set must be large, the
platform offers tool search with `defer_loading` so definitions load on demand
rather than all at once.

### 8.2 MCP Server Development (2.1%)

*Lab: notebook 05, § 8.2*

The Model Context Protocol is an open protocol for exposing capabilities to LLM
applications. Three roles, and getting them straight is most of the skill:

- **Host** — the application the user interacts with (Claude Desktop, Claude
  Code, your app).
- **Client** — the connector inside the host that speaks MCP to one server.
- **Server** — the process exposing capabilities.

A server can expose three kinds of thing, and the exam may well test the
distinction because it is the part people blur:

- **Tools** — functions the model can call. Model-controlled.
- **Resources** — data the host can read, addressed by URI. Application-controlled.
- **Prompts** — reusable templates the user can invoke. User-controlled.

The notebook's `get_claim` (tool), `policy_manual` (resource), and
`triage_prompt` (prompt) map onto those three exactly.

**Transports.** `stdio` runs the server as a local subprocess communicating over
standard input and output — simple, local, no network exposure, and the natural
choice for a developer tool on your own machine. HTTP-based transport runs the
server as a network service, which is what you need when the server is remote or
shared between several clients.

**Why MCP rather than just writing tools.** This is the exam's angle, and the
official sample question in the guide tests precisely it: an internal service
that several Claude applications need, maintained independently of any one app.
Hard-coding the logic into each application's prompt is neither reusable nor
maintainable. An MCP server exposes it once, and every application connects to
the same server. **Reusability across applications and independent maintenance
are the deciding factors.**

If you are wiring the MCP connector through the API rather than a host
application, note that it takes two halves: an `mcp_servers` entry *and* a
matching `mcp_toolset` entry in `tools`. Declaring only the server is a
validation error.

### 8.3 Agentic Customization (4.1%)

*Lab: notebook 05, § 8.3*

Choosing among built-in tools, custom tools, Skills, and MCPs. Nearly as heavy
as tool implementation, and pure judgement — which makes it very well suited to
scenario items.

The decision, in the order you should consider it:

- **Built-in (server-side) tools** — when Anthropic already provides the
  capability. Web search, web fetch, code execution. No code, no hosting, no
  maintenance. Do not build what already exists. The counter-trap: built-in
  tools do **not** reach arbitrary internal APIs, which is exactly the
  distractor in the official sample question.
- **Custom tools** — when the capability is specific to one application and you
  control the runtime. Fastest path when reuse is not a requirement.
- **Skills** — when what you need is *procedural knowledge* rather than a new
  capability: a checklist, a house style, a multi-step process. A skill is
  instructions and supporting files that load on demand, not a function.
- **MCP servers** — when the capability must be **reusable across applications**
  and **maintained independently**. This is the differentiator; if a scenario
  emphasises either phrase, MCP is the answer.

A useful compression: built-in if it exists, custom if it is yours alone, a
skill if it is knowledge rather than capability, MCP if it must be shared.

### Self-check — Domain 8

1. Why is the tool description a prompt, and what does a bad one cause?
2. Client-side versus server-side tool: what do you write differently, and what
   do you give up?
3. Tools, resources, prompts — who controls each?
4. stdio versus HTTP transport: when does each fit?
5. Which two phrases in a scenario point at MCP rather than a custom tool?
6. When is a Skill the right answer instead of a tool?

---

## Part 6 — Domain 7: Security and Safety (8.1%)

→ **Lab: `notebooks/06_domain7_security_and_safety.ipynb`**

| Skill | Weight |
|---|---|
| AI Application Security | 3.2% |
| Guardrails and Safe Deployment | 2.3% |
| Identity, Secrets, and Key Management | 1.6% |
| Claude Hooks | 1.0% |

### 7.1 AI Application Security (3.2%)

*Lab: notebook 06, § 7.1*

**Prompt injection is the headline threat, and the official sample question
tests it directly.** The scenario: an agent summarises user-submitted web pages,
and one page contains hidden text telling the model to ignore its instructions
and reveal its system prompt.

Work through why each defence does or does not hold, because the reasoning
generalises to any injection item you will see:

- **Raising temperature** — irrelevant. Injection is not a determinism problem.
  (And on current models the parameter no longer exists.)
- **Asking users not to include malicious instructions** — not an enforceable
  control. An attacker is not bound by your politeness.
- **Switching to a larger, more instruction-following model** — can make things
  *worse*, not better. A model that follows instructions more reliably follows
  injected instructions more reliably too. This is the most instructive
  distractor on the whole sample exam.
- **Treating retrieved content as untrusted, isolating it from trusted
  instructions, and enforcing guardrails so injected text cannot trigger
  sensitive actions** — correct, and note that it is *three* things, not one.

That three-part shape is the real lesson. The notebook builds it in stages:
`summarise_naively` shows the failure, `summarise_with_isolation` adds the
boundary, and then — crucially — a section titled *"Prompt-level defence is
necessary but not sufficient"* shows an injected call that **satisfies the
stated policy**. Sit with that one. It is the deepest idea in the domain: a
sufficiently clever injection produces a request that looks legitimate, and no
amount of prompt hardening catches it. What catches it is the architecture —
least privilege, so the model simply cannot invoke the dangerous capability, and
a deterministic gate on the actions that matter.

**Data leakage and PII.** Untrusted input flows in; sensitive data must not flow
out. The notebook's `redact` / `restore` pattern replaces sensitive values with
tokens before the prompt is sent and restores them after the response returns —
so the model never sees the real values but the output is still usable. Also
hold the basics the blueprint names: authentication, authorization,
confidentiality, privacy, integrity.

### 7.2 Guardrails and Safe Deployment (2.3%)

*Lab: notebook 06, § 7.2*

**Guardrail layering** is the concept. No single control is sufficient, so you
stack controls that fail in different ways: input sanitisation, then content
boundaries in the prompt, then constrained tool permissions, then deterministic
gates on dangerous actions, then monitoring and logging. An injection that
defeats layer one still meets layer four.

**Secure-by-design** means privacy, identity and access management, and **least
privilege** designed in from the start rather than bolted on. Least privilege is
the one that does the most work in this domain: if the agent has no tool that
can issue a payment, no prompt injection can make it issue a payment. Capability
you did not grant cannot be abused.

**Human-in-the-loop approval gates.** The notebook's `request_approval` /
`human_decides` / `gated_call` chain is the reference. The design question is
*which* actions need a human: the answer is those that are irreversible, costly,
or outside the blast radius you are willing to accept. Everything reversible and
cheap should run unattended, or the system is useless.

### 7.3 Identity, Secrets, and Key Management (1.6%)

*Lab: notebook 06, § 7.3*

Managing secrets, credentials, and API keys across development and production,
plus identity validation, access approval, and access monitoring.

The practices are ordinary and the exam will expect them: keys in environment
variables or a secrets manager, never in source; `.env` gitignored and
`.env.example` committed with placeholders; separate keys per environment;
rotation; least-privilege scoping; and monitoring of who used what.

There is a Claude-specific wrinkle worth knowing, and the notebook's
`scan_prompt_for_secrets` addresses it: **a key can leak through the prompt, not
just through the repo.** A user pasting a stack trace, a tool returning a config
file, an agent reading `.env` as part of a task — all put a live credential into
a context window that may be logged. Scan outbound prompts, not only commits.

This repository practises what it teaches: `.gitignore` excludes `.env` and
`*.key`, `.env.example` carries a placeholder, and the one `sk-ant-` string in
the notebooks is a deliberate fake inside the redaction lesson.

### 7.4 Claude Hooks (1.0%)

*Lab: notebook 03, § 1.4 — the hooks material lives in the agents notebook*

The smallest skill on the exam at 1.0%, roughly half an item. Covered under
Domain 1 above. The one sentence to carry: **hooks give deterministic
enforcement over a probabilistic system, which is why "must never" requirements
belong in a hook rather than a prompt.**

### Self-check — Domain 7

1. Why can a more instruction-following model be *worse* against injection?
2. Name the three parts of a correct injection defence.
3. What does "the injected call meets the policy" demonstrate, and what stops it?
4. Which actions warrant a human gate, and which should not have one?
5. Name two ways an API key leaks that `.gitignore` does not prevent.
6. Explain least privilege in one sentence using an agent and a payment tool.

---

## Part 7 — Domain 3: Claude Code (3.1%)

→ **Lab: `notebooks/07_domain3_claude_code.ipynb`**

One skill, 3.1%, about two items. Worth an evening, not a weekend — but it is
cheap to learn because you are using Claude Code to study for the exam about
Claude Code.

### 3.1 Claude Code Operation (3.1%)

The blueprint names: core components (Rules, Skills, Commands, Agents, Agent
Memory), features (session management, built-in and custom slash commands,
headless mode, streaming mode, auto-mode), the CLAUDE.md hierarchy, repository
initialization, and settings.json.

**The CLAUDE.md hierarchy.** CLAUDE.md files are **additive** — every applicable
level contributes to context simultaneously rather than one overriding another.
Files in your working directory and above load at launch; files in
subdirectories load as you work in those subdirectories. Personal configuration
lives in `~/.claude/` and applies across all projects; project configuration
lives in the repo and can be committed to share with the team.

Practical guidance that doubles as exam-relevant reasoning: keep the root
CLAUDE.md small (a couple of hundred lines), because it is loaded on every
session and competes for context with the actual work. Facts Claude should hold
all the time go here — build commands, directory layout, conventions.
*Procedures* do not; they belong in skills.

**Distinguishing the components** is the heart of this domain, and the notebook's
§ 3.3 is built for it. The distinctions turn on **when each loads** and **what it
costs**:

| Component | Loads | Use for |
|---|---|---|
| **CLAUDE.md** | session start, always | facts to hold all the time |
| **Rules** | session start, or on file match if path-scoped | specific constraints; path-scoping avoids wasted tokens |
| **Skills** | name + description at start; body on invocation | procedural workflows — a deploy checklist, a release process |
| **Subagents** | name + description at start; body when called | side tasks in an isolated context; only a summary returns |
| **Commands** | on explicit invocation (`/name`) | user-triggered repeatable actions |
| **Hooks** | on lifecycle events | deterministic automation and guardrails |
| **Plugins** | the packaging layer | bundling skills, hooks, subagents, MCP servers as one installable unit |

The two decision rules most likely to be tested:

- **Skills over CLAUDE.md for procedures.** CLAUDE.md is for what Claude should
  always know; a skill is for a process invoked when relevant. Putting a deploy
  checklist in CLAUDE.md pays its token cost in every session that has nothing
  to do with deploying.
- **Hooks over prompts for guarantees.** If something absolutely must not
  happen, a hook is deterministic; an instruction can fail under pressure. Same
  principle as Domains 1 and 7.

**settings.json** is where hooks are registered and permissions and environment
configuration live, at user, project, and local scopes. Note that skills and
subagents resolve by name with a priority order when the same name exists at
multiple levels.

**Modes.** *Interactive* is the normal terminal session. *Headless* (`-p` with
`--output-format json`) runs non-interactively for scripting and CI — and it is
also how you drive the agent loop from a language the Agent SDK does not
support. *Streaming* emits output incrementally. *Auto-mode* reduces the
approval prompting for routine operations.

**Agent Memory** is persistence across sessions, as distinct from the context
window, which is per-session. Same clear/summarise/persist distinction as
Domain 1.

### Self-check — Domain 3

1. Are CLAUDE.md files additive or overriding, and which levels load when?
2. A team wants a deploy checklist available to Claude. CLAUDE.md or a skill? Why?
3. What does a subagent give you that a skill does not?
4. When would you use headless mode?
5. Where do hooks get registered?

---

## Part 8 — Domain 4: Eval, Testing, and Debugging (2.6%)

→ **Lab: `notebooks/08_domain4_eval_testing_and_debugging.ipynb`**

The smallest domain — one skill, about one item. But the *thinking* here
underpins several other domains, so do not skip it; just do not over-invest.

### 4.1 Debugging and Error Handling (2.6%)

The blueprint names four things: error type identification, recovery strategy
selection, trace analysis to identify failure modes, and **problem origin
isolation between the integration layer and model output**.

That last phrase is the domain's centre of gravity. When an LLM application
misbehaves, the first question is always: **is this my code, or is this the
model?**

- **Integration-layer failures** are deterministic and reproducible. A 400 from
  a malformed request. A parsing error. A retry storm. Wrong model ID. Missing
  tool result. These reproduce every time with the same input, and they are
  fixed in code.
- **Model-output failures** are probabilistic. The output is well-formed but
  wrong. It is right four times in five. It degraded after a prompt edit or a
  model upgrade. These are fixed with prompts, examples, schemas, or a different
  model.

The diagnostic that separates them: **run the same input several times.** Fails
identically every time → integration layer. Fails sometimes → model output. The
notebook's `diagnose` and its worked cases drill exactly this, and it is the
most transferable thing in the domain.

**Instrumented traces** are what make that diagnosis possible after the fact.
The notebook's `run_traced_agent` records each turn: what was sent, what came
back, `stop_reason`, which tools were called with which arguments, token usage.
Without a trace you are guessing; with one you can point at the turn where the
run went wrong. In an agent loop this is not optional — a ten-turn failure with
no trace is close to undebuggable.

**Testing non-deterministic output.** You cannot assert equality against model
output. What you can do:

- Assert on **structure** — schema-valid, required fields present, values in
  range.
- Assert on **properties** — contains no PII, stays under a length cap, cites
  only documents that were supplied.
- Assert on **rates** — run N samples and require that k of N pass. This is what
  the notebook's `evaluate` does, and it is the honest way to test a
  probabilistic component.
- Use an **LLM judge** for qualitative criteria, accepting that the judge is
  itself non-deterministic and needs its own validation.

**Recovery strategy selection** ties back to Domain 2's retry discipline: retry
transient failures with backoff; repair schema failures by feeding the specific
validation error back; escalate to a human for irreducible ambiguity; and fail
loudly rather than silently degrading.

### Self-check — Domain 4

1. One diagnostic separates integration bugs from model bugs. What is it?
2. Why can't you write an exact-match test against model output? Give three
   things you can assert instead.
3. What should a trace record for a single agent turn?
4. Your output is schema-valid but wrong. Which layer, and which fixes apply?

---

## Part 9 — A study plan that fits the weights

Time allocated in proportion to exam weight, not to how interesting a topic is.
Adjust the calendar to your schedule; keep the proportions.

**Pass 1 — Understand (roughly 60% of your time)**

Work sections 1 → 8 in order. For each: read the guide section, run the matching
notebook top to bottom, break something deliberately, then answer the self-check
questions from memory. Do not move on while a self-check still needs the page
open.

Budget roughly: three sessions on §1 (Domain 2), two on §2 (Domain 5), two on §3
(Domain 1), one or two each on §4–§6, and one session covering §7 and §8
together.

**Pass 2 — Build (roughly 25%)**

The exam guide's own preparation advice is to build and operate at least one
Claude application that exercises the API, integrates one or more tools, applies
prompt and context engineering, and includes security and evaluation practices.
Do that. The notebooks are a claims-triage scenario throughout; extend it into
something that runs end to end. A good warm-up: take any cell that now uses
`output_config` raw JSON Schema and convert it to `client.messages.parse()` with
a Pydantic model, or the reverse. Moving between the two forms forces you through
the modern API surface, which Part 0.5 explains is exactly where the platform
moved.

**Pass 3 — Consolidate (roughly 15%)**

Re-read the blueprint in Section 6 of the official exam guide and self-assess
against each of the 23 skills honestly. Any skill you cannot explain in two
sentences goes back into pass 1. Re-run the self-checks cold. Work the three
official sample questions and, more importantly, articulate why each *wrong*
answer is wrong — the distractors teach more than the keys.

### The traps worth memorising

These recur across domains and are the kind of thing scenario items are built
from:

| Trap | The correction |
|---|---|
| Streaming reduces cost | It reduces *perceived latency*. Cost is identical. |
| Hiding thinking output saves money | Thinking is billed regardless. Lower `effort`. |
| `response.content[0].text` | Filter blocks by `type`. |
| A bigger model resists injection better | It can follow injected instructions *better*. |
| A strongly-worded prompt prevents an action | Only a hook or code-level gate is deterministic. |
| Built-in tools can reach internal APIs | They cannot. That is what MCP or a custom tool is for. |
| Parallel sync requests reduce per-token cost | They do not. Batch does (50%, within 24h). |
| Retry everything that failed | Retry 429/5xx/network. Never 400/401/403/404. |
| Well-formatted output is correct output | Validate structure, semantics, and coverage. |
| Lower `max_tokens` is a cost strategy | It truncates. Cache, batch, or tune effort instead. |

---

## Part 10 — Exam day

**Logistics.** 53 items, 120 minutes, proctored online or at a Pearson VUE test
centre. Bring valid, unexpired, government-issued photo ID whose name matches
your registration exactly. You can cancel or reschedule up to 24 hours before;
inside 24 hours you forfeit the fee.

**Rules.** Stay in view of the webcam for the whole session if testing online.
Keep the workspace clear — no notes, books, phones, smart watches, headphones,
or secondary monitors. Do not communicate with anyone. Do not capture or
reproduce any exam content in any form.

**The NDA.** Before the exam begins you accept a confidentiality agreement
covering all exam content — questions, answer options, and scenarios. This has a
practical consequence for you specifically: **this repository is public.** If
you add study notes after sitting the exam, keep anything resembling a real item
out of it. Paraphrasing a question you remember into a public repo is the
easiest way to breach an agreement you did not intend to breach. If you want to
keep notes as you study, make the repo private first.

**Pacing.** Just over two minutes per item. Most items are short scenarios; the
deciding constraint is usually one clause. Flag and move on rather than
stalling — there is no penalty for a guess, and an unanswered item is a
guaranteed zero. On multiple-response items, read how many selections are
required before you read the options.

**Afterwards.** You get pass/fail with a scaled score and percent-correct by
domain. If you do not pass, the waiting period is 14 days, then 30, then 90, up
to four attempts in a rolling year. The domain breakdown on the score report
tells you where to go back to — which, given the weights, will usually be
Domain 2.

---

## Reference card

Worth a final skim the morning of the exam.

**Weights, highest first:** D2 Applications and Integration 33.1% · D5 Model
Selection and Optimization 16.8% · D1 Agents and Workflows 14.7% · D6 Prompt and
Context Engineering 11.0% · D8 Tools and MCPs 10.6% · D7 Security and Safety
8.1% · D3 Claude Code 3.1% · D4 Eval, Testing, and Debugging 2.6%.

**Heaviest individual skills:** Claude Application Design 8.6% · Software
Engineering Foundations 7.4% · Claude API Mechanics 6.8% · Technical
Fundamentals 6.1% · Agent Construction 5.3% · LLM Fundamentals 5.2%.

**Models:** Opus 5 `claude-opus-5` 1M ctx $5/$25 · Sonnet 5 `claude-sonnet-5` 1M
ctx $2/$10 · Haiku 4.5 `claude-haiku-4-5` **200K** ctx $1/$5.

**Thinking:** `thinking={"type":"adaptive"}`; depth via
`output_config={"effort": low|medium|high|xhigh|max}`, default `high`. On Opus 5
thinking is on by default. Display setting does not change cost.

**Caching:** prefix match, render order `tools` → `system` → `messages`. Stable
first, volatile last. Write ≈1.25×, read ≈0.1×. Default TTL 5 min, 1 h
available. Max 4 breakpoints. Verify with `usage.cache_read_input_tokens`.

**Batch:** 50% off input and output, within 24 hours. Results in any order — key
by `custom_id`.

**Retry:** yes on 429, 5xx, connection/timeout. No on 400, 401, 403, 404.

**Agent loop:** send → `stop_reason == "tool_use"` → append full
`response.content` → execute → return **all** `tool_result` blocks in **one**
user message → repeat until `end_turn`. Tool failure → `tool_result` with
`is_error: true`.

**Mechanism choice:** built-in if it exists · custom if it is yours alone · a
Skill if it is knowledge not capability · MCP if it must be shared across
applications and maintained independently.

**MCP:** host / client / server. Tools (model-controlled), resources
(application-controlled), prompts (user-controlled). Transports: stdio (local
subprocess) or HTTP (remote/shared).

**Context:** context editing *clears*, compaction *summarises*, memory
*persists*, subagents *isolate*.

**Debugging:** same input, repeated. Fails identically → integration layer.
Fails intermittently → model output.
