import json

from uuid import uuid4


async def test_create_user(client, get_user_from_database):
    user_data = {
    	"name": "Aliaskar",
    	"surname": "Isakov",
    	"email": "aliaskar.isakov@gmail.com",
        "password": "somepassword", 
    }
    resp = client.post("/user/", content=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


async def test_create_user_duplicate_email_error(
    client, get_user_from_database
):
    user_data = {
        "name": "Aliaskar",
    	"surname": "Isakov",
    	"email": "aliaskar.isakov@gmail.com",
        "password": "somepassword"
    }
    user_data_same_email = {
        "name": "Ali",
        "surname": "Isakov",
        "email": "aliaskar.isakov@gmail.com",
        "password": "somepassword"
    }
    resp = client.post("/user/", content=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
    resp = client.post("/user/", content=json.dumps(user_data_same_email))
    assert resp.status_code == 400
    assert "User with this email already exists." in resp.json()["detail"]
