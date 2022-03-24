import pymongo
from pymongo import MongoClient
import pprint


client = MongoClient('localhost', 27017)
db = client.pchome
print(db.list_collection_names())
products = db.products
print(products.count_documents({}))
print(products.find_one({'price':3999}))
data = products.find()

# regex operator
name_condition = {'name':{'$regex':'.*ASUS.*'}}
# data = products.find(name_condition)

# comparison operator
price_condition = {'price':{'$gt':8000}}
data = products.find(price_condition)


for d in products.find({'$and':[name_condition, price_condition]}):
    print(d['name'], d['price'])


products.update_one({'name':'Bella'}, {'$set':{'price':1000000}}, upsert=True)
print(products.find_one({'name':'Bella'}))
products.delete_one({'name':'Bella'})