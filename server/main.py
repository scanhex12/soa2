from flask import Flask, request, make_response
import json
import requests
import sqlite3
from flask import Flask, request, make_response
import json

def update_data(login, data):
    data['login'] = login
    response = requests.post('http://database:8091/data/add', data=json.dumps(data))
    return response.status_code


app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    body = json.loads(request.data)
    login = body['login']
    password = body['password']
    metadata = {
        'firstName': body.get('firstName'),
        'lastName': body.get('lastName'),
        'birthDate': body.get('birthDate'),
        'mail': body.get('mail'),
        'phoneNumber': body.get('phoneNumber')
    }
        
    response = requests.get('http://database:8091/auth', data=json.dumps({'login': login}))
    if response.status_code == 200:
        return make_response('User already exists\n', 403)

    requests.post('http://database:8091/auth', data=json.dumps({'login': login, 'password': password}))
        
    update_data(login, metadata)

    return make_response('Successful registration\n', 200)

@app.route('/login', methods=['POST'])
def login():
    body = json.loads(request.data)
    login = body['login']
    password = body['password']

    response = requests.get('http://database:8091/auth', data=json.dumps({'login': login}))
    
    if response.status_code == 403:
        return make_response('User does not exist\n', 401)
    
    stored_password = response.text.strip()
    
    if stored_password != password:
        return make_response('Incorrect password\n', 403)

    response_metadata = requests.get('http://database:8091/data', data=json.dumps({'login': login}))
    
    if response_metadata.status_code != 200:
        return make_response('Error retrieving user data\n', 500)
    
    metadata = response_metadata.json()
    return make_response(json.dumps(metadata), 200, {'Content-Type': 'application/json'})

@app.route('/update', methods=['POST'])
def update():
    body = json.loads(request.data)
    login = body['login']
    password = body['password']
        
    response = requests.get('http://database:8091/auth', data=json.dumps({'login': login}))
    stored_password = response.text
        
    if stored_password != password:
        return make_response('Incorrect password\n', 403)
        
    metadata = {
        'firstName': body.get('firstName'),
        'lastName': body.get('lastName'),
        'birthDate': body.get('birthDate'),
        'mail': body.get('mail'),
        'phoneNumber': body.get('phoneNumber')
    }
        
    response = update_data(login, metadata)
        
    return make_response(f'Successfully updated user data\n{response}\n', 200)

def main():
    app.run(host='0.0.0.0', port=8090, debug=True)

if __name__ == "__main__":
    main()
