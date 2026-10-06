def test_register_new_user(client):
    response = client.post("/register", json={"email": "alice@example.com", "password": "secret123"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["role"] == "member"
    assert "hashed_password" not in data


def test_register_duplicate_email_fails(client):
    client.post("/register", json={"email": "bob@example.com", "password": "secret123"})
    response = client.post("/register", json={"email": "bob@example.com", "password": "different"})
    assert response.status_code == 409  

def test_login_success(client):
    client.post("/register", json={"email": "carol@example.com", "password": "secret123"})
    response = client.post("/login", json={"email": "carol@example.com", "password": "secret123"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password_fails(client):
    client.post("/register", json={"email": "dave@example.com", "password": "secret123"})
    response = client.post("/login", json={"email": "dave@example.com", "password": "wrongpassword"})
    assert response.status_code == 401


def test_login_nonexistent_email_fails(client):
    response = client.post("/login", json={"email": "ghost@example.com", "password": "whatever"})
    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get("/me")
    assert response.status_code == 401


def test_me_returns_current_user(client, registered_user):
    response = client.get("/me", headers=registered_user["headers"])
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_change_role_requires_admin(client, registered_user):
    response = client.patch(
        "/users/1/role", json={"role": "admin"}, headers=registered_user["headers"]
    )
    assert response.status_code == 403


def test_admin_can_change_role(client, admin_user, registered_user):

    me_response = client.get("/me", headers=registered_user["headers"])
    user_id = me_response.json()["id"]

    response = client.patch(
        f"/users/{user_id}/role?role=admin", headers=admin_user["headers"]
    )
    assert response.status_code == 200


def test_change_role_rejects_invalid_role(client, admin_user, registered_user):
    me_response = client.get("/me", headers=registered_user["headers"])
    user_id = me_response.json()["id"]

    response = client.patch(
        f"/users/{user_id}/role?role=superuser", headers=admin_user["headers"]
    )
    assert response.status_code == 400