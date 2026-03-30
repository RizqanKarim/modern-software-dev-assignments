import os
import pytest

from ..app.services.extract import extract_action_items


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items
import json
from unittest.mock import patch

# Since extract_action_items_llm is not imported at the top, import it here, using full path
from ..app.services.extract import extract_action_items_llm


@pytest.mark.parametrize(
    "text,ollama_response,expected",
    [
        (
            # Simple bullet list
            "- Do thing one\n- Do thing two",
            {"message": {"content": json.dumps(["Do thing one", "Do thing two"])}},
            ["Do thing one", "Do thing two"],
        ),
        (
            # Text with keyword prefixes
            "TODO: Refactor codebase\naction: Update dependencies",
            {"message": {"content": json.dumps(["Refactor codebase", "Update dependencies"])}},
            ["Refactor codebase", "Update dependencies"],
        ),
        (
            # Empty string
            "",
            {"message": {"content": json.dumps([])}},
            [],
        ),
        (
            # Text with no action items
            "There's nothing to do here. No tasks awaiting.",
            {"message": {"content": json.dumps([])}},
            [],
        ),
        (
            # Ollama returns something not a list (should fallback to empty)
            "Something odd",
            {"message": {"content": json.dumps({"not": "a list"})}},
            [],
        ),
        (
            # Ollama returns invalid JSON (should safely return empty)
            "Break parsing",
            {"message": {"content": "[this is not valid json]"}},
            [],
        )
    ]
)
def test_extract_action_items_llm(text, ollama_response, expected):
    with patch("..app.services.extract.ollama.chat", return_value=ollama_response):
        result = extract_action_items_llm(text)
        assert result == expected
