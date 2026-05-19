# Contributing to tessera-llamaindex

Thanks for your interest. The package is Apache-2.0 licensed and PRs are welcome.

For the canonical contributing rules (style, what we want, what we don't want,
PR review expectations) see
[`tessera-llm/tessera-sdk/CONTRIBUTING.md`](https://github.com/tessera-llm/tessera-sdk/blob/main/CONTRIBUTING.md).
This file documents the package-specific bits.

## Reporting bugs

Open an issue at
[github.com/tessera-llm/tessera-llamaindex/issues](https://github.com/tessera-llm/tessera-llamaindex/issues)
with:

- Package version (`pip show tessera-llamaindex` for Python, `npm list @tessera-llm/llamaindex` for Node)
- LlamaIndex version (`pip show llama-index llama-index-llms-openai` etc.)
- Language runtime version
- Minimum reproduction snippet
- Expected vs. actual behaviour

For security vulnerabilities, see [`SECURITY.md`](./SECURITY.md) — please do
not file public issues.

## Development setup

This repo carries two parallel implementations — Python and Node — sharing
the same wire format against the Tessera proxy.

### Python

```bash
cd python
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

### Node / TypeScript

```bash
cd node
npm install
npm test
npm run build
```

The CI workflow under `.github/workflows/` runs the same checks on every
push and pull request — keep it green.

## Package-specific scope

LlamaIndex's LLM abstraction lives in `llama_index.llms.<provider>` (Python)
and `@llamaindex/<provider>` (Node). The Tessera wrapper exposes a
`with_tessera(...)` helper that patches the LLM with the proxy base URL +
Tessera key header. Keep new provider wrappers tiny — one helper per
upstream provider, no RAG / index / agent logic inside the wrapper (that
belongs in LlamaIndex core or in user application code).

## Contact

- Bug reports: GitHub Issues.
- Security: [security@tesseraai.io](mailto:security@tesseraai.io).
- Code of Conduct enforcement: [conduct@tesseraai.io](mailto:conduct@tesseraai.io).
- General: [founder@tesseraai.io](mailto:founder@tesseraai.io).
