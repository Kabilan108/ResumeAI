"""Utility functions for ResumeAI."""

import openai

from .openai import patch

patch()


def extract_object(prompt, text, cls):
    """Extract a single object from a block of text."""

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        functions=[cls.openai_schema],
        function_call={"name": cls.openai_schema["name"]},
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            },
        ]
    )

    return cls.from_response(completion)
