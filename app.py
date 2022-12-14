from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""

@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})

@app.route("/users/all")
def allUsers():
    return create_response({"users": db.get('users')})

@app.route('/users/<id>')
def userById(id):
    ans=db.getById("users",int(id))
    if ans is None:
        return create_response(status=404,message="There is no user with such an id")
    return create_response({"user":ans})

@app.route("/users")
def byTeam():
    team=request.args.get('team')
    users=[i for i in db.get("users") if i["team"] == team]
    if users == []:
        return create_response(status=404,message="There is no users in this team!")
    return create_response({"users":users})

@app.route("/users",methods=['POST'])
def newUser():
    body=request.json
    for i in db.userBase:
        if i not in body:
            return create_response(status=422,message="The field "+i+" is required!!")
    ans=db.create("users",body)
    return create_response({"new user":ans},status=201,message=ans["name"]+ " added!")

@app.route("/users/<id>",methods=['PUT'])
def update(id):
    fields=request.json
    ans=db.updateById("users",int(id),fields)
    if ans is None:
        return create_response(status=404,message="The id "+id+" is not defined!")
    return create_response({"update user": ans})

@app.route("/users/<id>",methods=['DELETE'])
def delete(id):
    if db.getById("users",int(id)) is None:
        return create_response(status=404,message="The id "+id+" is not defined!")
    db.deleteById("users",int(id))
    return create_response(message="The user deleted successfully!")

@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(debug=True)
