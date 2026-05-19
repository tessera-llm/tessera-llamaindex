"""
anthropic-llamaindex.py — LlamaIndex Anthropic through the Tessera proxy.

Usage:

    pip install tessera-llamaindex llama-index-llms-anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    export TESSERA_API_KEY=tk_...
    python anthropic-llamaindex.py
"""

from __future__ import annotations

import os

from llama_index.core.llms import ChatMessage
from llama_index.llms.anthropic import Anthropic

from tessera_llamaindex import tessera_anthropic_config


def main() -> None:
    anthropic_key = os.environ["ANTHROPIC_API_KEY"]
    tessera_key = os.environ["TESSERA_API_KEY"]

    llm = Anthropic(
        model="claude-sonnet-4-5-20250929",
        api_key=anthropic_key,
        **tessera_anthropic_config(api_key=tessera_key),
    )

    response = llm.chat(
        [
            ChatMessage(
                role="system",
                content=(
                    "You are a senior data engineer. Answer in 3 concise "
                    "bullets."
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    "Compare DuckDB versus ClickHouse for ad-hoc analytical "
                    "queries against ~100M-row Parquet datasets."
                ),
            ),
        ]
    )

    print(response)


if __name__ == "__main__":
    main()
