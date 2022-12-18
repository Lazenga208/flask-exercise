
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users/all")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19

def test_post_new_user(client):
    body = {"name": "Avi", "age":45, "team": "NNB"}
    res = client.post("http://localhost:5000/users", json=body)
    assert res.status_code == 201

    res_user = res.json["result"]["new user"]
    assert res_user["name"] == body["name"]
    body = {"age": 45, "team": "NNB"}
    res = client.post("http://localhost:5000/users", json=body)
    assert res.status_code == 422

def test_put_user_id(client):
    fields = {"age": 50}
    res = client.put("http://localhost:5000/users/2", json=fields)
    assert res.status_code == 200
    res_user = res.json["result"]["update user"]
    assert res_user["age"] == 50

def test_delete_user_id(client):
    res = client.delete("http://localhost:5000/users/2")
    assert res.status_code == 200
    assert res.json["message"] == "The user deleted successfully!"
