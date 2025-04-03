import mysql.connector

# Connect to MySQL database using the provided credentials
conn = mysql.connector.connect(
    host="localhost:3306",
    user="cdac",
    password="cdac",
    database="sales_db"
)
cursor = conn.cursor()

# Drop tables if they exist to start fresh (optional, for debugging)
cursor.execute("DROP TABLE IF EXISTS SALES_ORDER_DETAILS")
cursor.execute("DROP TABLE IF EXISTS SALES_ORDER")
cursor.execute("DROP TABLE IF EXISTS SALESMAN_MASTER")
cursor.execute("DROP TABLE IF EXISTS PRODUCT_MASTER")
cursor.execute("DROP TABLE IF EXISTS CLIENT_MASTER")

# Step 1: Create the tables (from Question 1, adjusted for MySQL)
cursor.execute('''
CREATE TABLE CLIENT_MASTER (
    CLIENTNO VARCHAR(6) PRIMARY KEY CHECK (CLIENTNO LIKE 'C%'),
    NAME VARCHAR(20) NOT NULL,
    CITY VARCHAR(15),
    PINCODE INTEGER,
    STATE VARCHAR(15),
    BALDUE DECIMAL(10,2)
);
''')

cursor.execute('''
CREATE TABLE PRODUCT_MASTER (
    PRODUCTNO VARCHAR(6) PRIMARY KEY CHECK (PRODUCTNO LIKE 'P%'),
    DESCRIPTION VARCHAR(15) NOT NULL,
    PROFITPERCENT DECIMAL(4,2) NOT NULL,
    UNITMEASURE VARCHAR(10) NOT NULL,
    QTYONHAND INTEGER NOT NULL,
    REORDERLVL INTEGER NOT NULL CHECK (REORDERLVL != 0),
    SELLPRICE DECIMAL(8,2) NOT NULL CHECK (SELLPRICE != 0),
    COSTPRICE DECIMAL(8,2) NOT NULL CHECK (COSTPRICE != 0)
);
''')

cursor.execute('''
CREATE TABLE SALESMAN_MASTER (
    SALESMANNO VARCHAR(6) PRIMARY KEY CHECK (SALESMANNO LIKE 'S%'),
    SALESMANNAME VARCHAR(20) NOT NULL,
    ADDRESS1 VARCHAR(30) NOT NULL,
    ADDRESS2 VARCHAR(30),
    CITY VARCHAR(20),
    PINCODE INTEGER,
    STATE VARCHAR(20),
    SALAMT DECIMAL(8,2) NOT NULL CHECK (SALAMT != 0),
    TGTTOGET DECIMAL(6,2) NOT NULL CHECK (TGTTOGET != 0),
    YTDSALES DECIMAL(6,2) NOT NULL,
    REMARKS VARCHAR(60)
);
''')

cursor.execute('''
CREATE TABLE SALES_ORDER (
    ORDERNO VARCHAR(6) PRIMARY KEY CHECK (ORDERNO LIKE 'O%'),
    CLIENTNO VARCHAR(6),
    ORDERDATE DATE NOT NULL,
    DELYADDR VARCHAR(25),
    SALESMANNO VARCHAR(6),
    DELYTYPE CHAR(1),
    BILLYN CHAR(1),
    DELYDATE DATE,
    ORDERSTATUS VARCHAR(16),
    FOREIGN KEY (CLIENTNO) REFERENCES CLIENT_MASTER(CLIENTNO),
    FOREIGN KEY (SALESMANNO) REFERENCES SALESMAN_MASTER(SALESMANNO)
);
''')

cursor.execute('''
CREATE TABLE SALES_ORDER_DETAILS (
    ORDERNO VARCHAR(6),
    PRODUCTNO VARCHAR(6),
    QTYORDERED INTEGER,
    QTYDISP INTEGER,
    PRODUCTRATE DECIMAL(10,2),
    FOREIGN KEY (ORDERNO) REFERENCES SALES_ORDER(ORDERNO),
    FOREIGN KEY (PRODUCTNO) REFERENCES PRODUCT_MASTER(PRODUCTNO)
);
''')

# Step 2: Insert the data (from Question 2, with corrections)
# CLIENT_MASTER (added C00002 to resolve foreign key issue for SALES_ORDER)
cursor.execute('''
INSERT INTO CLIENT_MASTER (CLIENTNO, NAME, CITY, PINCODE, STATE, BALDUE) VALUES
('C00001', 'Ivan Bayross', 'Mumbai', 400054, 'Maharashtra', 15000),
('C00002', 'John Doe', 'Delhi', 110001, 'Delhi', 1000),
('C00003', 'Chhaya Bankar', 'Mumbai', 400057, 'Maharashtra', 5000),
('C00004', 'Ashwini Joshi', 'Bangalore', 560001, 'Karnataka', 0),
('C00005', 'Hansel Colaco', 'Mumbai', 400060, 'Maharashtra', 2000),
('C00006', 'Deepak Sharma', 'Mangalore', 560050, 'Karnataka', 0);
''')

# PRODUCT_MASTER
cursor.execute('''
INSERT INTO PRODUCT_MASTER (PRODUCTNO, DESCRIPTION, PROFITPERCENT, UNITMEASURE, QTYONHAND, REORDERLVL, SELLPRICE, COSTPRICE) VALUES
('P00001', 'T-Shirts', 5, 'Piece', 200, 50, 350, 250),
('P0345', 'Shirts', 6, 'Piece', 150, 50, 500, 350),
('P06734', 'Cotton Jeans', 5, 'Piece', 100, 20, 600, 450),
('P07865', 'Jeans', 5, 'Piece', 100, 20, 750, 500),
('P07868', 'Trousers', 2, 'Piece', 150, 50, 850, 550),
('P07885', 'Pull Overs', 2.5, 'Piece', 80, 30, 700, 450),
('P07965', 'Denim Shirts', 4, 'Piece', 100, 40, 350, 250),
('P07975', 'Lycra Tops', 5, 'Piece', 70, 30, 300, 175),
('P08865', 'Skirts', 5, 'Piece', 75, 30, 450, 300);
''')

