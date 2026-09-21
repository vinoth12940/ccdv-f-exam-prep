# CCDV-F Cheat Sheet — morning-of skim

**53 items · 120 min · pass 720/1000 · read "select N" · never leave blank · find the ONE deciding clause**

## Weights
D2 Apps&Integration **33.1** · D5 Model/Optimization **16.8** · D1 Agents **14.7** · D6 Prompt/Context **11.0** · D8 Tools/MCP **10.6** · D7 Security **8.1** · D3 Claude Code **3.1** · D4 Eval/Debug **2.6**

## Removed / changed (distractors)
| Old | Now |
|---|---|
| Assistant prefill | Structured outputs (`messages.parse(output_format=…)` / `output_config={"format":…}`) |
| `temperature/top_p/top_k` | Gone |
| `budget_tokens` | `thinking={"type":"adaptive"}` + `output_config={"effort":…}` |
| Opus 5 thinking | On by default |
| `effort` on Haiku 4.5 | 400 error |

## Models
| | ID | Ctx | $ in/out per 1M |
|---|---|---|---|
| Opus 5 | `claude-opus-5` | 1M | 5 / 25 |
| Sonnet 5 | `claude-sonnet-5` | 1M | 2 / 10 |
| Haiku 4.5 | `claude-haiku-4-5` | **200K** | 1 / 5 |

Opus = hardest · Sonnet = default · Haiku = simple/high-volume. **Pin exact IDs.**

## API
- `content` = list of blocks → filter `type=="text"`
- `system` param ≠ user message
- Streaming = latency, **not** cost
- **Batch:** −50%, ≤24h, unordered → `custom_id`
- Human waiting? realtime. Else batch.
- Effort: `low|medium|high(default)|xhigh|max` — the spend lever
- Thinking display ≠ cost

## Retry
**Yes:** 429 · 5xx · connection · timeout  |  **No:** 400 · 401 · 403 · 404
SDK: 2 retries, 10-min timeout

## Caching
- Prefix match: `tools → system → messages`
- Stable first, volatile last
- Write 1.25× · read 0.1× · TTL 5m/1h · 4 breakpoints
- Check `usage.cache_read_input_tokens`
- Killers: timestamps, unsorted JSON, changing tools, prefix too short

## Cost levers (free → costly)
cache → batch → trim input → lower effort → downgrade model

## Agents
- Can steps be written in advance? **Yes = workflow**, no = agent
- Loop: `stop_reason=="tool_use"` → append full `content` → run → **ONE** user msg w/ **ALL** `tool_result` → until `end_turn`
- Tool fails → `tool_result` `is_error:true`
- Subagent = context isolation (summary returns)
- **Clear**=context editing · **Summarise**=compaction · **Persist**=memory
- Compaction: append full `response.content`

| Build | Harness | Hosting |
|---|---|---|
| Manual loop | you | you |
| Tool Runner | SDK | you |
| Managed Agents | Anthropic | **Anthropic** |
| Agent SDK | SDK | you |

## Tools & MCP
- Description = prompt (when to use / when not)
- Client-side: you execute · Server-side: Anthropic executes, no loop
- MCP: host / client / server · **Tools**=model · **Resources**=app · **Prompts**=user
- stdio=local · HTTP=remote/shared
- API needs `mcp_servers` **+** `mcp_toolset`
- **Pick:** built-in → custom (one app) → Skill (procedure/knowledge) → **MCP (reusable + independently maintained)**
- Built-ins can't hit internal APIs

## Security
- Injection fix = **untrusted + isolated + guardrails on actions**
- Bigger model / higher temp / "please don't" = wrong
- Injection can pass policy → **least privilege + deterministic gate**
- **"Must never" → hook / code, not prompt**
- Human gate: irreversible / costly only
- PII: redact → send → restore
- Keys: env / secrets mgr; scan **prompts** for leaks too

## Prompt / output
- Persistent → `system`; few-shot > prose for format
- Sanitise input: necessary, not sufficient
- Validate: **structural · semantic · coverage**
- Confident ≠ correct
- Bloat: prune · compact · isolate

## Claude Code
- CLAUDE.md additive; keep small
- **Skills = procedures** · CLAUDE.md = always-on facts · **Hooks = guarantees**
- Subagent = isolated context · Plugin = bundle
- Headless: `-p --output-format json`
- `settings.json` = hooks/permissions/env

## Debug
- **Same input N times:** identical fail → integration · intermittent → model
- Test by structure / properties / rate (k of N) / judge
- Trace: sent, received, `stop_reason`, tools+args, tokens

## Top traps
Streaming≠cheaper · hide-thinking≠cheaper · `content[0]` · bigger model≠safer · prompt≠guarantee · built-in≠internal API · parallel sync≠batch · retry-all · formatted≠correct · low `max_tokens`=truncation · downgrade is last lever
