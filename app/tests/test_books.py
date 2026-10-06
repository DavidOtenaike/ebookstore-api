from decimal import Decimal
def test_create_book_requires_admin(client, registered_user, sample_author):
    response = client.post(
        "/books",
        json={
            "title": "Dune",
            "description": "Sci-fi epic",
            "price": "19.99",
            "stock_quantity": 5,
            "author_id": sample_author
        },
        headers=registered_user["headers"]
    )
    assert response.status_code == 403


def test_admin_can_create_book(client, admin_user, sample_author):
    response = client.post(
        "/books",
        json={
            "title": "Dune",
            "description": "Sci-fi epic",
            "price": "19.99",
            "stock_quantity": 5,
            "author_id": sample_author
        },
        headers=admin_user["headers"]
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Dune"
    assert data["author"]["name"] == "Frank Herbert"


def test_create_duplicate_title_fails(client, admin_user, sample_author):
    payload = {
        "title": "Dune",
        "description": "Sci-fi epic",
        "price": "19.99",
        "stock_quantity": 5,
        "author_id": sample_author
    }
    client.post("/books", json=payload, headers=admin_user["headers"])
    response = client.post("/books", json=payload, headers=admin_user["headers"])
    assert response.status_code == 409  


def test_get_book_not_found(client):
    response = client.get("/books/9999")
    assert response.status_code == 404


def test_get_book_by_id(client, sample_book):
    response = client.get(f"/books/{sample_book['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Dune"


def test_list_books_pagination_shape(client, sample_book):
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert data["total"] >= 1


def test_list_books_filters_by_author(client, sample_book):
    response = client.get("/books?author=Herbert")
    data = response.json()
    assert data["total"] == 1

    response = client.get("/books?author=NoSuchAuthor")
    data = response.json()
    assert data["total"] == 0


def test_update_book_requires_admin(client, registered_user, sample_book):
    response = client.patch(
        f"/books/{sample_book['id']}", json={"price": "9.99"}, headers=registered_user["headers"]
    )
    assert response.status_code == 403


def test_admin_can_update_book(client, admin_user, sample_book):
    response = client.patch(
        f"/books/{sample_book['id']}", json={"price": "9.99"}, headers=admin_user["headers"]
    )
    assert response.status_code == 200
    assert Decimal(response.json()["price"]) == Decimal("9.99")


def test_update_book_partial_leaves_other_fields_unchanged(client, admin_user, sample_book):
    response = client.patch(
        f"/books/{sample_book['id']}", json={"stock_quantity": 100}, headers=admin_user["headers"]
    )
    data = response.json()
    assert data["stock_quantity"] == 100
    assert data["title"] == "Dune"


def test_delete_book_requires_admin(client, registered_user, sample_book):
    response = client.delete(f"/books/{sample_book['id']}", headers=registered_user["headers"])
    assert response.status_code == 403


def test_admin_can_delete_book(client, admin_user, sample_book):
    response = client.delete(f"/books/{sample_book['id']}", headers=admin_user["headers"])
    assert response.status_code == 200

    get_response = client.get(f"/books/{sample_book['id']}")
    assert get_response.status_code == 404