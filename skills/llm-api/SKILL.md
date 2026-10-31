---
name: llm-api
description: >-
  Call any OpenAI-compatible chat endpoint (vLLM, SGLang, LM Studio, Ollama,
  hosted gateways) from the command line, with honest handling of the failure
  modes that reasoning models introduce: empty content with a populated
  reasoning channel, replies cut off by max_tokens, thinking that has to be
  toggled per server dialect, and silent 200s that are not JSON. Use when asked
  to run a prompt against a local or remote LLM, compare models, script a batch
  of calls, debug an empty or truncated reply, or control thinking/reasoning
  effort. Keywords — LLM, OpenAI compatible, chat completions, vLLM, SGLang,
  推理模型, thinking, reasoning_content, reasoning_effort, max_tokens, 截断,
  空回复, 调用模型.
metadata:
  version: "1.0.0"
---

# LLM API

The OpenAI chat contract is a de facto standard, and every implementation
deviates a little. The deviations that cost time are not the big ones (auth,
404) — they are the ones that return HTTP 200 with a subtly useless body.

## Shape of a call

```bash
python scripts/llm.py --base-url http://host:8000/v1 --model my-model \
  --system "answer briefly" --prompt "what is a merge base?"

echo "long document" | python scripts/llm.py --stdin --model my-model --json
```

`--base-url` overrides `LLM_BASE_URL`, `--api-key` overrides `LLM_API_KEY`; no
endpoint, key or model name is built in. `--dry-run` prints the exact URL and
JSON body without sending anything — use it first when a server behaves oddly.

`--json` prints one envelope (`text`, `chars`, `usage`, `reasoning_chars`) so a
caller never has to parse prose out of stdout.

## The reasoning-model traps

A thinking model may spend its whole budget thinking and return an empty
`content` with the work sitting in `reasoning_content`. A naive client prints
nothing and looks broken. This one reports the cause instead:

| Symptom | What actually happened | Fix |
| --- | --- | --- |
| `content` empty, `reasoning_content` full, `finish_reason=length` | thinking consumed `max_tokens` | raise `--max-tokens` or turn thinking off |
| `finish_reason=length` with text | reply truncated mid-sentence | raise `--max-tokens` |
| `content` empty, everything empty | server ignored the prompt or the model refused | exit 7; check the request with `--dry-run` |
| reply is fine but slow | thinking is on by default | `--think off` |

The client falls back to the reasoning text and warns on stderr, so you see the
diagnosis instead of a blank line.

## Turning thinking on and off

There is no single field; servers disagree, so pick the dialect explicitly:

| `--think-style` | Sends | Works with |
| --- | --- | --- |
| `effort` (default) | `reasoning_effort: none\|low\|medium\|high` | OpenAI-style gateways, some vLLM builds |
| `template` | `chat_template_kwargs: {enable_thinking: bool}` | vLLM/SGLang with Qwen-style chat templates |

`--think off` is the one that matters most: for classification, extraction and
short deterministic answers, thinking costs tokens and latency and buys nothing.
If a server rejects the field with a 400, switch `--think-style` rather than
removing the flag — the other dialect is usually accepted.

## Structured output

`--json-mode` sends `response_format: {"type": "json_object"}`. Two things to
know:

- Some servers require the word "json" to appear in the prompt, otherwise they
  return prose and look broken.
- JSON mode constrains syntax, not schema. Validate the parsed object yourself;
  a valid JSON document with the wrong keys is still a failure.

## Errors

| Exit | Meaning | First move |
| --- | --- | --- |
| 2 | no prompt | pass `--prompt` or `--stdin` |
| 3 | no base URL | pass `--base-url` or set `LLM_BASE_URL` |
| 4 | cannot connect, or timed out | check host/port; `--timeout` for slow models |
| 5 | 401/403 | key wrong or missing; the body says which |
| 6 | non-200, or a 200 that is not JSON | server-side; `--dry-run` to confirm the request |
| 7 | 200 with no usable content | see the reasoning-model table above |

`--retry` retries exactly once, and only for connection errors and 5xx. Never
retry a 4xx: the request is wrong and will stay wrong.

## Choosing a model

The client does not ship a model table — that belongs to your deployment. Decide
by capability, in this order:

1. **Does it need tools?** If yes, the model must support function calling; a
   reasoning model without it is the wrong pick no matter the benchmark.
2. **Does it need to see images?** Vision-capable or nothing.
3. **Is the task deterministic?** Extraction, classification and formatting
   usually want thinking **off** and a small model; multi-step reasoning wants
   thinking on and more `max_tokens`.
4. **Does the context fit?** A truncated prompt is a silent quality bug: the
   model answers confidently about the part it received. Count tokens before
   sending, not after.

Record the model name in the result envelope; a batch whose model is unknown is
not reproducible.

## Batching

Call the script per item and keep `--json` output; the client is stateless and
does not pool connections. For hundreds of calls, wrap it in your own loop with
a small concurrency limit and log `usage.total_tokens` per call — the aggregate
is the only reliable cost figure.

## Verification

```bash
python -X utf8 tests/run_tests.py     # 38 assertions, no API key, no network
```

`tests/stub_server.py` serves `/v1/chat/completions` with scenarios for the
reasoning-only reply, truncation, auth failure, 500, non-JSON 200, empty
choices, a hang, and a flaky endpoint that needs the single retry. Both thinking
dialects are asserted against the request bodies the server actually received.