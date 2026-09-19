# CCDV-F Study Guide — why each domain is on the exam

Read this before the notebooks. The notebooks teach you *how*; this explains
*why*, which is what makes the knowledge stick and what lets you reason through
a scenario question you haven't seen before.

---

## First: what the Reddit post is and isn't good for

I cross-mapped every topic that post reports onto the official blueprint skills.

**It touches skills worth ~46% of the exam. It never mentions the other ~54%.**

Unmentioned, largest first:

| Weight | Skill |
|---|---|
| 8.6% | Claude Application Design |
| 7.4% | Software Engineering Foundations |
| 6.1% | Technical Fundamentals |
| 5.2% | LLM Fundamentals |
| 4.6% | Prompt Engineering |
| 4.5% | Agent Architecture |
| 4.1% | Configuration Management |
| 4.1% | Agentic Customization |
| 3.4% | Understanding Requirements |
| 3.1% | Claude Code Operation |
| 2.8% | Systems Life Cycle |

This isn't a knock on the post. It's one person recalling what stuck out after
a 53-item exam, and what sticks out is what felt hard or novel — not what was
routine. **A topic being absent from a recall post is not evidence it's absent
from the exam.** Someone who found the software-engineering items easy wouldn't
think to list them.

So: use the post to confirm that the high-weight technical areas really do show
up in scenario form. Don't use it as a syllabus. The blueprint is the syllabus,
and Section 6 of the exam guide is the authoritative version of it.

One caution on the practice-exam recommendation in that post. Third-party
practice questions written against the public blueprint are normal and fine.
A claim that "75–80% matched the real exam" describes something else — the exam
content is confidential and non-disclosable under the NDA you accept before
starting. Material that close to the live bank is a risk to whoever sourced it
and potentially to your own standing if you're seen relying on it. Practice
questions are for calibration; understanding is what passes.

---

## The exam's actual theory of the candidate

Two facts from the exam guide drive everything else.

**It's criterion-referenced.** You're measured against a fixed standard set by
subject-matter experts describing a minimally qualified candidate — not graded
on a curve against other candidates. There's no "beat the median" strategy.
You either demonstrate the competencies or you don't.

**The cut score is 720 on a 100–1,000 scale, over 53 items in 120 minutes.**
That's roughly 2 minutes 15 seconds per item, and the items are multi-paragraph
scenarios. The blueprint is not distributed evenly, so a domain worth 2.6% is
roughly one or two items. Time spent mastering Domain 4 to perfection while
Domain 2 is shaky is time spent badly.

**What this means for how you study:** the exam is built around a person who
*ships* Claude applications. Nearly every item gives you a situation with
constraints — cost, latency, reliability, security — and asks which approach
fits. The wrong answers aren't nonsense; they're things that *would* work in a
different situation. You pass by recognising which constraint is binding, which
is a skill you build by writing code and hitting the tradeoff yourself, not by
memorising definitions.

That's why the notebooks are structured as runnable code rather than flashcards.

---

## Domain 2 — Applications and Integration (33.1%)

**Why it's the biggest domain.** This is the job. A third of the exam is here
because a third of the actual work of shipping a Claude app is ordinary software
engineering applied to a non-deterministic dependency. The credential claims you
can "independently own or significantly contribute to building, integrating, and
shipping Claude-powered systems" — most of that is integration.

**Why each skill is on the list:**

*Claude API Mechanics (6.8%)* — Because the response object's shape determines
whether your code survives contact with production. `response.content` is a list
of typed blocks. Code that grabs `content[0].text` works in development and
breaks the first time the model returns a thinking block or a tool call first.
The exam tests whether you parse by type.

*Software Engineering Foundations (7.4%)* — Because an LLM call is a network
call to a slow, rate-limited, occasionally-failing remote service. Everything you
know about async, retries, backoff, and error typing applies. The specific
judgement the exam wants: which errors are worth retrying. A 429 is transient, so
back off and retry. A 400 means your payload is malformed — retrying sends the
same malformed payload and burns quota to fail identically.

