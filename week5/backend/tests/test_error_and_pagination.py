"""
Task #10 – Test coverage improvements.

Covers:
  - 404 scenarios for every endpoint that can return one
  - 422 (validation) scenarios for every POST endpoint with invalid / missing fields
  - Pagination edge-cases from Task #8 not already present in the per-resource
    test files (empty collection, page_size=1 walk, max page_size boundary,
    default param reflection in response body)
"""

# ---------------------------------------------------------------------------
# Notes – 404 scenarios
# ---------------------------------------------------------------------------


def test_get_note_not_found(client):
    """GET /notes/{id} with a non-existent ID must return 404."""
    r = client.get("/notes/9999")
    assert r.status_code == 404


def test_get_note_invalid_id_type(client):
    """GET /notes/{id} with a non-integer path segment must return 422."""
    r = client.get("/notes/not-an-int")
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Notes – 422 validation scenarios (POST /notes/)
# ---------------------------------------------------------------------------


def test_create_note_missing_title(client):
    """POST /notes/ without 'title' must return 422."""
    r = client.post("/notes/", json={"content": "No title provided"})
    assert r.status_code == 422


def test_create_note_missing_content(client):
    """POST /notes/ without 'content' must return 422."""
    r = client.post("/notes/", json={"title": "No content provided"})
    assert r.status_code == 422


def test_create_note_empty_body(client):
    """POST /notes/ with an empty JSON object must return 422."""
    r = client.post("/notes/", json={})
    assert r.status_code == 422


def test_create_note_null_fields(client):
    """POST /notes/ with null fields must return 422."""
    r = client.post("/notes/", json={"title": None, "content": None})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Action items – 404 scenarios
# ---------------------------------------------------------------------------


def test_complete_action_item_not_found(client):
    """PUT /action-items/{id}/complete with a non-existent ID must return 404."""
    r = client.put("/action-items/9999/complete")
    assert r.status_code == 404


def test_complete_action_item_invalid_id_type(client):
    """PUT /action-items/{id}/complete with a non-integer segment must return 422."""
    r = client.put("/action-items/not-an-int/complete")
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Action items – 422 validation scenarios (POST /action-items/)
# ---------------------------------------------------------------------------


def test_create_action_item_missing_description(client):
    """POST /action-items/ without 'description' must return 422."""
    r = client.post("/action-items/", json={})
    assert r.status_code == 422


def test_create_action_item_null_description(client):
    """POST /action-items/ with null 'description' must return 422."""
    r = client.post("/action-items/", json={"description": None})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# Notes – Pagination edge cases (Task #8)
# ---------------------------------------------------------------------------


def test_list_notes_empty_collection(client):
    """GET /notes/ on an empty DB returns total=0 and an empty items list."""
    r = client.get("/notes/")
    assert r.status_code == 200
    page = r.json()
    assert page["items"] == []
    assert page["total"] == 0
    assert page["page"] == 1
    assert page["page_size"] == 10


def test_list_notes_default_params_reflected(client):
    """Default page/page_size values (1/10) are echoed back in the response."""
    r = client.get("/notes/")
    assert r.status_code == 200
    page = r.json()
    assert page["page"] == 1
    assert page["page_size"] == 10


def test_list_notes_page_size_one(client):
    """page_size=1 walks through three notes one at a time."""
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    for pg in range(1, 4):
        r = client.get("/notes/", params={"page": pg, "page_size": 1})
        assert r.status_code == 200
        page = r.json()
        assert len(page["items"]) == 1, f"Expected 1 item on page {pg}"
        assert page["total"] == 3
        assert page["page"] == pg
        assert page["page_size"] == 1


def test_list_notes_max_page_size_allowed(client):
    """page_size=100 (the maximum allowed value) must succeed with 200."""
    r = client.get("/notes/", params={"page": 1, "page_size": 100})
    assert r.status_code == 200
    page = r.json()
    assert page["page_size"] == 100


def test_list_notes_page_size_above_max(client):
    """page_size=101 (above the maximum) must return 422."""
    r = client.get("/notes/", params={"page": 1, "page_size": 101})
    assert r.status_code == 422


def test_list_notes_page_below_minimum(client):
    """page=0 (below the minimum of 1) must return 422."""
    r = client.get("/notes/", params={"page": 0})
    assert r.status_code == 422


def test_list_notes_page_beyond_last(client):
    """Requesting a page well past the last page returns items=[] but correct total."""
    client.post("/notes/", json={"title": "Only note", "content": "Hello"})

    r = client.get("/notes/", params={"page": 100, "page_size": 10})
    assert r.status_code == 200
    page = r.json()
    assert page["items"] == []
    assert page["total"] == 1


# ---------------------------------------------------------------------------
# Action items – Pagination edge cases (Task #8)
# ---------------------------------------------------------------------------


def test_list_action_items_empty_collection(client):
    """GET /action-items/ on an empty DB returns total=0 and an empty items list."""
    r = client.get("/action-items/")
    assert r.status_code == 200
    page = r.json()
    assert page["items"] == []
    assert page["total"] == 0
    assert page["page"] == 1
    assert page["page_size"] == 10


def test_list_action_items_default_params_reflected(client):
    """Default page/page_size values (1/10) are echoed back in the response."""
    r = client.get("/action-items/")
    assert r.status_code == 200
    page = r.json()
    assert page["page"] == 1
    assert page["page_size"] == 10


def test_list_action_items_page_size_one(client):
    """page_size=1 walks through three action items one at a time."""
    for i in range(3):
        client.post("/action-items/", json={"description": f"Task {i}"})

    for pg in range(1, 4):
        r = client.get("/action-items/", params={"page": pg, "page_size": 1})
        assert r.status_code == 200
        page = r.json()
        assert len(page["items"]) == 1, f"Expected 1 item on page {pg}"
        assert page["total"] == 3
        assert page["page"] == pg
        assert page["page_size"] == 1


def test_list_action_items_max_page_size_allowed(client):
    """page_size=100 (the maximum allowed value) must succeed with 200."""
    r = client.get("/action-items/", params={"page": 1, "page_size": 100})
    assert r.status_code == 200
    page = r.json()
    assert page["page_size"] == 100


def test_list_action_items_page_size_above_max(client):
    """page_size=101 (above the maximum) must return 422."""
    r = client.get("/action-items/", params={"page": 1, "page_size": 101})
    assert r.status_code == 422


def test_list_action_items_page_below_minimum(client):
    """page=0 (below the minimum of 1) must return 422."""
    r = client.get("/action-items/", params={"page": 0})
    assert r.status_code == 422


def test_list_action_items_page_beyond_last(client):
    """Requesting a page well past the last page returns items=[] but correct total."""
    client.post("/action-items/", json={"description": "Only item"})

    r = client.get("/action-items/", params={"page": 100, "page_size": 10})
    assert r.status_code == 200
    page = r.json()
    assert page["items"] == []
    assert page["total"] == 1
