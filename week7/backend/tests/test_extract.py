from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    result = extract_action_items(text)
    assert "TODO: write tests" in result["action_items"]
    assert "ACTION: review PR" in result["action_items"]
    assert "Ship it!" in result["action_items"]
    assert result["tags"] == []


def test_extract_markdown_checkboxes():
    text = """
    # Project Tasks
    - [ ] Write documentation
    - [x] Set up CI/CD
    - [ ] Review code changes
    - Normal bullet point
    """
    result = extract_action_items(text)
    assert "Write documentation" in result["action_items"]
    assert "[DONE] Set up CI/CD" in result["action_items"]
    assert "Review code changes" in result["action_items"]
    assert "Normal bullet point" not in result["action_items"]


def test_extract_tags():
    text = """
    Meeting notes #meeting #urgent
    - TODO: follow up with team #followup
    - [ ] Update project plan #planning
    """
    result = extract_action_items(text)
    assert "meeting" in result["tags"]
    assert "urgent" in result["tags"]
    assert "followup" in result["tags"]
    assert "planning" in result["tags"]


def test_extract_action_verbs():
    text = """
    Call the client tomorrow
    Buy groceries after work
    Just thinking about it
    """
    result = extract_action_items(text)
    assert "Call the client tomorrow" in result["action_items"]
    assert "Buy groceries after work" in result["action_items"]
    assert "Just thinking about it" not in result["action_items"]


def test_extract_markdown_headers():
    text = """
    # TODO List
    ## Action Items
    - [ ] Task one
    # Completed Tasks
    """
    result = extract_action_items(text)
    assert "Header: TODO List" in result["action_items"]
    assert "Header: Action Items" in result["action_items"]
    assert "Header: Completed Tasks" not in result["action_items"]


def test_extract_error_handling():
    # Test with invalid input
    result = extract_action_items(None)
    assert result["action_items"] == []
    assert result["tags"] == []
    assert "error" in result

    # Test with empty string
    result = extract_action_items("")
    assert result["action_items"] == []
    assert result["tags"] == []
    assert "error" not in result


