# ---------------------
# IMPORTS
# ---------------------
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

app = Flask(__name__)

# Configuring database (using SQLite for simplicity, can switch to PostgreSQL or another in production)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carboni.db'
app.config[
    'JWT_SECRET_KEY'] = 'your_jwt_secret'  # Change this to a more secure secret
db = SQLAlchemy(app)
jwt = JWTManager(app)


# ---------------------
# MODELS
# ---------------------
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(
      db.String(120),
      nullable=False)  # Hash passwords in a real-world application
  role = db.Column(db.String(80), nullable=False)


# ---------------------
# ENDPOINTS
# ---------------------
@app.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  user = User.query.filter_by(username=data['username']).first()
  if user and user.password == data['password']:
    access_token = create_access_token(identity={
        'username': user.username,
        'role': user.role
    })
    return jsonify(access_token=access_token), 200
  return jsonify({"message": "Invalid credentials"}), 401


@app.route('/plastic_update', methods=['POST'])
@jwt_required()
def plastic_update():
  identity = get_jwt_identity()
  role = identity['role']

  # Using roles to decide on actions
  if role == 'fisherman':
    # Code to handle fisherman's updates
    pass
  elif role == 'trucker':
    # Code to handle trucker's updates
    pass
  elif role == 'warehouse':
    # Code to handle warehouse's updates
    pass
  # ... add other roles accordingly

  return jsonify({"message": "Update added successfully!"}), 200


# ---------------------
# RUNNING THE APP
# ---------------------
if __name__ == '__main__':
  app.run(debug=True)
  db.create_all()  # Creates the SQLite database

  # you need to start the app first