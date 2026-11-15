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

def addproduct(name, unit, buyingprice, sellingprice, reorder, batchnumber, expirationdate, quantity):
    if quantity <=0:
        raise ValueError("Quantity must be greater than zero.")
    conn=sqlite3.connect("pharmacy.db")
    try:
        cursor=conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, unit, buyingprice, sellingprice, reorder) VALUES (?, ?, ?, ?, ?)",
            (name, unit, buyingprice, sellingprice, reorder)
        )
        productid=cursor.lastrowid
        cursor.exeute(
            "INSERT INTO batches (productid, batchnumber, expirationdate, quantity) VALUES (?, ?, ?, ?)",
            (productid, batchnumber, expirationdate, quantity)
        )
        conn.commit()
        return productid
    except Exception:
        raise
    finally:
        conn.close()
