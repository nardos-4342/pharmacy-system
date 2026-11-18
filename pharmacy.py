import sqlite3
from datetime import date, timedelta

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
def getexpiredproducts():
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    today = date.today().isoformat()
    cursor.execute("""
        SELECT products.name, batches.batchnumber, batches.quantity, batches.expirationdate
        FROM products
        JOIN batches on batches.productid=products.id
        WHERE batches.expirationdate <? AND batches.quantity>0
        ORDER BY batches.expirationdate ASC """,(today,) )
    products=cursor.fetchall()
    conn.close()
    return products

def getexpiringproducts(days):
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    today = date.today().isoformat()
    cutoff = (date.today() + timedelta(days=days)).isoformat()
    cursor.execute("""
        SELECT products.name, batches.batchnumber, batches.quantity, batches.expirationdate
        FROM products
        JOIN batches on batches.productid=products.id
        WHERE batches.expirationdate >= ? AND batches.expirationdate <= ? AND batches.quantity>0
        ORDER BY batches.expirationdate """, (today, cutoff))
    products=cursor.fetchall()
    conn.close()
    return products

