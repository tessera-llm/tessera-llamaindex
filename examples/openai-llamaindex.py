"""
openai-llamaindex.py — LlamaIndex OpenAI through the Tessera proxy.

Usage:

    pip install tessera-llamaindex llama-index-llms-openai
    export OPENAI_API_KEY=sk-...
    export TESSERA_API_KEY=tk_...
    python openai-llamaindex.py
"""

from __future__ import annotations

import os

from llama_index.core.llms import ChatMessage
from llama_index.llms.openai import OpenAI

from tessera_llamaindex import tessera_openai_config


def main() -> None:
    openai_key = os.environ['OPENAI_API_KEY']
    tessera_key = os.environ['TESSERA_API_KEY']

    llm = OpenAI(
        model='gpt-4o',
        api_key=openai_key,
        **tessera_openai_config(api_key=tessera_key),
    )

    response = llm.chat(
        [
            ChatMessage(
                role='system',
                content=(
                    'You are a senior platform engineer reviewing infrastructure '
                    'decisions. Answer in 3 concise bullets.'
                ),
            ),
            ChatMessage(
                role='user',
                content=(
                    'Compare a service mesh sidecar approach vs an eBPF-based '
                    'approach for east-west traffic policy enforcement.'
                ),
            ),
        ]
    )

    print(response)


if __name__ == '__main__':
    main()
