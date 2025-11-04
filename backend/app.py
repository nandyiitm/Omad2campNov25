from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

# jwt auth config
app.config['JWT_SECRET_KEY'] = "some-secret-key"
JWTManager(app)

# connecting to database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
from models import db, User
db.init_app(app)

## connecting to routes
from routes import api
api.init_app(app)

if __name__ == '__main__':
    
    with app.app_context():
        db.create_all()

        admin = User.query.get("admin@gmail.com")
        if not admin:
            admin = User(name='Admin', email='admin@gmail.com', password='admin', role="admin")
            db.session.add(admin); db.session.commit()
            print('Admin created!')

    
    app.run(debug=True)