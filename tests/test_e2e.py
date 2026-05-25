"""E2E shape compatibility tests against the real LlamaIndex provider
constructors. Gated by the `llama-index-llms-*` packages being installed.

Test coverage extended 2026-05-19 to cover that 3 of 5 provider configs
had unverified constructor-signature claims. The unverified Mistral one
turned out to be wrong (default_headers vs additional_kwargs.http_headers)
and was fixed before this test was committed.

If a future llama-index-llms-* release changes its constructor signature
in a breaking way, these tests fail BEFORE we ship a release that would
break customers.

These tests are SKIPPED when the llama-index-llms-* package isn't
installed (so the unit-test-only suite still passes for downstream
users who never install LlamaIndex itself).
"""

from __future__ import annotations

import importlib
import pytest

from tessera_llamaindex import (
    tessera_openai_config,
    tessera_anthropic_config,
    tessera_mistral_config,
    tessera_groq_config,
    tessera_cohere_config,
)


def _has(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False


# The minimal contract we verify: each provider's constructor accepts the
# kwargs dict our config function returns, without raising. We do NOT
# assert post-construction attribute introspection because LlamaIndex
# providers do not uniformly expose their init args back as instance
# attributes (some are consumed and stored internally, some go through
# pydantic field renaming, some are forwarded to underlying SDK clients).
# Constructor-survives is the strongest portable check across all 5
# providers and pins our config-shape correctness in CI.


@pytest.mark.skipif(not _has("llama_index.llms.openai"), reason="llama-index-llms-openai not installed")
def test_openai_constructor_accepts_config():
    from llama_index.llms.openai import OpenAI

    # Should not raise.
    OpenAI(model="gpt-4o", api_key="sk-fake", **tessera_openai_config(api_key="tk_test"))


@pytest.mark.skipif(not _has("llama_index.llms.anthropic"), reason="llama-index-llms-anthropic not installed")
def test_anthropic_constructor_accepts_config():
    from llama_index.llms.anthropic import Anthropic

    Anthropic(
        model="claude-sonnet-4-5-20250929",
        api_key="sk-ant-fake",
        **tessera_anthropic_config(api_key="tk_test"),
    )


@pytest.mark.skipif(not _has("llama_index.llms.mistralai"), reason="llama-index-llms-mistralai not installed")
def test_mistral_constructor_accepts_config():
    from llama_index.llms.mistralai import MistralAI

    MistralAI(
        model="mistral-large-latest",
        api_key="fake",
        **tessera_mistral_config(api_key="tk_test"),
    )


@pytest.mark.skipif(not _has("llama_index.llms.groq"), reason="llama-index-llms-groq not installed")
def test_groq_constructor_accepts_config():
    from llama_index.llms.groq import Groq

    Groq(
        model="llama-3.3-70b-versatile",
        api_key="gsk-fake",
        **tessera_groq_config(api_key="tk_test"),
    )


@pytest.mark.skipif(not _has("llama_index.llms.cohere"), reason="llama-index-llms-cohere not installed")
def test_cohere_constructor_accepts_config():
    from llama_index.llms.cohere import Cohere

    Cohere(
        model="command-r-plus",
        api_key="fake",
        **tessera_cohere_config(api_key="tk_test"),
    )
