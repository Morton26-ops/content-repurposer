from collections.abc import AsyncIterator

import anthropic

from config import settings
from prompts import SYSTEM_PROMPT, get_prompt


async def stream_repurposed_content(platform: str, content: str) -> AsyncIterator[str]:
    """Stream repurposed content from Claude, yielding text chunks."""
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    user_prompt = get_prompt(platform, content)

    async with client.messages.stream(
        model=settings.model,
        max_tokens=settings.max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    ) as stream:
        async for text in stream.text_stream:
            yield text
