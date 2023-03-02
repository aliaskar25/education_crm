import json

from uuid import uuid4


async def test_get_user(client, create_user_in_database, get_user_from_database):
	user_data = {
		"user_id": uuid4(),
		"name": "Mikasa",
		"surname": "Ackerman",
		"email": "mikasa@gmail.com",
		"is_active": True,
		"hashed_password": "somepassword"
	}
	await create_user_in_database(**user_data)
	resp = client.get(f"/user/?user_id={user_data['user_id']}")
	assert resp.status_code == 200
	user_from_response = resp.json()
	assert user_from_response["user_id"] == str(user_data["user_id"])
	assert user_from_response["name"] == user_data["name"]
	assert user_from_response["surname"] == user_data["surname"]
	assert user_from_response["email"] == user_data["email"]
	assert user_from_response["is_active"] == user_data["is_active"]

