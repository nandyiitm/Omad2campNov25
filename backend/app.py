from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

## this is what we were doing in mad1
# @app.route('/')
# def index():
#     return rendered_template('index.html')

## this is how we do it in mad2
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, world! from flask restful'}
api.add_resource(HelloWorld, '/message')

if __name__ == '__main__':
    app.run(debug=True)