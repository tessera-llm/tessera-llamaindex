# Security Policy

If you find a vulnerability in `tessera-llamaindex` or in the way it interacts
with the Tessera proxy, please report it privately.

**Email:** security@tesseraai.io

We aim to acknowledge reports within two business days and to ship a fix or a
public mitigation note within 90 days of the initial report. If a report is
materially time-sensitive (active exploitation, credential exposure) we cut a
release immediately and notify all PyPI / npm installs on next install.

For the umbrella Tessera security policy, see
[`tessera-llm/tessera-sdk/SECURITY.md`](https://github.com/tessera-llm/tessera-sdk/blob/main/SECURITY.md).

## Scope

In scope:

- The published Python package `tessera-llamaindex` on PyPI.
- The published npm package `@tessera-llm/llamaindex`.
- The runnable examples under `examples/`.
- The wire format the wrapper uses to talk to the Tessera proxy at
  `api.tesseraai.io` (header names, base-URL handling, auth surface).

Out of scope:

- The internal implementation of the Tessera proxy itself (report proxy-side
  vulnerabilities to the same email; we do not publish the proxy source).
- The Tessera dashboard at `ledger.tesseraai.io` — same email, same SLA.
- LlamaIndex core itself — report to
  [run-llama/llama_index](https://github.com/run-llama/llama_index)
  first; we will fast-follow.

## What to include

A clean reproduction is the fastest path to a fix. Please include:

1. Package language and version (`pip show tessera-llamaindex` /
   `npm list @tessera-llm/llamaindex`).
2. LlamaIndex version.
3. Minimal repro code or a curl command.
4. Expected behaviour vs. observed behaviour.
5. Any logs, stack traces, or HTTP responses.

If your report includes potentially sensitive data (a prompt, an API key
fragment, customer identifiers), encrypt the payload with our PGP key on
request — email `security@tesseraai.io` and we will send the key.

## Disclosure

We follow a 90-day responsible disclosure window. Reporters are credited in
the corresponding `CHANGELOG.md` entry unless they prefer anonymity.

## Out-of-band

If you cannot reach `security@tesseraai.io`, DM `@govpun1-web` on GitHub for
a fallback channel. Please do not file public issues for unpatched
vulnerabilities.

Tessera is operated by Fintechagency OÜ, Tallinn, Estonia (registry 16638667).
