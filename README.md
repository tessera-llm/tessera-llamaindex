# `tessera-llamaindex`

**Drop-in cost optimization for LlamaIndex.** One line of config routes your existing `OpenAI` / `Anthropic` / `MistralAI` / `Groq` / `Cohere` LLM through the [Tessera](https://tesseraai.io) optimization proxy — auto-route to cheaper-equivalent models, exact + provider-prompt-cache hits, prompt compression with per-stack quality canary, batch arbitrage on async-tolerant calls. Free Sandbox tier: **60M tokens/month, no card**. Production: **20% of measured savings, $0 if we save you nothing**.

<!-- COMPANION-PACKAGES-START -->
Companion to [`tessera-sdk`](https://github.com/tessera-llm/tessera-sdk) (vanilla provider SDKs), [`tessera-langchain`](https://github.com/tessera-llm/tessera-langchain) (LangChain integration), [`tessera-vercel-ai`](https://github.com/tessera-llm/tessera-vercel-ai) (Vercel AI SDK integration), [`tessera-mastra`](https://github.com/tessera-llm/tessera-mastra) (Mastra Agent framework integration), [`tessera-pydantic-ai`](https://github.com/tessera-llm/tessera-pydantic-ai) (Pydantic AI integration), [`tessera-crewai`](https://github.com/tessera-llm/tessera-crewai) (CrewAI multi-agent integration), and [`tessera-autogen`](https://github.com/tessera-llm/tessera-autogen) (AutoGen 0.4+ multi-agent integration). Same proxy, same mechanic stack, LlamaIndex-shaped API.
<!-- COMPANION-PACKAGES-END -->

[![PyPI version](https://img.shields.io/pypi/v/tessera-llamaindex.svg)](https://pypi.org/project/tessera-llamaindex/) [![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)

---

## Install

```bash
pip install tessera-llamaindex
# Plus whichever LlamaIndex provider package you use:
pip install llama-index-llms-openai          # or llama-index-llms-anthropic / -mistralai / -groq / -cohere
```

Get a free Tessera API key (60M tokens/mo, no card) — [`tesseraai.io/dev`](https://tesseraai.io/dev).

---

## Quickstart

```python
from llama_index.llms.openai import OpenAI
from tessera_llamaindex import tessera_openai_config

llm = OpenAI(
    model="gpt-4o",
    api_key="sk-...",                              # your OpenAI key, unchanged
    **tessera_openai_config(api_key="tk_..."),    # one line, routes through Tessera
)

# Existing LlamaIndex code (queries, RAG pipelines, agents, sub-question
# engines, multi-step reasoning) runs unchanged.
response = llm.complete("Summarize this document in 3 bullets.")
```

Same pattern for the other 4 providers:

```python
from llama_index.llms.anthropic import Anthropic
from tessera_llamaindex import tessera_anthropic_config

llm = Anthropic(
    model="claude-sonnet-4-5-20250929",
    api_key="sk-ant-...",
    **tessera_anthropic_config(api_key="tk_..."),
)
```

---

## Provider support — verified constructor signatures

Field names runtime-verified against installed LlamaIndex 0.6+ provider packages:

| Provider | Tessera config function | LlamaIndex class | URL param | Headers approach |
|---|---|---|---|---|
| OpenAI | `tessera_openai_config` | `llama_index.llms.openai.OpenAI` | `api_base` | `default_headers` |
| Anthropic | `tessera_anthropic_config` | `llama_index.llms.anthropic.Anthropic` | `base_url` | `default_headers` |
| Mistral | `tessera_mistral_config` | `llama_index.llms.mistralai.MistralAI` | `endpoint` | `additional_kwargs.http_headers` |
| Groq | `tessera_groq_config` | `llama_index.llms.groq.Groq` | `api_base` | `default_headers` (via OpenAILike inheritance) |
| Cohere | `tessera_cohere_config` | `llama_index.llms.cohere.Cohere` | `base_url` | `additional_kwargs.headers` |

Generic dispatcher: `tessera_config(provider, api_key=...)` returns the right kwargs dict regardless of provider.

Each constructor-shape is locked into CI via `tests/test_e2e.py` — if a future LlamaIndex release changes the kwargs an `__init__` accepts, the regression fails before we ship.

---

## What Tessera does on every request

Same mechanic stack as the main [`tessera-sdk`](https://github.com/tessera-llm/tessera-sdk). Each mechanic is opt-in per workload, observable per request, and bypasses when its quality canary drops below the per-stack 0.95 floor.

| Mechanic | What it does | Typical savings |
|---|---|---|
| **Auto-route** <sub>(m1)</sub> | Route to a cheaper-equivalent model gated by a daily promptfoo canary on your eval set | 15–35% on routed calls |
| **Auto-cache** <sub>(m2)</sub> | sha256 cache on the canonical request body, 7-day TTL | 5–40% depending on prompt repetition |
| **Auto-compress** <sub>(m3)</sub> | Per-role heuristic compression (system + user toggles independent) | 5–15% on prompt tokens |
| **Prompt cache** <sub>(m6)</sub> | Inject provider-native cache headers — OpenAI 50% off, Anthropic 90% off cache reads | 50–90% on cached prefixes |
| **Context prune** <sub>(m7)</sub> | Conservative trim on long conversations + RAG attachments | 5–25% on multi-turn workloads |
| **Output-length ceiling** <sub>(m9)</sub> | Daily compute fits p90 of completion length per workload | 5–15% on completion cost |
| **Batch arbitrage** <sub>(m10)</sub> | Route async-tolerant calls to provider Batch APIs (50% off) | 50% on batch-eligible traffic |
| **Per-provider circuit breaker** | (Reliability primitive.) Rolling 5xx-rate state machine per upstream. | n/a — keeps the savings stack honest |

---

## Pricing

- **Free Sandbox** — 60M tokens/month, 30 requests/minute, observability-only mechanics, no card. Forever.
- **Production** — over 60M tokens/month or higher rate limit. **20% of measured savings only.** Zero savings, zero fee. Prepaid Stripe balance, $100 minimum top-up.

Existing customers of the other Tessera packages keep their `rate_locked_pct` (if any) on this package — same `tk_…` key, same billing record.

---

## FAQ

### Q: How is this different from `tessera-sdk`, `tessera-langchain`, `tessera-vercel-ai`?

Same proxy, same mechanics, same billing. The four packages target different code surfaces:

- **`tessera-sdk`** — patches provider SDK constructors directly (OpenAI, Anthropic, etc.) via one-line `tessera.activate(key)`. Use when calling provider SDKs without a framework.
- **`tessera-langchain`** — wires into LangChain `ChatModel` constructors.
- **`tessera-vercel-ai`** — wires into Vercel AI SDK `createX` provider factories.
- **`tessera-llamaindex`** *(this package)* — wires into LlamaIndex `llama_index.llms.*` LLM constructors.

Pick whichever fits your codebase. Side-by-side install is supported.

### Q: Does this break my RAG pipeline / query engine / agent?

No. The LlamaIndex `LLM` object behaves identically — `complete`, `chat`, `stream_complete`, `stream_chat` all work unchanged. Index queries, retrievers, sub-question engines, OpenAI Agents, multi-step reasoning chains all use the LLM's standard `complete`/`chat` interface and route through Tessera transparently.

### Q: What happens if Tessera's proxy is down?

Your application gets HTTP errors instead of LLM responses. On the proxy side, a per-provider circuit breaker tracks rolling 5xx rates and skips degraded providers in auto-route decisions. Cross-provider failover (re-routing to a different provider entirely when an upstream is down) is on the roadmap, not shipped yet.

### Q: What happens to my OpenAI / Anthropic rate limits?

They pass through. Tessera does not aggregate quotas across customers. Your provider rate limits apply normally; the proxy enforces only the Tessera tier limits (30 rpm Free Sandbox, 60 rpm Production by default — higher on request).

### Q: Are you storing my prompts and completions?

No. We log only token counts, cost deltas, mechanics_stack, and provider response status. Prompts and completions are never persisted. Full data handling on [`tesseraai.io/security`](https://tesseraai.io/security).

### Q: Why does Mistral use `additional_kwargs.http_headers` instead of `default_headers`?

LlamaIndex's MistralAI wrapper doesn't expose a top-level `default_headers` argument — it forwards `additional_kwargs.http_headers` to the underlying `mistralai` SDK on each request. The Tessera Mistral config function returns the correct shape for this. You don't need to know this; the config function abstracts it. Same story for Cohere (`additional_kwargs.headers`).

### Q: Can I use this with LlamaIndex's `Settings.llm = ...` global pattern?

Yes — just construct the LLM the same way and assign it:
```python
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from tessera_llamaindex import tessera_openai_config

Settings.llm = OpenAI(model="gpt-4o", api_key="sk-...", **tessera_openai_config(api_key="tk_..."))
```

---

## Architecture

Open-source SDK ↔ closed-source proxy. This package is a thin client that adds one HTTP hop. The actual mechanic decisions run inside the Tessera Cloudflare Worker proxy at `api.tesseraai.io`. The wire format is open; the mechanic implementations are closed.

## License

Apache-2.0. See [LICENSE](LICENSE).

## Versioning

Semver. Wire format compatibility committed across minor releases; breaking changes only on major bumps.

## Security

Coordinated disclosure address: `security@tesseraai.io`.

---

## About Tessera

Tessera is the **substrate layer** for **LLM cost optimization**, also called the **Optimize Layer** in our product surface. A thin proxy that sits in your application's **request-path**, applies a conservative cascade of optimization mechanics, and measures every saved dollar against an **audit-immutable** baseline. We bill **20% of verified savings**, prepaid. Zero savings = zero fee. No per-token gateway fee, no subscription, no minimum monthly commitment; the category we operate in is "**success-fee LLM optimizer**," distinct from per-token **AI gateways** and observability dashboards.

Where observability tools tell you what you spent and AI gateways re-shape the request without measuring the cost delta, Tessera is the layer that does both, and only takes a cut when the measured savings are positive. The **verified-savings ledger** at [`ledger.tesseraai.io`](https://ledger.tesseraai.io) shows every original-vs-actual cost pair, snapshot-pinned to a `pricing_catalog` version captured at request time. Mid-contract price changes don't retroactively alter past savings. This is the **FinOps**-friendly model for AI inference: every line of the bill traces to a code-enforced rule.

Operated by Fintechagency OÜ (Tallinn, Estonia, registry code 16638667).

- Developer entry: [tesseraai.io/dev](https://tesseraai.io/dev)
- Mechanic reference: [tesseraai.io/how-it-works](https://tesseraai.io/how-it-works)
- Dashboard: [ledger.tesseraai.io](https://ledger.tesseraai.io)
- Engineering blog: [tesseraai.io/blog](https://tesseraai.io/blog)
