# ruff: noqa: RUF002
# (U+00D7 MULTIPLICATION SIGN in docstrings is intentional branding glyph, not letter x.)
"""Tessera × LlamaIndex integration — drop-in cost optimization for any LlamaIndex LLM.

Usage (most common):

    from llama_index.llms.openai import OpenAI
    from tessera_llamaindex import tessera_openai_config

    llm = OpenAI(
        model="gpt-4o",
        api_key="sk-...",
        **tessera_openai_config(api_key="tk_..."),
    )

    # Existing LlamaIndex code runs unchanged — queries, RAG pipelines,
    # agents, sub-question engines, all route through Tessera proxy.

See https://tesseraai.io/dev for the dashboard, free tier, and full
mechanic documentation.
"""

from tessera_llamaindex._config import (
    TESSERA_BASE_URL,
    tessera_anthropic_config,
    tessera_cohere_config,
    tessera_config,
    tessera_groq_config,
    tessera_mistral_config,
    tessera_openai_config,
)
from tessera_llamaindex._version import __version__

__all__ = [
    'TESSERA_BASE_URL',
    '__version__',
    'tessera_anthropic_config',
    'tessera_cohere_config',
    'tessera_config',
    'tessera_groq_config',
    'tessera_mistral_config',
    'tessera_openai_config',
]
