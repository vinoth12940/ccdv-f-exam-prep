# CCDV-F Study Guide

**Claude Certified Developer – Foundations · Blueprint v1.0 (July 2026)**

Loop for each section: **read → run the notebook → answer the self-check from memory.**
One-page summary: [`02_CHEAT_SHEET.md`](02_CHEAT_SHEET.md). Old long version: `archive/STUDY_GUIDE_verbose.md`.

---

## 0. Exam basics

- **53 items · 120 min · pass 720 / 1000** · criterion-referenced (no curve)
- Multiple-choice + multiple-response → **read how many to select**
- Scenario-based: find the **one deciding clause** ("by morning", "must never", "data can't leave VPC")
- No penalty for guessing → never leave blank; flag and move on (~2 min/item)
- Score report: pass/fail + scaled score + % per domain (domain % is diagnostic only)
- Valid 12 months · retakes wait 14d → 30d → 90d · max 4 per 12 months
- Content is under NDA → don't paste exam questions into this public repo

### Weights — study in this order

| § | Domain | Weight | ~Items | Notebook |
|---|---|---|---|---|
| 1 | D2 Applications & Integration | **33.1%** | 18 | 01 |
| 2 | D5 Model Selection & Optimization | **16.8%** | 9 | 02 |
| 3 | D1 Agents & Workflows | 14.7% | 8 | 03 |
| 4 | D6 Prompt & Context Engineering | 11.0% | 6 | 04 |
| 5 | D8 Tools & MCPs | 10.6% | 6 | 05 |
| 6 | D7 Security & Safety | 8.1% | 4 | 06 |
| 7 | D3 Claude Code | 3.1% | 2 | 07 |
| 8 | D4 Eval, Testing, Debugging | 2.6% | 1 | 08 |

- **D2 + D5 = half the exam.**
- Design/judgement skills outweigh API trivia. Generic engineering (REST, async, retries, config) is worth more than D1 and D4 combined.

---

## 0.5 API changes — old patterns are now wrong answers

| Removed | Replacement |
|---|---|
| Assistant **prefill** (last message = `assistant`) → 400 | **Structured outputs** |
| `temperature`, `top_p`, `top_k` | none — non-determinism is a fact, not a dial |
| `thinking={"type":"enabled","budget_tokens":N}` | `thinking={"type":"adaptive"}` + `output_config={"effort":…}` |

- Structured output, two forms:
  - `client.messages.parse(..., output_format=PydanticModel)` → `response.parsed_output`
  - `client.messages.create(..., output_config={"format":{"type":"json_schema","schema":{…}}})`
- Schema enforces **patterns, enums, bounds** too, not only JSON shape
  - So validation loops now defend **business rules** (cross-field, checks vs. your data)
- Still valid (not prefill): few-shot assistant turns **followed by** a user turn; appending the model's reply to history
- Opus 5: thinking **on by default** (Opus 4.8/4.7: off if omitted)
- `effort` is **model-gated** — Haiku 4.5 returns 400
- Why it matters: D5 tests "breaking behaviour changes across releases"

### Models

| Model | ID | Context | $/1M in / out |
|---|---|---|---|
| Opus 5 | `claude-opus-5` | 1M | 5 / 25 |
| Sonnet 5 | `claude-sonnet-5` | 1M | 2 / 10 |
| Haiku 4.5 | `claude-haiku-4-5` | **200K** | 1 / 5 |

- Remember ratios: Sonnet ≈ 2.5× cheaper than Opus; Haiku ≈ 2× cheaper than Sonnet
- Haiku's 200K window is an **architectural constraint** (long docs can't just move to Haiku)

---

## 1. D2 — Applications & Integration (33.1%) · `notebooks/01`

| Skill | Weight |
|---|---|
| Claude Application Design | 8.6% |
| Software Engineering Foundations | 7.4% |
| Claude API Mechanics | 6.8% |
| Configuration Management | 4.1% |
| Understanding Requirements | 3.4% |
| Systems Life Cycle | 2.8% |

### API mechanics
- `response.content` = **list of typed blocks** (`text`, `tool_use`, `thinking`…)
  - `content[0].text` breaks when the model thinks or calls a tool first
  - Use `"".join(b.text for b in content if b.type == "text")`
- `system` = separate param for persistent role/rules; `messages` = conversation
- **Streaming** → better perceived latency, avoids long-request timeouts. **Same cost.**
- **Realtime vs Batch** — one question: *is a human waiting?*
  - Batch = **50% off** input + output, done within 24 h
  - Results unordered → match by **`custom_id`**
  - Wrong answers for "10k docs overnight": parallel sync calls, lower `max_tokens`, blind model downsizing
