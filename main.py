import flask
from flask import Flask, abort, request, jsonify
import json, ast
import base64

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cred_file = "cred.txt"
# Creating a file to store user creds run time DB type part
with open(cred_file, 'w'):
    pass

#register new user with POST request
def register_user(data):
    if user_exists(data):
        return {"message":"Registration failed as user exists "}, 400
    print("Registering user")
    add(data)
    return {"message":"Register done "}, 200

#method to add user in file
def add(text):
    try:
        f = open(cred_file, "a")
        f.write(str(text)+ "\n")
        f.close()
        return True
    except Exception as e:
        return False

#login to user method
def login_user(data):
    if user_exists(data):
        return {"message": "login done "}, 200
    return {"message": "login failed for the user"}, 400

#method to check if user exists or not
def user_exists(data):
    file1 = open(cred_file, 'r')
    l = file1.readlines()
    for line in l:
        line = eval(line)
        if line == data:
            return True
    return False

#get method for login
#post method for registering user
@app.route('/api/user', methods=['GET','POST'])
def user():
    try:
        data = ast.literal_eval(json.dumps(request.json))
        data["password"] = base64.b64encode(data["password"])

        if data['first_name'] is None or data['last_name'] is None or data['username'] is None or data['password'] is None:
            abort(400)    # missing arguments

        if request.method =='POST':
            #register the usee
            return register_user(data)

        if request.method =='GET':
            #login the user
            return login_user(data)


    except Exception as e:
        return jsonify({'message': str(e), "status": 500})


if __name__ == '__main__':
    app.run()