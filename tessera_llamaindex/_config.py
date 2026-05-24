"""Provider-specific config dicts for routing LlamaIndex LLM constructors
through the Tessera proxy.

Each `tessera_<provider>_config(api_key=...)` returns a dict of kwargs
that can be unpacked into the corresponding LlamaIndex `llama_index.llms.*`
LLM constructor. The kwargs change two things: the upstream base URL (to
api.tesseraai.io) and the auth header (Tessera API key alongside the
existing provider key).

No LlamaIndex import is required by this module — the kwargs are plain
dicts that LlamaIndex LLM classes accept via their public init signatures.

Field names verified against LlamaIndex 0.6+ family (2026-05-19 runtime
constructor probe):
- llama_index.llms.openai.OpenAI         → api_base, default_headers
- llama_index.llms.anthropic.Anthropic   → base_url, default_headers
- llama_index.llms.mistralai.MistralAI   → endpoint, additional_kwargs={"http_headers": ...}
- llama_index.llms.groq.Groq             → api_base, default_headers (via OpenAILike inheritance)
- llama_index.llms.cohere.Cohere         → base_url, additional_kwargs={"headers": ...}

If LlamaIndex changes a field name in a future release, the corresponding
config function gets a patch release. Wire format stays the same.
"""

from __future__ import annotations

from typing import Any, Literal

TESSERA_BASE_URL = 'https://api.tesseraai.io'

ProviderName = Literal['openai', 'anthropic', 'mistral', 'groq', 'cohere']


def _validate_api_key(api_key: str) -> str:
    if not isinstance(api_key, str) or not api_key:
        raise ValueError(
            'tessera_*_config(api_key=...) requires a non-empty string. '
            'Get a free key from https://tesseraai.io/dev'
        )
    return api_key


def _proxy_endpoint(provider: ProviderName) -> str:
    return f'{TESSERA_BASE_URL}/v1/{provider}'


def _headers(api_key: str, extra: dict[str, str] | None = None) -> dict[str, str]:
    headers = {'x-tessera-api-key': api_key}
    if extra:
        headers.update(extra)
    return headers


def tessera_openai_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `llama_index.llms.openai.OpenAI(...)` to route through Tessera.

    Example::

        from llama_index.llms.openai import OpenAI
        from tessera_llamaindex import tessera_openai_config

        llm = OpenAI(
            model="gpt-4o",
            api_key="sk-...",
            **tessera_openai_config(api_key="tk_..."),
        )
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('openai')
    return {
        'api_base': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_anthropic_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `llama_index.llms.anthropic.Anthropic(...)` to route through Tessera."""
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('anthropic')
    return {
        'base_url': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_mistral_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `llama_index.llms.mistralai.MistralAI(...)` to route through Tessera.

    Note: MistralAI doesn't accept `default_headers` directly. Headers go
    via `additional_kwargs={"http_headers": ...}` which the LlamaIndex
    Mistral wrapper forwards to the underlying mistralai SDK per request.
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('mistral')
    return {
        'endpoint': endpoint,
        'additional_kwargs': {'http_headers': _headers(api_key, extra_headers)},
    }


def tessera_groq_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `llama_index.llms.groq.Groq(...)` to route through Tessera."""
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('groq')
    return {
        'api_base': endpoint,
        'default_headers': _headers(api_key, extra_headers),
    }


def tessera_cohere_config(
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Kwargs for `llama_index.llms.cohere.Cohere(...)` to route through Tessera.

    Note: Cohere's LlamaIndex wrapper uses `additional_kwargs` for headers
    rather than a direct `default_headers` field. We translate transparently.
    """
    api_key = _validate_api_key(api_key)
    endpoint = base_url or _proxy_endpoint('cohere')
    return {
        'base_url': endpoint,
        'additional_kwargs': {'headers': _headers(api_key, extra_headers)},
    }


def tessera_config(
    provider: ProviderName,
    api_key: str,
    extra_headers: dict[str, str] | None = None,
    base_url: str | None = None,
) -> dict[str, Any]:
    """Generic dispatcher — returns the right kwargs dict for the given provider."""
    mapping = {
        'openai': tessera_openai_config,
        'anthropic': tessera_anthropic_config,
        'mistral': tessera_mistral_config,
        'groq': tessera_groq_config,
        'cohere': tessera_cohere_config,
    }
    if provider not in mapping:
        raise ValueError(f'Unknown provider {provider!r}. Supported: {list(mapping)}')
    return mapping[provider](api_key=api_key, extra_headers=extra_headers, base_url=base_url)
