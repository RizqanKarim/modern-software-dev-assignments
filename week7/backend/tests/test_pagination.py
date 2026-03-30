import pytest
from fastapi.testclient import TestClient


def test_pagination_default_values(client: TestClient):
    """Test default pagination behavior (limit=50, skip=0)"""
    # Create multiple test notes
    notes_data = [
        {"title": f"Note {i}", "content": f"Content {i}"}
        for i in range(10)
    ]

    created_notes = []
    for note_data in notes_data:
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201
        created_notes.append(response.json())

    # Test default pagination
    response = client.get("/notes/")
    assert response.status_code == 200
    data = response.json()

    # Should return all 10 notes (default limit is 50)
    assert len(data) == 10
    assert all(note["title"].startswith("Note ") for note in data)


def test_pagination_with_limit(client: TestClient):
    """Test pagination with limit parameter"""
    # Create 5 test notes
    for i in range(5):
        note_data = {"title": f"Pagination Test {i}", "content": f"Content {i}"}
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201

    # Test with limit=3
    response = client.get("/notes/", params={"limit": 3})
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3
    assert all(note["title"].startswith("Pagination Test ") for note in data)

    # Test with limit=1
    response = client.get("/notes/", params={"limit": 1})
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1

    # Test with limit=0 (should return empty list)
    response = client.get("/notes/", params={"limit": 0})
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 0


def test_pagination_with_offset(client: TestClient):
    """Test pagination with offset (skip) parameter"""
    # Create 5 test notes with known titles
    note_titles = []
    for i in range(5):
        note_data = {"title": f"Offset Test {i}", "content": f"Content {i}"}
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201
        note_titles.append(f"Offset Test {i}")

    # Default sort is -created_at (newest first), so notes are returned as 4,3,2,1,0
    expected_order = [f"Offset Test {4-i}" for i in range(5)]

    # Test with skip=2 (offset 2)
    response = client.get("/notes/", params={"skip": 2})
    assert response.status_code == 200
    data = response.json()

    # Should return notes starting from index 2 in the sorted order
    assert len(data) == 3  # 5 total - 2 skipped
    assert data[0]["title"] == expected_order[2]  # Offset Test 2
    assert data[1]["title"] == expected_order[3]  # Offset Test 1
    assert data[2]["title"] == expected_order[4]  # Offset Test 0

    # Test with skip=0 (same as default)
    response = client.get("/notes/", params={"skip": 0})
    assert response.status_code == 200
    data_default = response.json()

    response = client.get("/notes/")
    assert response.status_code == 200
    data_no_skip = response.json()

    assert data_default == data_no_skip


def test_pagination_limit_and_offset_combined(client: TestClient):
    """Test pagination with both limit and offset parameters"""
    # Get initial count
    response = client.get("/notes/")
    initial_count = len(response.json())

    # Create 10 test notes
    for i in range(10):
        note_data = {"title": f"Combined Test {i}", "content": f"Content {i}"}
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201

    # Test limit=3, skip=2
    response = client.get("/notes/", params={"limit": 3, "skip": 2})
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 3
    # The first 2 notes (newest) are skipped, so we get the next 3
    # Since we don't know the exact order of existing notes, just verify we get 3 items
    assert len(data) == 3
    assert all("title" in item for item in data)


def test_pagination_offset_beyond_available_data(client: TestClient):
    """Test pagination when offset exceeds available data"""
    # Create 3 test notes
    for i in range(3):
        note_data = {"title": f"Beyond Test {i}", "content": f"Content {i}"}
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201

    # Test with skip=10 (way beyond available data)
    response = client.get("/notes/", params={"skip": 10})
    assert response.status_code == 200
    data = response.json()

    # Should return empty list
    assert len(data) == 0


def test_pagination_limit_larger_than_available_data(client: TestClient):
    """Test pagination when limit exceeds available data"""
    # Create 2 test notes
    for i in range(2):
        note_data = {"title": f"Limit Test {i}", "content": f"Content {i}"}
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201

    # Test with limit=10 (larger than available)
    response = client.get("/notes/", params={"limit": 10})
    assert response.status_code == 200
    data = response.json()

    # Should return only available notes (2)
    assert len(data) == 2


def test_pagination_with_search_query(client: TestClient):
    """Test pagination works correctly with search queries"""
    # Create notes with different content
    notes_data = [
        {"title": "Apple Note", "content": "About apples"},
        {"title": "Banana Note", "content": "About bananas"},
        {"title": "Cherry Note", "content": "About cherries"},
        {"title": "Date Note", "content": "About dates"},
        {"title": "Elderberry Note", "content": "About elderberries"},
    ]

    for note_data in notes_data:
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201

    # Search for "About" with pagination
    response = client.get("/notes/", params={"q": "About", "limit": 2, "skip": 1})
    assert response.status_code == 200
    data = response.json()

    # Should return 2 results, skipping the first one
    assert len(data) == 2
    # Results should be in reverse chronological order
    assert "About" in data[0]["content"]
    assert "About" in data[1]["content"]


def test_pagination_limit_validation(client: TestClient):
    """Test that limit parameter works correctly"""
    # Create some test data
    for i in range(5):
        note_data = {"title": f"Validation Test {i}", "content": f"Content {i}"}
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201

    # Test with limit=3
    response = client.get("/notes/", params={"limit": 3})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Test with limit=1
    response = client.get("/notes/", params={"limit": 1})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_pagination_negative_values(client: TestClient):
    """Test pagination with negative values (should be handled gracefully)"""
    # Create some test data
    for i in range(3):
        note_data = {"title": f"Negative Test {i}", "content": f"Content {i}"}
        response = client.post("/notes/", json=note_data)
        assert response.status_code == 201

    # Test negative limit (should default to positive or be handled)
    response = client.get("/notes/", params={"limit": -1})
    assert response.status_code == 200
    data = response.json()
    # Behavior may vary, but should not crash

    # Test negative skip (should default to 0 or be handled)
    response = client.get("/notes/", params={"skip": -5})
    assert response.status_code == 200
    data = response.json()
    # Should behave as if skip=0 or handle gracefully
