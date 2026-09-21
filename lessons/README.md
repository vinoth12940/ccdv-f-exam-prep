# Lessons — small runnable files, in exam-weight order

One file per concept. Read the docstring, run the file, change something,
run it again. Every file stands alone — `python3 lessons/NN_name.py`.

```bash
cd lessons
export ANTHROPIC_API_KEY=sk-ant-...
python3 01_response_blocks.py
```

`common.py` holds the client, the model IDs and `extract_text()`.
Files marked *notes* have no code — they are the concept only.


## D2 Applications & Integration — 33.1%

| File | Concept |
|---|---|
| [`01_response_blocks.py`](01_response_blocks.py) | 2.1 Claude API Mechanics — the response object |
| [`02_system_vs_user.py`](02_system_vs_user.py) | The system parameter is separate from messages |
| [`03_streaming.py`](03_streaming.py) | Streaming |
| [`04_structured_outputs.py`](04_structured_outputs.py) | Forcing a response shape with structured outputs |
| [`05_batch_vs_realtime.py`](05_batch_vs_realtime.py) | Realtime vs. Batch |
| [`06_async_concurrency.py`](06_async_concurrency.py) | 2.2 Software Engineering Foundations (7.4%) |
| [`07_retries_and_errors.py`](07_retries_and_errors.py) | Retries and error typing |
| [`08_schema_validation.py`](08_schema_validation.py) | 2.3 Claude Application Design (8.6%) |
| [`09_content_boundaries.py`](09_content_boundaries.py) | Content boundaries |
| [`10_config_management.py`](10_config_management.py) | 2.4 Configuration Management (4.1%) |
| [`11_requirements_and_lifecycle.py`](11_requirements_and_lifecycle.py) | 2.5 Understanding Requirements (3.4%) and Systems Life Cycle (2.8%) *(notes)* |

## D5 Model Selection & Optimization — 16.8%

| File | Concept |
|---|---|
| [`12_token_counting.py`](12_token_counting.py) | 5.1 LLM Fundamentals — counting tokens before you spend them |
| [`13_thinking_and_effort.py`](13_thinking_and_effort.py) | Extended thinking, and what replaced the token budget |
| [`14_non_determinism.py`](14_non_determinism.py) | Non-determinism |
| [`15_prompt_caching.py`](15_prompt_caching.py) | 5.2 Cost and Token Management (2.8%) |
| [`16_model_selection.py`](16_model_selection.py) | 5.3 Model Selection and Tradeoffs (2.7%) |
| [`17_sdk_vs_raw_rest.py`](17_sdk_vs_raw_rest.py) | 5.4 Technical Fundamentals (6.1%) |

## D1 Agents & Workflows — 14.7%

| File | Concept |
|---|---|
| [`18_workflow_or_agent.py`](18_workflow_or_agent.py) | 1.1 Workflow or agent? |
| [`19_workflow_fixed_steps.py`](19_workflow_fixed_steps.py) | A workflow: fixed, predetermined steps |
| [`20_tool_use_loop.py`](20_tool_use_loop.py) | 1.2 Agent Construction — the tool-use loop |
| [`21_parallel_tool_calls.py`](21_parallel_tool_calls.py) | Parallel tool calls |
| [`22_tool_errors.py`](22_tool_errors.py) | Tool errors belong in tool_result, not in an exception |
| [`23_subagents.py`](23_subagents.py) | 1.3 Agent Patterns — supervisor and subagents |
| [`24_hooks.py`](24_hooks.py) | 1.4 Hooks: deterministic control over a non-deterministic system |
| [`25_managed_vs_selfhosted.py`](25_managed_vs_selfhosted.py) | 1.5 Managed vs. self-hosted agents *(notes)* |

## D6 Prompt & Context Engineering — 11.0%

| File | Concept |
|---|---|
| [`26_prompt_placement.py`](26_prompt_placement.py) | 6.1 Prompt Engineering — placement |
| [`27_few_shot_examples.py`](27_few_shot_examples.py) | Zero-shot, single-shot, multi-shot |
| [`28_input_sanitisation.py`](28_input_sanitisation.py) | Input sanitisation |
| [`29_context_pruning.py`](29_context_pruning.py) | 6.2 Context Engineering — pruning and compaction |
| [`30_output_validation.py`](30_output_validation.py) | 6.3 Output Handling — validate, do not trust |

## D8 Tools & MCPs — 10.6%

| File | Concept |
|---|---|
| [`31_tool_descriptions.py`](31_tool_descriptions.py) | 8.1 Tool Implementation — the description is the prompt |
| [`32_client_vs_server_tools.py`](32_client_vs_server_tools.py) | Client-side vs. server-side tools |
| [`33_mcp_server.py`](33_mcp_server.py) | 8.2 MCP — host, client, server |
| [`34_mcp_transports.py`](34_mcp_transports.py) | Transports *(notes)* |
| [`35_choosing_the_mechanism.py`](35_choosing_the_mechanism.py) | 8.3 Agentic Customization — choosing the mechanism *(notes)* |

## D7 Security & Safety — 8.1%

| File | Concept |
|---|---|
| [`36_prompt_injection.py`](36_prompt_injection.py) | 7.1 Prompt injection |
| [`37_defence_not_sufficient.py`](37_defence_not_sufficient.py) | Prompt-level defence is necessary but not sufficient |
| [`38_least_privilege.py`](38_least_privilege.py) | The injected call meets the policy |
| [`39_approval_gates.py`](39_approval_gates.py) | 7.2 Human-in-the-loop approval gates |
| [`40_secrets_and_pii.py`](40_secrets_and_pii.py) | 7.3 Secrets and PII |

## D3 Claude Code — 3.1%

| File | Concept |
|---|---|
| [`41_claude_md_hierarchy.py`](41_claude_md_hierarchy.py) | 3.1 The CLAUDE.md hierarchy |
| [`42_settings_json.py`](42_settings_json.py) | 3.2 settings.json |
| [`43_components_compared.py`](43_components_compared.py) | 3.3 The components, distinguished |
| [`44_claude_code_modes.py`](44_claude_code_modes.py) | 3.4 Modes *(notes)* |

## D4 Eval, Testing & Debugging — 2.6%

| File | Concept |
|---|---|
| [`45_instrumented_traces.py`](45_instrumented_traces.py) | 4.1 Instrumented traces |
| [`46_testing_nondeterministic.py`](46_testing_nondeterministic.py) | 4.2 Testing non-deterministic output |
| [`47_diagnosing_failures.py`](47_diagnosing_failures.py) | 4.3 Isolating the origin — worked cases |

---

Derived from the notebooks by hand — editing a notebook does **not**
update these files, and vice versa. Pick one as your source of truth.
