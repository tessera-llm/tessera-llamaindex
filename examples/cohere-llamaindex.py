"""
cohere-llamaindex.py — LlamaIndex Cohere through the Tessera proxy.

Usage:

    pip install tessera-llamaindex llama-index-llms-cohere
    export COHERE_API_KEY=...
    export TESSERA_API_KEY=tk_...
    python cohere-llamaindex.py
"""

from __future__ import annotations

import os

from llama_index.core.llms import ChatMessage
from llama_index.llms.cohere import Cohere

from tessera_llamaindex import tessera_cohere_config


def main() -> None:
    cohere_key = os.environ['COHERE_API_KEY']
    tessera_key = os.environ['TESSERA_API_KEY']

    llm = Cohere(
        model='command-r-plus-08-2024',
        api_key=cohere_key,
        **tessera_cohere_config(api_key=tessera_key),
    )

    response = llm.chat(
        [
            ChatMessage(
                role='user',
                content="Compare Cohere's Rerank model to a dense vector retriever for production RAG. 3 concise bullets.",
            ),
        ]
    )

    print(response)


if __name__ == '__main__':
    main()
