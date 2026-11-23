import sqlite3
from datetime import date, datetime, timedelta

def getstock():
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    today = date.today().isoformat()
    cursor.execute("""
        SELECT products.name, products.reorder, COALESCE(SUM(batches.quantity), 0)
        FROM products
        LEFT JOIN batches ON batches.productid = products.id AND batches.expirationdate>=?
        GROUP BY products.id;
    """, (today,))
    rows=cursor.fetchall()
    conn.close()
    return rows

def addproduct(name, unit, buyingprice, sellingprice, reorder,familyid, batchnumber, expirationdate, quantity):
    if quantity <=0:
        raise ValueError("Quantity must be greater than zero.")
    conn=sqlite3.connect("pharmacy.db")
    try:
        cursor=conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, unit, buyingprice, sellingprice, reorder) VALUES (?, ?, ?, ?, ?)",
            (name, unit, buyingprice, sellingprice, reorder, familyid)
        )
        productid=cursor.lastrowid
        cursor.execute(
            "INSERT INTO batches (productid, batchnumber, expirationdate, quantity) VALUES (?, ?, ?, ?)",
            (productid, batchnumber, expirationdate, quantity)
        )
        conn.commit()
        return productid
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
def getsolditems(days):
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    cursor.execute("""
        SELECT products.name, solditems.quantity, solditems.unitprice, sales.saledate
        FROM solditems
        JOIN batches ON solditems.batchid = batches.id
        JOIN products ON batches.productid = products.id
        JOIN sales ON solditems.saleid = sales.id
        WHERE sales.saledate >= ?
        ORDER BY sales.saledate DESC """, (cutoff,))
    items=cursor.fetchall()
    conn.close()
    return items

def getfamilies():
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    today=date.today().isoformat()
    cursor.execute("""
        SELECT medicinefamilies.id, medicinefamilies.name, COALESCE(SUM(batches.quantity), 0)
        FROM medicinefamilies
        LEFT JOIN products ON products.familyid=medicinefamilies.id
        LEFT JOIN batches ON batches.productid=products.id AND batches.expirationdate>=?
        GROUP BY medicinefamilies.id; """, (today, ))
    rows=cursor.fetchall()
    conn.close()
    return rows

def getfamilymedicines(familyid):
    conn=sqlite3.connect("pharmacy.db")
    cursor=conn.cursor()
    today=date.today().isoformat()
    cursor.execute("""
        SELECT products.id, products.name, COALESCE(SUM(batches.quantity), 0)
        FROM products
        LEFT JOIN batches ON batches.productid=products.id AND batches.expirationdate>=?
        WHERE products.familyid=?
        GROUP BY products.id; """, (today, familyid))
    rows=cursor.fetchall()
    conn.close()
    return rows
if __name__ == "__main__":
    for name, reorder, stock in getstock():
        if stock <= reorder:
            print(name, stock, "LOW")
        else:
            print(name, stock, "GOOD")

def addstock(productid, batchnumber, expirationdate, quantity):
    if quantity<=0:
        raise ValueError("Quantity must be greater than zero.")
    try:
        parsed=datetime.strptime(expirationdate, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Expiration date must be in YYYY-MM-DD format.")
    expirationdate=parsed.isoformat()
    if expirationdate < date.today().isoformat():
        raise ValueError("Expiration date cannot be in the past.")
    conn=sqlite3.connect("pharmacy.db")
    try:
        cursor=conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id=?", (productid, ))
        if cursor.fetchone() is None:
            raise ValueError("No such product.")
        cursor.execute("SELECT id FROM batches WHERE productid=? AND batchnumber=?",
                       (productid, batchnumber))
        if cursor.fetchone is not None:
            raise ValueError("The batch number already exists.")
        cursor.execute("INSERT INTO batches(productid, batchnumber, expirationdate, quantity) "
                       "VALUES(?, ?, ?, ?)", (productid, batchnumber, expirationdate, quantity))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
def sell(batchid, quantity, userid):
    if quantity<=0:
            raise ValueError("Quantity should be above 0.")
    conn=sqlite3.connect("pharmacy.db")
    try:
        cursor=conn.cursor()
        cursor.execute("""
            SELECT batches.expirationdate, batches.quantity, products.sellingprice
            FROM batches
            JOIN products ON products.id=batches.productid 
            WHERE batches.id=?""", (batchid, ))
        row=cursor.fetchone()
        if row is None:
            raise ValueError("No such batch.")
        expirationdate, available, sellingprice=row
        if expirationdate < date.today().isoformat():
            raise ValueError("The batch has expired.")
        if quantity>available:
            raise ValueError("The requested quantity is above the availiable amount.")
        total=quantity*sellingprice
        saledate =datetime.now().isoformat(sep=" ", timespec="seconds")    
        
        cursor.execute("INSERT INTO sales(userid, saledate, total)"
                       "VALUES (?, ?, ?)", (userid, saledate, total))
        saleid=cursor.lastrowid
        cursor.execute("INSERT INTO solditems(saleid, batchid, quantity, sellingprice) " 
                       "Values (?, ?, ?,?)", (saleid, batchid, quantity, sellingprice))
        cursor.execute(
            "UPDATE batches SET quantity = quantity - ? WHERE id = ? AND quantity >= ?",
            (quantity, batchid, quantity)
        )
        if cursor.rowcount == 0:
            raise ValueError("Not enough stock in this batch.")
        
        conn.commit()
        return saleid
    finally:
        conn.close()
        