*Claude Application Design (8.6%)* — The single heaviest skill on the exam, and
the one the Reddit post never mentions. It covers how Claude interprets
instructions differently across Claude Code, Desktop, claude.ai, API, and SDKs;
content boundaries; schema design; session hygiene. Why it's weighted so heavily:
these are the decisions that are expensive to reverse. A bad schema or a missing
trust boundary gets baked into a system and costs months.

*Configuration Management (4.1%)* — Because models change. `claude-sonnet-5` is
an alias that moves; `claude-haiku-4-5-20251001` is frozen. If production runs on
an alias, a model release changes your output format on a random Tuesday and your
parser breaks with no deploy in your git history to blame. Pinning, then
upgrading deliberately behind an eval suite, is the discipline being tested.

*Understanding Requirements (3.4%) and Systems Life Cycle (2.8%)* — Because the
intended audience "operates at the intersection of business requirements and
technical implementation." These items give you a business scenario and ask you
to derive functional and infrastructure requirements. The reasoning move: find
the constraint that eliminates options before any quality question is on the
table. A data-residency requirement decides which endpoint you may call at all.

**Reddit confirms:** Messages API requests, content blocks, prefilling; streaming
vs. Batch. Both are API Mechanics. It says nothing about the two heaviest skills
in the domain.

→ Notebook `01`.

---

## Domain 5 — Model Selection and Optimization (16.8%)

**Why it's second-heaviest.** Because this is where money is won and lost, and
because the failure mode is invisible. Nobody files a bug report saying "we used
Opus for a classification task and paid 5x too much." It just quietly happens.

*LLM Fundamentals (5.2%) and Technical Fundamentals (6.1%)* — Together 11.3%,
and the Reddit post mentions neither. These cover tokens, context windows,
sampling, non-determinism, extended thinking, and the fact that SDKs are wrappers
over REST. Why it matters: non-determinism has a concrete consequence — **you
cannot write a test that asserts exact string equality on model output.** You
assert on structure and properties, and you measure a pass rate over several
runs. Engineers who haven't internalised that write test suites that flake.

*Cost and Token Management (2.8%)* — The two multipliers that carry most of the
weight: Batch is 50% off input and output; a cache read is 0.1x base input while
a 5-minute cache write is 1.25x. That second ratio has a clean consequence — a
5-minute cache pays for itself after **one** read, a 1-hour cache after **two**.
That's a fact you can reason from rather than memorise.

*Model Selection and Tradeoffs (2.7%)* — Haiku for simple work at volume, Sonnet
as the production default, Opus for complex agentic reasoning. The exam's trap is
always "use the most capable model." A scenario that specifies high volume and
simple tasks is testing whether you'll downshift.

**Reddit confirms:** model tier picking, prompt caching and breakpoint placement,
token tracking. Silent on the 11.3% of fundamentals underneath.

→ Notebook `02`.

---

## Domain 1 — Agents and Workflows (14.7%)

**Why it's weighted heavily.** An agent is the hardest thing in the blueprint to
get right, because it's a loop whose length the model decides at runtime. That's
a category of failure ordinary software doesn't have.

*Agent Architecture (4.5%)* — The decision the exam most wants you to get right
is **workflow or agent**. A workflow runs steps you fixed in advance: cheap,
testable, debuggable, no runaway risk. An agent decides its own steps: necessary
when the number and order of steps depends on what's discovered mid-task, and
strictly worse in every other case. The trap is reaching for an agent when a
workflow would do.

*Agent Construction (5.3%)* — Claude never executes a tool. It returns a
`tool_use` block; your code runs the function and returns a `tool_result`. Four
things the exam checks: append the *entire* content list including tool_use
blocks; match every `tool_use` with a `tool_result` carrying the same id in the
very next turn; handle *multiple* tool_use blocks (parallel calls); and bound the
loop. That last one is the classic production failure — the Reddit post lists
"forgetting to set strict loop limits" as a top mistake, and it's right.

