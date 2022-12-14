import unittest
import requests

class Test_App(unittest.TestCase):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')


    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_get(self):
        res = requests.get("http://localhost:5000")
        assert res.status_code == 200
        assert res.json()["result"]["content"] == "hello world!"

    def test_mirror(self):
        res = requests.get("http://localhost:5000/mirror/Tim")
        assert res.status_code == 200
        assert res.json()["result"]["name"] == "Tim"

    def test_get_users(self):
        res = requests.get("http://localhost:5000/users/all")
        assert res.status_code == 200

        res_users = res.json()["result"]["users"]
        assert len(res_users) == 4
        assert res_users[0]["name"] == "Aria"

    def tests_get_users_with_team(self):
        res = requests.get("http://localhost:5000/users?team=LWB")
        assert res.status_code == 200

        res_users = res.json()["result"]["users"]
        assert len(res_users) == 2
        assert res_users[1]["name"] == "Tim"

    def test_get_user_id(self):
        res = requests.get("http://localhost:5000/users/1")
        assert res.status_code == 200

        res_user = res.json()["result"]["user"]
        assert res_user["name"] == "Aria"
        assert res_user["age"] == 19

    def test_post_new_user(self):
        body={"name":"Avi","age":45,"team":"NNB"}
        res=requests.post("http://localhost:5000/users",json=body)
        assert res.status_code == 201

        res_user = res.json()["result"]["new user"]
        assert res_user["name"]==body["name"]
        body = { "age": 45, "team": "NNB"}
        res = requests.post("http://localhost:5000/users", json=body)
        assert res.status_code == 422

    def test_put_user_id(self):
        fields={"age":50}
        res = requests.put("http://localhost:5000/users/2",json=fields)
        assert res.status_code==200
        res_user = res.json()["result"]["update user"]
        assert res_user["age"] == 50

    def test_delete_user_id(self):
        res = requests.delete("http://localhost:5000/users/2")
        assert res.status_code == 200
        assert res.json()["message"] == "The user deleted successfully!"

if __name__ == '__main__':
    unittest.main()