- Multi-format: `image` blocks (base64/URL), `document` blocks (PDF), Files API (upload once, reuse `file_id`), citations per document
- **Bedrock / Vertex / Foundry**
  - Own client class (not `base_url` override)
  - Different model IDs and auth (Vertex = GCP ADC)
  - **Feature availability not uniform** — likely exam angle

### Software engineering foundations
- Async = overlapping network waits (I/O-bound), not parallel compute
  - Once rate-limited, concurrency stops helping
- **Retry** with exponential backoff: `429`, `5xx`, connection, timeout
- **Don't retry:** `400`, `401`, `403`, `404` (same error, more expensive)
- SDK defaults: 2 retries (408/409/429/5xx), 10-min timeout → worst case `timeout × (retries + 1)`
- Blanket `except APIError: retry` is a bug → catch most-specific first

### Application design (heaviest skill)
- Behaviour differs by **surface** (API is stateless; Claude Code brings CLAUDE.md, settings, skills)
- **Content boundaries** are drawn at design time: delimit untrusted content, label it as data, say instructions inside are not to be followed
- Schema + validate + repair; on failure send the **specific validation error** back (bare retry repeats the mistake)
- Session hygiene: history is re-sent every request → decide what persists

### Configuration management
- **Pin the exact model ID** ("latest" = surprise)
- Version prompts like code (reviewable diff, traceable to deploy)
- Record model + max_tokens + prompt version as one unit

### Requirements & life cycle
- Split each scenario: **functional** / **infrastructure** / **quality** (speed, cost, reliability, privacy)
- LLM behaviour can change with no code change (model update, prompt edit, input drift)
  - → monitoring and evals are **operational**, not just pre-launch

### Self-check
1. Why is `content[0].text` a latent bug?
2. Chat feature too expensive — why isn't streaming the fix?
3. 10k docs by morning, cost-sensitive: which API, why are the 3 alternatives wrong?
4. Which codes retry, which don't, why?
5. Provider ships a new model — 3 things that make it a non-event?
6. What does `system` give you over a user message?

---

## 2. D5 — Model Selection & Optimization (16.8%) · `notebooks/02`

| Skill | Weight |
|---|---|
| Technical Fundamentals | 6.1% |
| LLM Fundamentals | 5.2% |
| Cost & Token Management | 2.8% |
| Model Selection & Tradeoffs | 2.7% |

- The two "fundamentals" (11.3%) outweigh "Model Selection" (2.7%) — don't only memorise the tier table

### LLM fundamentals
- Tokens: cost and limits are in tokens; window is shared by input + output
- Use `messages.count_tokens` (model-specific) — don't estimate with a generic tokeniser
- Non-deterministic → no exact-match tests; evals need multiple samples
- **Adaptive thinking** — model decides when/how much to think
- **Effort** — `low | medium | high (default) | xhigh | max`
  - Main spend-vs-thoroughness lever within one model
  - Low = subagents/simple; high+ = coding/long-horizon agents
- **Fast mode** — same model, faster output, premium price (latency lever only)
- **Thinking display** (summary vs omitted) — **doesn't change what is billed**
  - "Hide thinking to save money" = wrong → lower `effort`
- Zero / single / multi-shot: examples fix format & judgement boundaries; cost input tokens every call → cache them

### Technical fundamentals
- SDK = convenience layer over REST (`x-api-key`, `anthropic-version`, JSON body)
- Failures surface at HTTP level: status, `retry-after`, request ID
- Streaming = server-sent events (one-way); websocket = bidirectional persistent connection

### Cost & token management
- Cache = **prefix match**; render order `tools → system → messages`
- **Any byte change in the prefix invalidates everything after it**
- Design: stable first (system, sorted tools), volatile last (timestamps, IDs, the question)
- Write ≈ **1.25×** · read ≈ **0.1×** · TTL 5 min (1 h available) · max 4 breakpoints
- Verify via `usage.cache_read_input_tokens`; zero means silent invalidation:
  1. `datetime.now()` in system prompt
  2. Unsorted `json.dumps()`
  3. Tool list changes between calls
  4. Prefix under model minimum (~512–4096 tokens; no error raised)
- **Lever order (free → costly):** cache → batch → trim input → lower effort → downgrade model
- Measure cost **per completed task**, not per request

