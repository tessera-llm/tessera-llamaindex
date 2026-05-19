"""
mistral-llamaindex.py — LlamaIndex Mistral through the Tessera proxy.

Usage:

    pip install tessera-llamaindex llama-index-llms-mistralai
    export MISTRAL_API_KEY=...
    export TESSERA_API_KEY=tk_...
    python mistral-llamaindex.py
"""

from __future__ import annotations

import os

from llama_index.core.llms import ChatMessage
from llama_index.llms.mistralai import MistralAI

from tessera_llamaindex import tessera_mistral_config


def main() -> None:
    mistral_key = os.environ["MISTRAL_API_KEY"]
    tessera_key = os.environ["TESSERA_API_KEY"]

    llm = MistralAI(
        model="mistral-large-latest",
        api_key=mistral_key,
        **tessera_mistral_config(api_key=tessera_key),
    )

    response = llm.chat(
        [
            ChatMessage(role="user", content="Summarise the trade-offs between top-k and top-p sampling in 3 bullets."),
        ]
    )

    print(response)


if __name__ == "__main__":
    main()
