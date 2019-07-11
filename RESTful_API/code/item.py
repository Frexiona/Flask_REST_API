import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    # only paramter price will pass

    @jwt_required()
    def get(self, name):
        '''
        # next gets the first item found by the filter function
        # None: if next function does not find ant item, it will return None
        item = next(filter(lambda x: x['name'] == name, items), None)
        # for item in items:
        # 	if item['name'] == name:
        # 		return item
        return {'item': item}, 200 if item else 404  # 404 for Not Found
        '''
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


    def post(self, name):
        '''
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'An item with name "{name}" already exists.'}, 400  # 400 for bad request
        # force = True ## don't look at the header
        # silent = True ## it doesn't give error, just null
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        # 201 for Created
        return item, 201
        '''
        if self.find_by_name(name):
            return {'message': f'An item with name "{name}" already exists.'}, 400  # 400 Bad Request (User Side)

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 # Internal Server Error (Server Side)

        return item, 201

    def delete(self, name):
        '''
        global items
        """
        items here is local variable, which is not what we want
        """
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item delete'}
        '''

        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'item delete'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            item = {'name': name, 'price': data['price']}
            try:
                self.insert(updated_item)
            except Exception as e:
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            try:
                self.update(data)
            except Exception as e:
                return {'message': 'An error occurred updating the item.'}, 500
        return updated_item

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}