# SALESMAN_MASTER
cursor.execute('''
INSERT INTO SALESMAN_MASTER (SALESMANNO, SALESMANNAME, ADDRESS1, ADDRESS2, CITY, PINCODE, STATE, SALAMT, TGTTOGET, YTDSALES, REMARKS) VALUES
('S00001', 'Aman', 'A/14', 'Worli', 'Mumbai', 400002, 'Maharashtra', 3000, 100, 50, 'Good'),
('S00002', 'Omkar', '65', 'Nariman', 'Mumbai', 400001, 'Maharashtra', 3000, 200, 100, 'Good'),
('S00003', 'Raj', 'P-7', 'Bandra', 'Mumbai', 400032, 'Maharashtra', 3000, 200, 100, 'Good'),
('S00004', 'Ashish', 'A/5', 'Juhu', 'Bombay', 400044, 'Maharashtra', 3500, 200, 150, 'Good');
''')

# SALES_ORDER (added O19002 to match earlier data attempts)
cursor.execute('''
INSERT INTO SALES_ORDER (ORDERNO, CLIENTNO, ORDERDATE, DELYADDR, SALESMANNO, DELYTYPE, BILLYN, DELYDATE, ORDERSTATUS) VALUES
('O19003', 'C00001', '2002-04-03', 'Delhi', 'S00001', 'F', 'Y', '2002-04-04', 'Fulfilled'),
('O46866', 'C00003', '2002-05-24', 'Delhi', 'S00002', 'P', 'N', '2002-05-22', 'Cancelled'),
('O19008', 'C00005', '2002-05-24', 'Delhi', 'S00004', 'F', 'N', '2002-07-26', 'In Process'),
('O19001', 'C00001', '2002-06-12', 'Delhi', 'S00001', 'F', 'N', '2002-07-20', 'In Process'),
('O19002', 'C00002', '2002-06-25', 'Delhi', 'S00002', 'P', 'N', '2002-07-27', 'Cancelled');
''')

# SALES_ORDER_DETAILS (removed rows with O46865 since it doesn't exist in SALES_ORDER)
cursor.execute('''
INSERT INTO SALES_ORDER_DETAILS (ORDERNO, PRODUCTNO, QTYORDERED, QTYDISP, PRODUCTRATE) VALUES
('O19001', 'P00001', 4, 4, 525),
('O19001', 'P07965', 2, 1, 8400),
('O19001', 'P07885', 2, 1, 5250),
('O19008', 'P00001', 5, 3, 1050),
('O19003', 'P0345', 1, 1, 1200),
('O46866', 'P06734', 1, 1, 1200),
('O46866', 'P07965', 1, 0, 8400),
('O19008', 'P07975', 10, 5, 1050);
''')

# Step 3: Write SQL Queries for Question 3

# a. List the names of all clients having 'a' as the second letter in their names.
print("a. Clients with 'a' as the second letter in their names:")
cursor.execute("SELECT NAME FROM CLIENT_MASTER WHERE NAME LIKE '_a%'")
for row in cursor.fetchall():
    print(row[0])

# b. List the clients who stay in a city whose first letter is 'M'.
print("\nb. Clients in a city starting with 'M':")
cursor.execute("SELECT NAME FROM CLIENT_MASTER WHERE CITY LIKE 'M%'")
for row in cursor.fetchall():
    print(row[0])

# c. List all clients who stay in 'Bangalore' or 'Mangalore'.
print("\nc. Clients in Bangalore or Mangalore:")
cursor.execute("SELECT NAME FROM CLIENT_MASTER WHERE CITY IN ('Bangalore', 'Mangalore')")
for row in cursor.fetchall():
    print(row[0])

# d. List all clients whose BALDUE is greater than value 10000.
print("\nd. Clients with BALDUE greater than 10000:")
cursor.execute("SELECT NAME FROM CLIENT_MASTER WHERE BALDUE > 10000")
for row in cursor.fetchall():
    print(row[0])

# e. List all information from the Sales_order table for orders placed in the month of June.
print("\ne. Sales orders in June:")
cursor.execute("SELECT * FROM SALES_ORDER WHERE MONTH(ORDERDATE) = 6")
for row in cursor.fetchall():
    print(row)

# f. List the Order No & day on which clients placed their order.
print("\nf. Order No and day of orders:")
cursor.execute("SELECT ORDERNO, DAY(ORDERDATE) AS DAY FROM SALES_ORDER")
for row in cursor.fetchall():
    print(row)

# g. List the names, city, and state of clients who are not in the state of 'Maharashtra'.
print("\ng. Clients not in Maharashtra:")
cursor.execute("SELECT NAME, CITY, STATE FROM CLIENT_MASTER WHERE STATE != 'Maharashtra'")
for row in cursor.fetchall():
    print(row)

# Step 4: Exercises on Using Having, Group By, and Joins (Question 4)

# a. Print the description and total quantity sold for each product.
print("\n4a. Description and total quantity sold for each product:")
cursor.execute('''
    SELECT P.DESCRIPTION, SUM(S.QTYDISP) AS TOTAL_SOLD
    FROM PRODUCT_MASTER P
    JOIN SALES_ORDER_DETAILS S ON P.PRODUCTNO = S.PRODUCTNO
    GROUP BY P.PRODUCTNO, P.DESCRIPTION
''')
for row in cursor.fetchall():
    print(row)

# Commit changes and close the connection
conn.commit()
conn.close()