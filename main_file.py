import os
from decimal import Decimal,InvalidOperation

import mysql.connector

deposit = "Deposit"
withdrawal = "Withdrawal"

DATABASE = {
    "host" : os.getenv("DB_HOST","localhost"),
    "port" : int(os.getnv("DB_PORT","3306")),
    "user" : os.getnv("DB_USER","root"),
    "password" : os.getnv("DB_PASSWORD",""),
    "database" : os.getnv("DB_NAME","Bank_Management_System"),
}

Table=[
    
    """CREATE TABLE IF NOT EXISTS Accounts(
    Account_NO INT AUTO_INCREMENT PRIMARY KEY,
    Customer_Name VARCHAR (100) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Balance_note BIGINT NOT NULL DEFAULT 0,
    CHECK (Balance_note>=0)
    )ENGINE=InnoDB """

    """CREATE TABLE IF NOT EXISTS Transactions(
    Transaction_ID INT AUTO_INCREMENT PRIMARY KEY,
    Account_No INT NOT NULL,
    Amount_Note BIGINT NOT NULL,
    New_Balance BIGINT NOT NULL,
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Note VARCHAR (450),
    FOREIGN KEY (Account_No) REFERENCES Accounts(Account_No)    
    )ENGINE=InnoDB """

]

def connect():
    return mysql.connector.connect(**DATABASE)

def create_table():
    con=connect()
    try :
        cur=con.cursor()
        for queries in Table:
            cur.execute(queries)
        con.commit()

    finally:
        cur.close()
        con.close()

def get_acc (cur,Account_No,lock=False):
    sql=(
        "Select Account_No,Customer_Name,Phone,Balance_note"
        "FROM Accounts WHERE Account_NO = %s"
    )
    if lock:
        sql+="  FOR UPDATE"
    cur.execute(sql,(Account_No,))
    return cur.fetchone()