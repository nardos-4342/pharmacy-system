import sqlite3
from datetime import date

def getstock():
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    cursor.execute("""
        SELECT products.name, products.reorder, SUM(batches.quantity)
        FROM products
        JOIN batches ON batches.productid = products.id
        GROUP BY products.id;
    """)
    return cursor.fetchall() 
x=[("Aspirin", 5, 4), ("Cough syrup", 50, 10)]

for name, reorder, stock in getstock():
    if stock<=reorder:
        print(name, stock, "LOW")
    else:
        print(name, stock, "GOOD")


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
        cursor.execute(
            "INSERT INTO batches (productid, batchnumber, expirationdate, quantity) VALUES (?, ?, ?, ?)",
            (productid, batchnumber, expirationdate, quantity)
        )
        conn.commit()
        return productid
    except Exception:
        raise
    finally:
        conn.close()
def getexpiringproducts():
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    cursor.execute("""
        SELECT products.name, batches.batchnumber, batches.expirationdate
        FROM products
        JOIN batches on batches.id=products.id
        WHERE batches.expirationdate <= ? """, (date.today().isoformat(),))
    products=cursor.fetchall()
    conn.close()
    return products