*Agent Patterns (4.9%)* — Supervisor/subagent exists for **context isolation**,
not speed. Each subagent gets a clean narrow window instead of inheriting the
whole conversation. Why that matters: a long shared context invites drift, costs
more every turn, and lets stale content bias later answers. This is why the
blueprint pairs subagents with context management rather than with performance.

**Reddit confirms:** bounded loops with explicit step limits and stop conditions,
coordinator vs. subagent context passing. Both match. It doesn't mention the
workflow-vs-agent architecture decision, which is 4.5% on its own.

→ Notebook `03`.

---

## Domain 6 — Prompt and Context Engineering (11.0%)

**Why it's here and why it's capped at 11%.** Note what the exam guide says the
credential is *not* for: "roles limited to prompt writing or other isolated tasks
without broader application development responsibility." Prompting matters, but
the exam deliberately refuses to let it dominate.

*Prompt Engineering (4.6%)* — Placement is the core idea. Standing rules go in
`system`; the task goes in the user turn. Two reasons: the model weights system
content as standing instruction, and a stable system block is what prompt caching
can reuse. The other high-value idea: when output format drifts, add examples,
don't add adjectives. Few-shot examples teach format and edge-case policy more
reliably than prose description.

*Context Engineering (3.8%)* — Context grows every turn and tool results are the
worst offender: verbose, and stale the moment they've been used. Pruning replaces
old tool output with placeholders; compaction summarises old turns and drops the
originals. Both fight context drift, the degradation that comes from a window
crowded with irrelevant content.

*Output Handling (2.6%)* — The most important sentence in this domain, and the
Reddit post's sharpest observation: **prompt engineering cannot replace code
validation.** No prompt makes output reliable enough to consume unvalidated. You
need two checks, and the exam wants both: structural (does it match the schema)
and semantic (does it agree with your source of truth). A response can be
perfectly well-formed JSON and still factually wrong. "Skepticism toward
confident output" is a named blueprint skill for that reason.

**Reddit confirms:** defensive JSON schemas, malformed output handling, long
context without drift, and the "prompting isn't validation" mistake. Doesn't
mention prompt engineering proper (4.6%).

→ Notebook `04`.

---

## Domain 8 — Tools and MCPs (10.6%)

*Tool Implementation (4.4%)* — The tool `description` **is** a prompt. It's how
the model decides whether and when to call the tool. Vague descriptions cause
wrong-tool selection, which is why "tool description writing" is a named skill. A
good description states what it does, the exact input format with an example,
what it returns, and when *not* to call it versus a similar tool.

*MCP Server Development (2.1%)* — Small weight, high trap density. The three
roles: **Host** is the application that owns the conversation (Claude Code, your
app); **Client** lives inside the host and manages one connection to one server;
**Server** exposes capabilities and is *called*, never the caller. The error the
Reddit post flags — "getting MCP server roles mixed up with application-side API
clients" — is exactly the one the exam sets up. Your code that calls the Claude
API is the host, not a server.

*Agentic Customization (4.1%)* — Twice the weight of MCP server development, and
unmentioned by the post. Given a need, which mechanism: built-in tool, custom
tool, Skill, or MCP server? Two hinges decide it. **Reuse across applications** →
MCP server, because a custom tool duplicated in five codebases is five places to
fix a bug. **Knowledge versus action** → a Skill teaches Claude how your team
does something; a tool gives it the ability to do something external.

**Reddit confirms:** typed tool definitions, parallel tool calls, MCP host/client/
server roles, resource and tool discovery.

→ Notebook `05`.

---

## Domain 7 — Security and Safety (8.1%)

**Why it earns 8% in a developer exam.** Because an LLM that reads untrusted
content and can call tools is a new class of attack surface, and the standard
engineering instincts don't cover it.

