"""Unit tests for tessera_llamaindex._config.

These tests run without LlamaIndex installed. They verify the returned
kwargs dicts have the right shape for each provider's LLM constructor.
"""

from __future__ import annotations

import pytest

from tessera_llamaindex import (
    TESSERA_BASE_URL,
    tessera_openai_config,
    tessera_anthropic_config,
    tessera_mistral_config,
    tessera_groq_config,
    tessera_cohere_config,
    tessera_config,
)


class TestOpenAI:
    def test_default(self):
        cfg = tessera_openai_config(api_key="tk_test")
        assert cfg["api_base"] == f"{TESSERA_BASE_URL}/v1/openai"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}

    def test_extra_headers_merge(self):
        cfg = tessera_openai_config(
            api_key="tk_test",
            extra_headers={"x-trace": "abc"},
        )
        assert cfg["default_headers"] == {
            "x-tessera-api-key": "tk_test",
            "x-trace": "abc",
        }

    def test_custom_base_url_override(self):
        cfg = tessera_openai_config(
            api_key="tk_test",
            base_url="https://staging.tesseraai.io/v1/openai",
        )
        assert cfg["api_base"] == "https://staging.tesseraai.io/v1/openai"


class TestAnthropic:
    def test_default(self):
        cfg = tessera_anthropic_config(api_key="tk_test")
        assert cfg["base_url"] == f"{TESSERA_BASE_URL}/v1/anthropic"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}


class TestMistral:
    def test_default(self):
        cfg = tessera_mistral_config(api_key="tk_test")
        assert cfg["endpoint"] == f"{TESSERA_BASE_URL}/v1/mistral"
        # MistralAI doesn't accept default_headers directly — headers go via
        # additional_kwargs.http_headers which propagates to the underlying SDK.
        assert cfg["additional_kwargs"] == {
            "http_headers": {"x-tessera-api-key": "tk_test"}
        }


class TestGroq:
    def test_default(self):
        cfg = tessera_groq_config(api_key="tk_test")
        assert cfg["api_base"] == f"{TESSERA_BASE_URL}/v1/groq"
        assert cfg["default_headers"] == {"x-tessera-api-key": "tk_test"}


class TestCohere:
    def test_default(self):
        cfg = tessera_cohere_config(api_key="tk_test")
        assert cfg["base_url"] == f"{TESSERA_BASE_URL}/v1/cohere"
        # Cohere uses additional_kwargs.headers instead of default_headers
        assert cfg["additional_kwargs"] == {
            "headers": {"x-tessera-api-key": "tk_test"}
        }


class TestGenericDispatcher:
    @pytest.mark.parametrize(
        "provider,base_url_key",
        [
            ("openai", "api_base"),
            ("anthropic", "base_url"),
            ("mistral", "endpoint"),
            ("groq", "api_base"),
            ("cohere", "base_url"),
        ],
    )
    def test_provider_routing(self, provider, base_url_key):
        cfg = tessera_config(provider=provider, api_key="tk_test")
        assert cfg[base_url_key] == f"{TESSERA_BASE_URL}/v1/{provider}"

    def test_unknown_provider_raises(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            tessera_config(provider="not-a-provider", api_key="tk_test")  # type: ignore[arg-type]


class TestValidation:
    def test_empty_api_key_raises(self):
        with pytest.raises(ValueError, match="non-empty string"):
            tessera_openai_config(api_key="")

    def test_non_string_api_key_raises(self):
        with pytest.raises(ValueError, match="non-empty string"):
            tessera_openai_config(api_key=None)  # type: ignore[arg-type]
