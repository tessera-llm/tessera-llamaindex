# Changelog

All notable changes to `tessera-llamaindex` documented here. Follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- README cross-link block extended to include `tessera-mastra` (Mastra Agent
  framework integration) and `tessera-pydantic-ai` (Pydantic AI integration)
  — Tessera's sibling-package roster now covers six framework surfaces.
  No code change in this package; the cross-link refresh ships on the next
  code-driven version bump per the package's piggy-back policy.

## [0.1.0] — 2026-05-19 — first public release

### Added

- **Config functions** for the five LlamaIndex LLM providers most-used in production:
  - `tessera_openai_config(api_key=...)` → kwargs for `llama_index.llms.openai.OpenAI(...)`
  - `tessera_anthropic_config(api_key=...)` → kwargs for `llama_index.llms.anthropic.Anthropic(...)`
  - `tessera_mistral_config(api_key=...)` → kwargs for `llama_index.llms.mistralai.MistralAI(...)`
  - `tessera_groq_config(api_key=...)` → kwargs for `llama_index.llms.groq.Groq(...)`
  - `tessera_cohere_config(api_key=...)` → kwargs for `llama_index.llms.cohere.Cohere(...)`
- `tessera_config(provider, api_key=...)` — generic dispatcher.
- Optional `extra_headers` and `base_url` parameters on every config function.
- All 5 provider configs **runtime-verified** against installed LlamaIndex 0.6+ packages — constructor-survives tests gate every release in CI.

### Verified shapes

Field names locked in via `tests/test_e2e.py`:
- OpenAI / Groq (via OpenAILike inheritance): `api_base` + `default_headers`
- Anthropic: `base_url` + `default_headers`
- Mistral: `endpoint` + `additional_kwargs.http_headers` (LlamaIndex Mistral doesn't expose top-level `default_headers`; forwarded via underlying `mistralai` SDK)
- Cohere: `base_url` + `additional_kwargs.headers`

### Architecture notes

- Same proxy as `tessera-sdk` / `tessera-langchain` / `tessera-vercel-ai`. Same `tsr_…` API key works across all four; same billing record. Safe to install side by side.
- Open-source thin client × closed-source proxy at `api.tesseraai.io`.
- No `llama-index-*` dependencies in the package itself. Config functions return plain dicts that LlamaIndex LLM classes accept via their public init signatures.

### CI + tooling

- pytest unit tests (15 cases covering shape + dispatcher + validation)
- pytest E2E tests (5 cases, one per provider; SKIP if `llama-index-llms-*` not installed)
- Python 3.9–3.12 matrix
- PEP 561 `py.typed` marker for `mypy --strict` recognition
- Apache-2.0 license

[Unreleased]: https://github.com/tessera-llm/tessera-llamaindex/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/tessera-llm/tessera-llamaindex/releases/tag/v0.1.0
