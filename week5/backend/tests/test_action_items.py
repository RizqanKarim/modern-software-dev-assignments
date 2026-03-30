def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    page = r.json()
    assert "items" in page
    assert "total" in page
    assert "page" in page
    assert "page_size" in page
    assert len(page["items"]) == 1
    assert page["total"] == 1


def test_action_items_pagination(client):
    # Create 3 action items
    for i in range(3):
        client.post("/action-items/", json={"description": f"Task {i}"})

    # page_size=2 should return first 2 items
    r = client.get("/action-items/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    page = r.json()
    assert page["total"] == 3
    assert len(page["items"]) == 2
    assert page["page"] == 1
    assert page["page_size"] == 2

    # page 2 should return the remaining 1 item
    r = client.get("/action-items/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    page = r.json()
    assert page["total"] == 3
    assert len(page["items"]) == 1

    # empty last page (beyond total)
    r = client.get("/action-items/", params={"page": 10, "page_size": 10})
    assert r.status_code == 200
    page = r.json()
    assert page["items"] == []
    assert page["total"] == 3

    # page_size capped at 100; requesting 101 should return 422
    r = client.get("/action-items/", params={"page": 1, "page_size": 101})
    assert r.status_code == 422

    # page < 1 should return 422
    r = client.get("/action-items/", params={"page": 0})
    assert r.status_code == 422
