#nosql models for nosql_products, categories

from mongoengine import Document, StringField, FloatField, IntField, ReferenceField, ListField, BooleanField

class Category(Document):
    name = StringField(required=True, unique=True)
    description = StringField()

    meta = {'collection':'categories'}

class Product(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    stock = IntField(default=0)
    category = ReferenceField(Category)
    images = ListField(StringField())
    tags = ListField(StringField())
    available = BooleanField(default=True)

    meta = {'collection':'products'}