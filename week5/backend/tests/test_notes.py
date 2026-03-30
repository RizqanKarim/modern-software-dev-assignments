def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    page = r.json()
    assert "items" in page
    assert "total" in page
    assert "page" in page
    assert "page_size" in page
    assert len(page["items"]) >= 1
    assert page["total"] >= 1
    assert page["page"] == 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_notes_pagination(client):
    # Create 3 notes
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    # page_size=2 should return first 2 items
    r = client.get("/notes/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    page = r.json()
    assert page["total"] == 3
    assert len(page["items"]) == 2
    assert page["page"] == 1
    assert page["page_size"] == 2

    # page 2 should return the remaining 1 item
    r = client.get("/notes/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    page = r.json()
    assert page["total"] == 3
    assert len(page["items"]) == 1

    # empty last page (beyond total)
    r = client.get("/notes/", params={"page": 10, "page_size": 10})
    assert r.status_code == 200
    page = r.json()
    assert page["items"] == []
    assert page["total"] == 3

    # page_size capped at 100; requesting 101 should return 422
    r = client.get("/notes/", params={"page": 1, "page_size": 101})
    assert r.status_code == 422

    # page < 1 should return 422
    r = client.get("/notes/", params={"page": 0})
    assert r.status_code == 422
