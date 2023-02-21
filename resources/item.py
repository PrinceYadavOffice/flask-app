from db import db
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from models import ItemsModel
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt


from schemas import ItemSchema, ItemsUpdateSchema

blp = Blueprint("items",__name__, description="operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemsModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self,item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemsModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted"}
        
    @jwt_required()    
    @blp.arguments(ItemsUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):              
        item = ItemsModel.query.get(item_id)
        if item:
            if item_data.get('name'):
                item.name=item_data["name"]
            elif item_data.get('price'):
                item.price=item_data["price"]
        else:
            item = ItemsModel(id=item_id,**item_data)
        
        db.session.add(item)
        db.session.commit()
        return item


@blp.route("/items/")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        items = ItemsModel.query.all()
        return items

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):        
        item = ItemsModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occured while inserting the data")
        return item
