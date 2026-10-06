def test_purchase_book_decrements_stock(client, registered_user, sample_book):
    response = client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    assert response.status_code == 200

    book_response = client.get(f"/books/{sample_book['id']}")
    assert book_response.json()["stock_quantity"] == sample_book["stock_quantity"] - 1


def test_purchase_requires_auth(client, sample_book):
    response = client.post(f"/books/{sample_book['id']}/purchase")
    assert response.status_code == 401


def test_purchase_out_of_stock_book_fails(client, admin_user, registered_user, sample_author):
    create_response = client.post(
        "/books",
        json={
            "title": "Rare Book",
            "description": "None left",
            "price": "50.00",
            "stock_quantity": 0,
            "author_id": sample_author
        },
        headers=admin_user["headers"]
    )
    book_id = create_response.json()["id"]

    response = client.post(f"/books/{book_id}/purchase", headers=registered_user["headers"])
    assert response.status_code == 400


def test_purchase_appears_in_history(client, registered_user, sample_book):
    client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    response = client.get("/me/purchases", headers=registered_user["headers"])
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["book"]["id"] == sample_book["id"]


def test_review_requires_purchase(client, registered_user, sample_book):
    response = client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 5, "text": "Loved it"},
        headers=registered_user["headers"]
    )
    assert response.status_code == 403


def test_review_after_purchase_succeeds(client, registered_user, sample_book):
    client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    response = client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 5, "text": "Loved it"},
        headers=registered_user["headers"]
    )
    assert response.status_code == 200
    assert response.json()["rating"] == 5


def test_duplicate_review_fails(client, registered_user, sample_book):
    client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 5, "text": "Loved it"},
        headers=registered_user["headers"]
    )
    response = client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 3, "text": "Second attempt"},
        headers=registered_user["headers"]
    )
    assert response.status_code == 400


def test_rating_out_of_range_rejected(client, registered_user, sample_book):
    client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    response = client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 10, "text": "Too high"},
        headers=registered_user["headers"]
    )
    assert response.status_code == 422 

def test_owner_can_delete_own_review(client, registered_user, sample_book):
    client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    review_response = client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 5, "text": "Loved it"},
        headers=registered_user["headers"]
    )
    review_id = review_response.json()["id"]

    response = client.delete(f"/reviews/{review_id}", headers=registered_user["headers"])
    assert response.status_code == 200


def test_other_user_cannot_delete_review(client, registered_user, second_user, sample_book):
    client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    review_response = client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 5, "text": "Loved it"},
        headers=registered_user["headers"]
    )
    review_id = review_response.json()["id"]

    response = client.delete(f"/reviews/{review_id}", headers=second_user["headers"])
    assert response.status_code == 403


def test_admin_can_delete_any_review(client, admin_user, registered_user, sample_book):
    client.post(f"/books/{sample_book['id']}/purchase", headers=registered_user["headers"])
    review_response = client.post(
        f"/books/{sample_book['id']}/reviews",
        json={"rating": 5, "text": "Loved it"},
        headers=registered_user["headers"]
    )
    review_id = review_response.json()["id"]

    response = client.delete(f"/reviews/{review_id}", headers=admin_user["headers"])
    assert response.status_code == 200