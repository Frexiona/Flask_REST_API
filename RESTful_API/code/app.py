from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList

app = Flask(__name__)
# Turn off FLask SQL Alchemy track but SQL Alchemy is still on
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rex'
api = Api(app)

@app.before_first_request
def create_table():
    db.create_all()

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
    from db import db

    db.init_app(app)
    app.run(port=5068, debug=True)