*AI Application Security (3.2%)* — **Indirect** prompt injection is the hard
problem: the attack is hidden in content your system fetched — a web page, a PDF,
a customer-controlled database field — so no human reviewed the payload. The
exam's own sample question gives the answer: isolate untrusted content from
trusted instructions, and enforce least privilege so injected text can't reach a
sensitive tool.

Three wrong answers worth recognising on sight, from that same sample: raising
temperature (unrelated to injection), asking users not to inject (not an
enforceable control), and using a bigger model — which the guide explicitly notes
can be *more* susceptible, because better instruction-following means better
following of the injected instruction too.

*Guardrails and Safe Deployment (2.3%) and Claude Hooks (1.0%)* — The reason
these are separate from the prompt-level defence: **a prompt-level rule can be
argued around; an `if` statement cannot.** A hook intercepts a tool call before
execution and blocks it in code. Layer both — the prompt reduces the chance the
model is fooled, the hook makes it not matter when it eventually is. That's
defence in depth, and it assumes the earlier layer will fail.

*Identity, Secrets, and Key Management (1.6%)* — One rule carries it: a secret
never enters a prompt. Context gets logged, cached, traced, and echoed back. A
key in context is a key in every log and trace that context touches.

**Reddit confirms:** indirect injection when parsing untrusted web content and
PDFs, intercepting unsafe tool calls with hooks, HITL approval gates for risky
writes, credentials outside prompt contexts, and "skimping on security
permissions around tool execution" as a top mistake. The strongest agreement
between the post and the blueprint of any domain.

→ Notebook `06`.

---

## Domain 3 — Claude Code (3.1%) and Domain 4 — Eval/Debugging (2.6%)

Together 5.7% — roughly three items. Budget your time accordingly, but don't skip
them, because they're cheap to learn.

*Claude Code Operation (3.1%)* — Mostly precedence and component roles. The
CLAUDE.md hierarchy layers enterprise → project → project-local → user, more
specific winning. The distinction the exam presses: a **Command** is user-invoked
(`/name`), a **Skill** is model-invoked when relevant, and a **Subagent** exists
for context isolation — a fresh window, not just a different prompt. Headless mode
(`claude -p`) is the CI/CD answer, because a pipeline has no terminal to type into.

*Debugging and Error Handling (2.6%)* — The whole skill is **isolating the
problem origin**: integration layer or model output? They need opposite fixes and
confusing them wastes days. A `TypeError` unpacking `tool_use.input` means your
schema and function signature disagree — the model did exactly what the schema
said, so that's your bug. A model citing a policy clause that doesn't exist is
model output — inputs were fine, reasoning wasn't.

The Reddit post's "feed structured error messages back so it can fix itself"
lands here: a retry that resends the original prompt without saying what was
wrong usually reproduces the same failure. Append the validation error so the
next attempt has new information.

→ Notebooks `07` and `08`.

---

## How to work through this

1. **Read this guide.** The *why* is what lets you reason through an unfamiliar
   scenario instead of pattern-matching.
2. **Run the notebooks in order** — they're weighted, so `01`–`03` cover ~65% of
   the exam.
3. **Break things deliberately.** Remove the turn limit and watch a loop run.
   Send only the first of two parallel tool results and read the 400. Pass a
   schema field name your function doesn't accept. The error messages are the
   lesson — Domain 4 is asking you to recognise these on sight.
4. **Build one small end-to-end app** — the exam guide's own recommendation. API
   call, one or two tools, prompt and context engineering, a guardrail, an eval.
   Every domain touches it.
5. **Practice the clock.** ~2m15s per multi-paragraph scenario. Read for the
   binding constraint first — cost, latency, reliability, or security — because
   that's usually what separates two otherwise-plausible answers.

When a cell's output surprises you, stop there. That's the concept worth the
time. Bring it back and we'll go deeper on it.
