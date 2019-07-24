import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")
    parser.add_argument('store_id', type=int, required=True, help="Every item needs a store id")

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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

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
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name "{name}" already exists.'}, 400  # 400 Bad Request (User Side)

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500  # Internal Server Error (Server Side)

        return item.json(), 201

    def delete(self, name):
        '''
        global items
        """
        items here is local variable, which is not what we want
        """
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item delete'}
        '''

        '''
        item = ItemModel.find_by_name(name)
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
        '''

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        if item is None:
            '''
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
            '''
            item = ItemModel(name, **data)
        else:
            '''
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred updating the item.'}, 500
            '''
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        '''
        OLD VERSION
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[1], 'price': row[2]})

        connection.close()

        return {'items': items}
        '''
        # return {'items': [item.json() for item in ItemModel.query.all()]}
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