### Model selection
- **Opus** hardest / long-horizon agents · **Sonnet** balanced default · **Haiku** simple, high-volume, low-latency
- Try **lower effort on a better model** before downgrading
- Caches are model-scoped → multi-model cascades lose cache reuse
- Defence against release changes: pin model + re-run evals

### Self-check
1. Adaptive thinking vs effort — which do you change to cut spend?
2. Does hiding thinking cut cost?
3. Cache hit rate zero — 3 checks in order?
4. Rank cost levers.
5. When is Haiku off the table regardless of budget?
6. Why can a model cascade cost more than one model?

---

## 3. D1 — Agents & Workflows (14.7%) · `notebooks/03`

| Skill | Weight |
|---|---|
| Agent Construction | 5.3% |
| Agent Patterns & Frameworks | 4.9% |
| Agent Architecture | 4.5% |

### Architecture
- **Workflow** = steps fixed in advance; your code controls flow → predictable, cheap, testable
- **Agent** = model chooses steps → flexible, but costlier, slower, harder to debug
- **Test: can you write the steps down in advance?** Yes → workflow (agent = over-engineering)
- Before choosing agent check: **complexity, value, viability, cost of error**
- **Subagents** → context isolation: reads 50 files, returns a summary

### Construction — the tool loop
1. Send `messages` + `tools`
2. `stop_reason == "tool_use"` with `tool_use` blocks
3. Append the **full** `response.content` to history
4. Execute each tool
5. Append **one** user message with **all** `tool_result` blocks
6. Repeat until `end_turn`

- Parallel calls: return all results in **one** message (splitting silently kills parallelism)
- Tool failure → `tool_result` with **`is_error: true`** + description; never raise past the loop

| Approach | Who writes loop | Who hosts | Built-in tools |
|---|---|---|---|
| Manual loop (Messages API) | you | you | none |
| Tool Runner (`beta.messages.tool_runner`) | SDK | you | none |
| **Managed Agents** (beta) | Anthropic | **Anthropic** | sandbox: bash/files/code |
| Claude Agent SDK | SDK | you | Read/Write/Edit/Bash/Glob/Grep/WebSearch |

- Only Managed Agents supplies deployment
- **Tool Runner ≠ Agent SDK** (SDK = Claude Code as a library, Python/TS only)
- Start simple: most tasks = one call or a workflow

### Patterns & frameworks
- Frameworks (Strands, LangGraph, PydanticAI) declare graph/state instead of hand-written loops → structure vs. indirection
- Three answers to "context is filling":
  - **Context editing** clears · **Compaction** summarises · **Memory** persists

### Hooks
- Fire on lifecycle events (pre-tool, post-response, session start); your code → always runs
- **"Must never" → hook / code gate, not a prompt** (prompts are probabilistic)

### Managed vs self-hosted
- Self-hosted: max control, max ops burden
- Anthropic-hosted: less ops, versioned configs, long sessions, scheduling
- "Data can't leave our environment" → self-hosted

### Self-check
1. Workflow-vs-agent test in one sentence?
2. Why all `tool_result`s in one message?
3. Tool throws — what do you send back?
4. Four ways to build an agent; which supplies deployment?
5. "Must never" action — where does the control live?
6. Clear / summarise / persist → which technique?

---

## 4. D6 — Prompt & Context Engineering (11.0%) · `notebooks/04`

| Skill | Weight |
|---|---|
| Prompt Engineering | 4.6% |
| Context Engineering | 3.8% |
| Output Handling | 2.6% |

### Prompt engineering
- **Placement:** persistent behaviour → `system`; request → user; examples before real input
- System prompt = stable cache prefix too (good placement = good caching)
- Few-shot beats prose for format, tone, judgement boundaries
- Output constraints: state exact shape ("one word: APPROVE/DENY/REVIEW") + low `max_tokens`; strongest = structured outputs
- Sanitise untrusted input: escape look-alike delimiters, cap length, wrap as data
  - **Necessary, not sufficient**

### Context engineering
- Stateless API → history re-sent → tool results dominate tokens → **cost, latency, drift**
- **Prune** — replace superseded tool results with placeholders
- **Compact** — summarise (server-side on current models)
  - Must append full `response.content` — text-only loses the compaction state
- **Isolate** — subagent does heavy reading, returns summary (**prevents** bloat rather than cleaning it)

### Output handling
- **Structural** — well-formed, matches schema
- **Semantic** — content actually right (amount exists in source?)
- **Coverage** — did it handle all items or silently drop some?
- **Fluent, confident output ≠ correct**

