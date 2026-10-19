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
    Transaction_type  VARCHAR(20) NOT NULL,
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

def transaction(cur,Account_No,Transaction_type,Amount_Note,New_Balance):
    cur.execute(
        """INSERT INTO Transaction 
        (Account_No,Transaction_type,Amount_Note,New_Balance) 
        VALUES (%s,%s,%s,%s,%s)""",
        (Account_No,Transaction_type,Amount_Note,New_Balance),
    )

def money_converter(amount_text):
    """TO covert 205.75 to (25075). since float can make mistake print (0.1+0.3)=0.300000004 by float"""
    try:
        amount=Decimal(amount_text.strip())
    except InvalidOperation :
        raise ValueError("Enter Valid Amount (500 or 284.45)")
    if not amount.is_finite() or amount!=amount.quantize(Decimal("0.01")):
        raise ValueError("Atmost Two Decimal Places Are Allowed.")
    if amount<=0:
        raise ValueError("Amount must be greater then 0.")
    return int(amount*100)

def format_money(money):
    return f"INR{money//100:,}.{money%100:0.2d}"

def read_acc_no():
    acc=input("Account Number: ").strip()
    if not acc.isdigit() or int(acc)<=0 :
        raise ValueError("Account must be positive integer.")
    return int (acc)

def read_money():
    return money_converter(input("Amount(INR): "))

#_Menu

def Create_Account():
    pass

def Deposite():
    pass

def Withdraw():
    pass

def View_Account():
    pass

def Statement():
    pass


Menu="""
----------------BANK MANAGEMENT----------------
1. Create Account
2. Deposite
3. Withdraw
4. View Account
5. Statement
6. Exit
"""  
action={
"1": Create_Account,
"2": Deposite,
"3": Withdraw,
"4": View_Account,
"5": Statement
}