import sqlite3

conn=sqlite3.connect("pharmacy.db")
conn.executescript("""
DROP TABLE IF EXISTS solditems;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS batches;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
    
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    unit TEXT,
    buyingprice REAL,
    sellingprice REAL,
    reorder INTEGER
);
    
CREATE TABLE batches(
    id INTEGER PRIMARY KEY,
    productid INTEGER NOT NULL,
    batchnumber TEXT,
    expirationdate TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (productid) REFERENCES products(id)
);
    
CREATE TABLE sales(
    id INTEGER PRIMARY KEY,
    userid INTEGER NOT NULL,
    saledate TEXT NOT NULL,
    total REAL NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(id)
);
    
CREATE TABLE solditems(
    id INTEGER PRIMARY KEY,
    saleid INTEGER NOT NULL,
    batchid INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unitprice REAL NOT NULL,
    FOREIGN KEY (saleid) REFERENCES sales(id),
    FOREIGN KEY (batchid) REFERENCES batches(id)
);
    
INSERT INTO products (name, unit, buyingprice, sellingprice, reorder)
VALUES ('Paracetamol', 'box', 10, 12.5, 20),
       ('Amoxicillin', 'strip', 22, 30, 10);

INSERT INTO batches (productid, batchnumber, expirationdate, quantity)
VALUES (1, 'B001', '2027-03-15', 100),
       (1, 'B002', '2027-08-20', 200),
       (2, 'B003', '2027-01-10', 50);
""")
conn.commit()
rows=conn.execute("""
    SELECT products.name, SUM(batches.quantity)
    FROM products
    JOIN batches ON batches.productid = products.id
    GROUP BY products.id;
""")
for row in rows:
    print(row)

conn.close()
