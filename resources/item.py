import uuid
from db import items
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request

blp = Blueprint("items",__name__, description="operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id] ,200
        except:
            abort(404, message="Store not found")
    
    def delete(self,item_id):
        try:
            del items[item_id]
            return {"message":"Item deleted"}
        except:
            abort(404, message="Item not found")

    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(
                400,
                message = "Bad request. Ensure 'price' and 'name' is included in JSON payload."
            )
        try:
            item = items[item_id]

            item |=item_data
            return item
        except:
            abort(404, message="Item not found")


@blp.route("/items/")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()

        if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
            abort(
                400,
                message="Bad request, Ensure 'price' 'store_id' and 'name' in the JSON Payload."
            )
        
        for item in items.values():
            if item_data['name'] == item['name'] and item_data['store_id'] == item['store_id']:
                abort(
                    400,
                    message = "Item already exits"
                )
        item_id = uuid.uuid4().hex
        item = {**item_data, "id":item_id}
        items[item_id]=item
        return item
