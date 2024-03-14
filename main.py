from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://robertj:<YOUR_PASSWORD>@localhost:5432/users_db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, username, password, first_name, last_name, date_of_birth, email, phone_number):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.email = email
        self.phone_number = phone_number

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    new_user = User(**data)
    print(data)
    try:
        db.session.add(new_user)
        #print("OK")
        db.session.commit()
        #print("OK 2")
        return jsonify({'message': 'OK'}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'error'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        return jsonify({'message': 'OK'}), 200
    else:
        return jsonify({'error': 'error'}), 401

@app.route('/update', methods=['PUT'])
def update_user():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        db.session.commit()
        return jsonify({'message': 'OK'}), 200
    else:
        return jsonify({'error': 'error'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8012)
