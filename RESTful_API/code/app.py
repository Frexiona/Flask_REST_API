from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'rex'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # JWT will create a new end-point which is called /auth

api.add_resource(UserRegister, '/register')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')


'''
class Student(Resource):
    def get(self, name):
        return {'student': name}


api.add_resource(Student, '/student/<string:name>')
'''

if __name__ == '__main__':
    app.run(port=5068, debug=True)