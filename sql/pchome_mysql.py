import requests
import mysql.connector
from mysql.connector import errorcode

try:
  cnx = mysql.connector.connect(user='root', password='****', host='127.0.0.1')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  print('successfully connected to MySQL srver')


cursor = cnx.cursor()
DB_NAME = 'pchome'
def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

TABLES = {}
TABLES['products'] = (
    "CREATE TABLE `products` ("
    "  `id` int NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(100) NOT NULL,"
    "  `price` int NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")


add_products = ("INSERT INTO products "
               "(name, price) "
               "VALUES (%s, %s)")


for i in range(100):
    r = requests.get(f'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q=%E9%9B%BB%E8%85%A6%E8%9E%A2%E5%B9%95&page={i+1}&sort=sale/dc')
    if r.status_code == requests.codes.ok:
        data = r.json()
        for prod in data['prods']:
            name = prod['name']
            price = prod['price']
            data_products = (name, price)
            cursor.execute(add_products, data_products) # 執行SQL指令

cnx.commit() # 提交, 才能完成以上動作

# cursor.close()
# cnx.close()