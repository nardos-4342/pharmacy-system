import sqlite3

conn=sqlite3.connect("pharmacy.db")
conn.executescript("""
DROP TABLE IF EXISTS solditems;
DROP TABLE IF EXISTS sales;
DROP TABLE IF EXISTS batches;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS medicinefamilies;
DROP TABLE IF EXISTS history;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);
CREATE TABLE medicinefamilies (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
    
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    unit TEXT,
    buyingprice REAL NOT NULL,
    sellingprice REAL NOT NULL,
    familyid INTEGER NOT NULL,
    reorder INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (familyid) REFERENCES medicinefamilies(id)
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
CREATE TABLE history (
    id INTEGER PRIMARY KEY,
    userid INTEGER NOT NULL,
    action TEXT NOT NULL,
    details TEXT,
    createdat TEXT NOT NULL,
    FOREIGN KEY (userid) REFERENCES users(id)
);
INSERT INTO users (username, password, role)
VALUES ('owner', 'temp123', 'owner'),
       ('pharmacist', 'temp123', 'pharmacist'),
       ('cashier', 'temp123', 'cashier');

INSERT INTO medicinefamilies (name)
VALUES ('Antibiotics'),
       ('Hygiene and cosmetics'),
       ('Urinary'),
       ('Other');

INSERT INTO products (name, unit, buyingprice, sellingprice, reorder, familyid)
VALUES ('Paracetamol 500mg tablet', 'box', 10, 12.5, 20, 4),
       ('Amoxicillin 500mg capsule', 'strip', 22, 30, 10, 1),
       ('Ciprofloxacin 500mg tablet', 'strip', 35, 50, 8, 1),
       ('Hand sanitizer 100ml', 'bottle', 25, 40, 5, 2),
       ('Nitrofurantoin 100mg capsule', 'strip', 28, 45, 6, 3),
       ('Ibuprofen 200mg tablet', 'box', 8, 11, 15, 4);

INSERT INTO batches (productid, batchnumber, expirationdate, quantity)
VALUES (1, 'B001', '2027-03-15', 10),
       (1, 'B002', '2027-08-20', 30),
       (2, 'B003', '2026-01-10', 5),
       (2, 'B004', '2026-12-10', 8),
       (3, 'B005', '2027-05-01', 40),
       (4, 'B006', '2027-01-31', 3),
       (5, 'B007', '2026-10-01', 12),
       (6, 'B008', '2027-06-30', 0),
       (6, 'B009', '2027-09-30', 25);
""")
conn.commit()
conn.close()