### Self-check
1. Why does `system` placement help caching?
2. What is context drift; 3 fixes?
3. Server-side compaction: what must you append, what breaks otherwise?
4. Three validation layers + one failure each catches uniquely?
5. Why is sanitisation necessary but not sufficient?

---

## 5. D8 — Tools & MCPs (10.6%) · `notebooks/05`

| Skill | Weight |
|---|---|
| Tool Implementation | 4.4% |
| Agentic Customization | 4.1% |
| MCP Server Development | 2.1% |

### Tool implementation
- **Tool description = a prompt.** Model sees name + description + schema, never the code
- Say **when to use and when not to**; overlapping tools → unreliable selection
- **Client-side:** model emits `tool_use` → you run it → `tool_result`; you own execution + security boundary
- **Server-side** (web search, web fetch, code exec): Anthropic runs it, no loop on your side, less control
  - Server-tool errors are HTTP 200 with an error object
- **Approval gate** between model request and execution for risky calls (same idea as hooks, D7 gates)
- Fewer, crisper tools; large sets → tool search + `defer_loading`

### MCP
- Roles: **host** (app) · **client** (connector) · **server**
- Server exposes:
  - **Tools** — model-controlled
  - **Resources** — application-controlled (URI-addressed data)
  - **Prompts** — user-controlled templates
- Transports: **stdio** (local subprocess) · **HTTP** (remote / shared)
- Why MCP: **reusable across apps** + **independently maintained**
- API connector needs both `mcp_servers` **and** `mcp_toolset` entries

