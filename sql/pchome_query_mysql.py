import mysql.connector

cnx = mysql.connector.connect(user='root', password='1006', host='127.0.0.1', database='pchome')
cursor = cnx.cursor()

query = ("SELECT * FROM products "
         "WHERE name LIKE '%小米%'")

cursor.execute(query)

# for row in cursor:
#   print(row)

rows = cursor.fetchall()
for row in rows:
  print(row)


print('closing')

cursor.close()
cnx.close()