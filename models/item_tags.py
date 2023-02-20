from db import db 

class ItemTags(db.Model):
    __tablename__="items_tags"

    id = db.Column(db.Integer, primary_key = True)
    item_id = db.Column(db.Integer, db.Foreignkey("items.id"))
    tag_id = db.Column(db.Integer, db.Foreignkey("tags.id"))

