from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'rex'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # JWT will create a new end-point which is called /auth

items = list()


class Student(Resource):
    def get(self, name):
        return {'student': name}


api.add_resource(Student, '/student/<string:name>')


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    # only paramter price will pass

    @jwt_required()
    def get(self, name):
        # next gets the first item found by the filter function
        # None: if next function does not find ant item, it will return None
        item = next(filter(lambda x: x['name'] == name, items), None)
        # for item in items:
        # 	if item['name'] == name:
        # 		return item
        return {'item': item}, 200 if item else 404  # 404 for Not Found

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'An item with name "{name}" already exists.'}, 400  # 400 for bad request
        # force = True ## don't look at the header
        # silent = True ## it doesn't give error, just null
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        # 201 for Created
        return item, 201

    def delete(self, name):
        global items
        """
        items here is local variable, which is not what we want
        """
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item delete'}

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else: 
            item.update(data)
        return item


api.add_resource(Item, '/item/<string:name>')


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(ItemList, '/items')

app.run(port=5068, debug=True)
