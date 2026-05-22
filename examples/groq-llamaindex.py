"""
groq-llamaindex.py — LlamaIndex Groq through the Tessera proxy.

Usage:

    pip install tessera-llamaindex llama-index-llms-groq
    export GROQ_API_KEY=gsk_...
    export TESSERA_API_KEY=tk_...
    python groq-llamaindex.py
"""

from __future__ import annotations

import os

from llama_index.core.llms import ChatMessage
from llama_index.llms.groq import Groq

from tessera_llamaindex import tessera_groq_config


def main() -> None:
    groq_key = os.environ['GROQ_API_KEY']
    tessera_key = os.environ['TESSERA_API_KEY']

    llm = Groq(
        model='llama-3.3-70b-versatile',
        api_key=groq_key,
        **tessera_groq_config(api_key=tessera_key),
    )

    response = llm.chat(
        [
            ChatMessage(
                role='user',
                content="How does Groq's LPU architecture differ from a GPU for inference workloads? 3 concise bullets.",
            ),
        ]
    )

    print(response)


if __name__ == '__main__':
    main()