### Agentic customization — how to choose
1. **Built-in tool** — if Anthropic provides it (can't reach internal APIs!)
2. **Custom tool** — specific to one app you control
3. **Skill** — procedural knowledge (checklist, process), loads on demand
4. **MCP server** — must be shared across apps and maintained independently

### Self-check
1. Why is a tool description a prompt?
2. Client-side vs server-side — what do you write, what do you give up?
3. Tools / resources / prompts — who controls each?
4. stdio vs HTTP?
5. Which two phrases point to MCP?
6. When is a Skill right instead of a tool?

---

## 6. D7 — Security & Safety (8.1%) · `notebooks/06`

| Skill | Weight |
|---|---|
| AI Application Security | 3.2% |
| Guardrails & Safe Deployment | 2.3% |
| Identity, Secrets, Keys | 1.6% |
| Claude Hooks | 1.0% |

### Prompt injection (headline threat)
- Correct defence = **three parts**:
  1. Treat retrieved content as **untrusted**
  2. **Isolate** it from trusted instructions
  3. **Guardrails** so injected text can't trigger sensitive actions
- Wrong answers: raise temperature · "ask users not to" · bigger model
  - Bigger / more instruction-following model can follow injections **better**
- A clever injection can **satisfy your stated policy** → prompt hardening can't catch it
  - Architecture does: **least privilege** + **deterministic gate**

### Guardrails
- **Layer** controls that fail differently: sanitise → prompt boundaries → constrained tools → deterministic gates → monitoring/logging
- **Least privilege:** no payment tool → injection can't cause a payment
- **Human approval** only for irreversible / costly / high-blast-radius actions (gating everything makes the system useless)
- **PII:** redact → send → restore
- Basics: authentication, authorization, confidentiality, privacy, integrity

### Secrets
- Keys in env vars / secrets manager, never in source
- `.env` gitignored, `.env.example` committed
- Separate keys per environment · rotate · least-privilege scope · monitor use
- Keys also leak **via prompts** (pasted stack trace, tool output, agent reading `.env`) → scan outbound prompts

### Hooks (1.0%)
- Deterministic enforcement over a probabilistic system

### Self-check
1. Why can a more instruction-following model be worse against injection?
2. Three parts of a correct defence?
3. What does "the injected call meets the policy" show, and what stops it?
4. Which actions get a human gate?
5. Two ways keys leak that `.gitignore` misses?
6. Least privilege in one sentence?

---

## 7. D3 — Claude Code (3.1%) · `notebooks/07`

- CLAUDE.md is **additive** (all applicable levels stack, none override)
  - Working dir and above load at launch; subdirs load when you work there
  - `~/.claude/` = personal; repo = shared/committed
  - Keep root small (~200 lines) — loaded every session

| Component | Loads | Use for |
|---|---|---|
| CLAUDE.md | always | permanent facts (build cmds, layout, conventions) |
| Rules | start, or on file match | specific constraints (path-scope to save tokens) |
| Skills | description at start; body on use | procedures (deploy checklist) |
| Subagents | description at start; body on call | isolated side task; summary returns |
| Commands | `/name` | user-triggered actions |
| Hooks | lifecycle events | deterministic guardrails |
| Plugins | packaging | bundle of skills/hooks/subagents/MCP |

- **Procedures → Skills**, not CLAUDE.md
- **Guarantees → Hooks**, not prompts
- `settings.json` (user/project/local): hooks, permissions, env
- Modes: interactive · **headless** (`-p --output-format json`, scripts/CI) · streaming · auto-mode
- Agent memory = persists across sessions (context window is per-session)

### Self-check
1. CLAUDE.md additive or overriding?
2. Deploy checklist — CLAUDE.md or skill?
3. What does a subagent give that a skill doesn't?
4. When use headless mode?
5. Where are hooks registered?

---

## 8. D4 — Eval, Testing, Debugging (2.6%) · `notebooks/08`

- Core question: **is it my code or the model?**
- **Integration failures** — deterministic: 400, parse error, retry storm, wrong model ID, missing tool result → fix in code
- **Model failures** — probabilistic: well-formed but wrong, right 4/5 times, regressed after prompt/model change → fix with prompts, examples, schemas, model
- **Diagnostic: run the same input several times.** Identical failure → integration · intermittent → model
- **Trace per turn:** what was sent, what came back, `stop_reason`, tools + args, token usage
- **Testing non-deterministic output** — can't exact-match; assert:
  - **Structure** (schema, fields, ranges)
  - **Properties** (no PII, length cap, cites only supplied docs)
  - **Rates** (k of N pass)
  - **LLM judge** for qualitative criteria (validate the judge too)
- **Recovery:** retry transient · repair with the specific error · escalate real ambiguity · fail loudly

### Self-check
1. The one diagnostic separating integration from model bugs?
2. Why no exact-match tests; 3 alternatives?
3. What does a trace record per turn?
4. Output is schema-valid but wrong — which layer, which fixes?

---

## 9. Trap table

| Trap | Truth |
|---|---|
| Streaming reduces cost | Latency only |
| Hiding thinking saves money | Billed anyway → lower `effort` |
| `response.content[0].text` | Filter by `type` |
| Bigger model resists injection | Follows injections better too |
| Strong prompt prevents action | Only hook / code gate is deterministic |
| Built-in tools reach internal APIs | Use MCP / custom tool |
| Parallel sync requests are cheaper | Batch is (50%, ≤24 h) |
| Retry every failure | Only 429 / 5xx / network |
| Well-formatted = correct | Validate structure, semantics, coverage |
| Lower `max_tokens` cuts cost | Truncates → cache / batch / effort |
| Downgrade model first | Last lever |
| Prefill / temperature / `budget_tokens` | Removed |

---

## 10. Study plan (time ∝ weight)

1. **Understand (~60%)** — §1 → §8 in order: read, run notebook, break something, answer self-check without peeking
   - Sessions: D2 ×3 · D5 ×2 · D1 ×2 · D6/D8/D7 ×1–2 each · D3 + D4 ×1 together
2. **Build (~25%)** — one end-to-end Claude app: API + tools + prompt/context engineering + security + evals
   - Warm-up: convert a raw JSON-Schema cell to `messages.parse()` + Pydantic (or reverse)
3. **Consolidate (~15%)** — self-assess against all 23 skills; anything you can't explain in 2 sentences goes back to step 1
   - Work the 3 official sample questions; explain why each **wrong** answer is wrong

---

## 11. Exam day

- ID: valid government photo ID, name matches registration exactly
- Online: stay in webcam view; clear desk; no notes, phones, watches, headphones, 2nd monitor
- Reschedule/cancel ≥24 h before or forfeit fee
- Multi-response: read the **required count** first
- One clause usually decides the item — find it
- Flag, move on, come back; guess if needed

### Last-minute recall
- **D2 + D5 = 50%**
- Batch −50% ≤24h · retry 429/5xx only · cache = prefix, read 0.1×
- `effort` = spend lever · thinking display = free of cost effect
- Workflow if steps known · one user msg for all `tool_result`s · `is_error:true`
- MCP = shared + independently maintained · Skill = procedure · Hook = "must never"
- Injection = untrusted + isolated + gated · least privilege
- Same input repeated → identical = my code, intermittent = model
