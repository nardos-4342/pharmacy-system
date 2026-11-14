import sqlite3

def getstock():
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    cursor.execute("""
        SELECT products.name, SUM(batches.quantity)
        FROM products
        JOIN batches ON batches.productid = products.id
        GROUP BY products.id;
    """)
    return cursor.fetchall() 

for row in getstock():
    print(row)