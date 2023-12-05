"""Utility functions for ResumeAI."""

from openai import OpenAI, AsyncOpenAI
import instructor

import os


def get_client(is_async: bool = False) -> OpenAI | AsyncOpenAI:
    """Create an OpenAI client with Helicone logging."""

    kwargs = {
        "base_url": "https://oai.hconeai.com/v1",
        "default_headers": {
            "Helicone-Auth": f"Bearer {os.environ['HELICONE_API_KEY']}",
            "Helicone-Property-Project": "ResumeAI"
        }
    }

    if is_async:
        client = AsyncOpenAI(**kwargs)
    else:
        client = OpenAI(**kwargs)

    return instructor.patch(client)


def extract_object(prompt, text, cls):
    """Extract a single object from a block of text."""

    client = get_client()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        response_model=cls,
        temperature=0.0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
    )

    return response
