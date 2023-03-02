import json

from uuid import uuid4


async def test_update_user(client, create_user_in_database, get_user_from_database):
	user_data = {
		"user_id": uuid4(),
		"name": "Armin",
		"surname": "Arlert",
		"email": "armin@gmail.com",
		"is_active": True,
		"hashed_password": "somepassword"
	}
	user_data_updated = {
		"name": "Armin-Collosal",
		"surname": "Arlerd",
		"email": "collos@gmail.com",
		"hashed_password": "somepassword"
	}
	await create_user_in_database(**user_data)
	resp = client.patch(
		f"/user/?user_id={user_data['user_id']}", 
		content=json.dumps(user_data_updated)
	)
	assert resp.status_code == 200
	resp_data = resp.json()
	assert resp_data["updated_user_id"] == str(user_data["user_id"])
	users_from_db = await get_user_from_database(user_data["user_id"])
	user_from_db = dict(users_from_db[0])
	assert user_from_db["user_id"] == user_data["user_id"]
	assert user_from_db["name"] == user_data_updated["name"]
	assert user_from_db["surname"] == user_data_updated["surname"]
	assert user_from_db["email"] == user_data_updated["email"]
	assert user_from_db["is_active"] is user_data["is_active"]
