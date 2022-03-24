import requests
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
for i in range(87):
    r = requests.get(f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E9%9B%BB%E8%85%A6%E8%9E%A2%E5%B9%95&page={i+1}&sort=sale/dc')
    if r.status_code == requests.codes.ok:
        data = r.json()
        for prod in data['prods']:
            name = prod['name']
            price = prod['price']
            data_products = {'name':name, 'price':int(price)}
            client.pchome.products.insert_one(data_products)




