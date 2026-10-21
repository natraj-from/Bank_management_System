import os
from decimal import Decimal, InvalidOperation

import mysql.connector

DEPOSIT = "DEPOSIT"
WITHDRAWAL = "WITHDRAWAL"

DATABASE = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "Bank_Management_System"),
}

Table = [
    """CREATE TABLE IF NOT EXISTS Accounts(
    Account_No INT AUTO_INCREMENT PRIMARY KEY,
    Customer_Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Balance BIGINT NOT NULL DEFAULT 0,
    CHECK (Balance>=0)
    )ENGINE=InnoDB """,
    """CREATE TABLE IF NOT EXISTS Transactions(
    Transaction_ID INT AUTO_INCREMENT PRIMARY KEY,
    Account_No INT NOT NULL,
    Transaction_type  VARCHAR(20) NOT NULL,
    Amount_Note BIGINT NOT NULL,
    New_Balance BIGINT NOT NULL,
    Created_At TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Note VARCHAR (450),
    FOREIGN KEY (Account_No) REFERENCES Accounts(Account_No)    
    )ENGINE=InnoDB """,
]


def connect():
    return mysql.connector.connect(**DATABASE)


def create_table():
    con = connect()
    cur = None
    try:
        cur = con.cursor()
        for queries in Table:
            cur.execute(queries)
        con.commit()
    finally:
        if cur:
            cur.close()
        con.close()


def get_acc(cur, Account_No, lock=False):
    sql = (
        "SELECT Account_No,Customer_Name,Phone,Balance "
        "FROM Accounts WHERE Account_No = %s"
    )
    if lock:
        sql += "  FOR UPDATE"
    cur.execute(sql, (Account_No,))
    return cur.fetchone()


def transaction(
    cur, Account_No, Transaction_type, Amount_Note, New_Balance, Note
):
    cur.execute(
        """INSERT INTO Transactions
        (Account_No,Transaction_type,Amount_Note,New_Balance,Note) 
        VALUES (%s,%s,%s,%s,%s)""",
        (Account_No, Transaction_type, Amount_Note, New_Balance, Note),
    )


def money_converter(amount_text):
    """To covert 205.75 to (25075). since float can make mistake print (0.1+0.3)=0.300000004 by float"""
    try:
        amount = Decimal(amount_text.strip())
    except InvalidOperation:
        raise ValueError("Enter Valid Amount (500 or 284.45)")
    if not amount.is_finite() or amount != amount.quantize(Decimal("0.01")):
        raise ValueError("Atmost Two Decimal Places Are Allowed.")
    if amount <= 0:
        raise ValueError("Amount must be greater then 0.")
    return int(amount * 100)


def format_money(money):
    return f"INR {money//100:,}.{money%100:02d}"


def read_text(name, max=100):
    while True:
        value = input(name).strip()
        if value and len(value) <= max:
            return value
        print(f"Value is required and must be atmost {max} characters.")


def read_acc_no():
    acc = input("Account Number: ").strip()
    if not acc.isdigit() or int(acc) <= 0:
        raise ValueError("Account must be positive integer.")
    return int(acc)


def read_money():
    return money_converter(input("Amount(INR): "))


# _Menu


def Create_Account():
    Customer_Name = read_text("Customer Name: ")
    Phone = read_text("Phone/Contact: ", max=15)

    con = connect()
    cur = None
    try:
        cur = con.cursor()
        cur.execute(
            """INSERT INTO Accounts(
            Customer_Name,Phone) VALUES(
            %s,%s)""",
            (Customer_Name, Phone),
        )
        acc_no = cur.lastrowid
        transaction(cur, acc_no, "Opening", 0, 0, "Account Created")
        con.commit()
        print(f"Account created.\nAccount Number={acc_no}")
    except Exception:
        con.rollback()
        raise
    finally:
        if cur:
            cur.close()
        con.close()


def New_Balance(Transaction_Type):
    acc_no = read_acc_no()
    amt = read_money()

    con = connect()
    cur = None
    try:
        cur = con.cursor()
        acc_row = get_acc(cur, acc_no, lock=True)
        if acc_row is None:
            print("Account not found.")
            return

        balance = acc_row[3]
        if Transaction_Type == DEPOSIT:
            revised_balance = balance + amt
        else:
            if amt > balance:
                print(
                    f"Insufficient Balance.\nCurrent Balance: {format_money(balance)}"
                )
                return
            revised_balance = balance - amt

        cur.execute(
            "UPDATE Accounts SET Balance=%s WHERE Account_No=%s",
            (revised_balance, acc_no),
        )

        transaction(
            cur,
            acc_no,
            Transaction_Type,
            amt,
            revised_balance,
            Transaction_Type.title(),
        )
        con.commit()
        print(
            f"{Transaction_Type.title()} Successful.\nNew Balance: {format_money(revised_balance)}"
        )

    except Exception:
        con.rollback()
        raise

    finally:
        if cur:
            cur.close()
        con.close()


def Deposit():
    New_Balance(DEPOSIT)


def Withdraw():
    New_Balance(WITHDRAWAL)


def Statement():
    acc_no = read_acc_no()
    con = connect()
    cur = None

    try:
        cur = con.cursor()
        acc_row = get_acc(cur, acc_no)
        if acc_row is None:
            print("Account not found.")
            return
        cur.execute(
            """SELECT Transaction_ID, Transaction_type, Amount_Note, New_Balance, Created_At, Note 
        FROM Transactions WHERE Account_No = %s ORDER BY Created_At, Transaction_ID""",
            (acc_no,),
        )
        print(" ID | TYPE | AMOUNT | NEW BALANCE | DATE | NOTE ")
        for (
            Transaction_ID,
            Transaction_type,
            Amount_Note,
            New_Balance,
            Created_At,
            Note,
        ) in cur.fetchall():
            print(
                f"{Transaction_ID} | {Transaction_type} | {format_money(Amount_Note)} | {format_money(New_Balance)} | {Created_At} | {Note}"
            )

    finally:
        if cur:
            cur.close()
        con.close()


def View_Account():
    acc_no = read_acc_no()
    con = connect()
    cur = None

    try:
        cur = con.cursor()
        acc_row = get_acc(cur, acc_no)
        if acc_row is None:
            print("Account not found.")
            return
        Account_No, Customer_Name, Phone, Balance = acc_row
        print(
            f"Account: {Account_No} | Name: {Customer_Name} | Contact: {Phone} | Balance: {format_money(Balance)}"
        )

    finally:
        if cur:
            cur.close()
        con.close()


Menu = """
----------------BANK MANAGEMENT----------------
1. Create Account
2. Deposit
3. Withdraw
4. View Account
5. Statement
6. Exit
"""
Action = {
    "1": Create_Account,
    "2": Deposit,
    "3": Withdraw,
    "4": View_Account,
    "5": Statement,
}


def main():
    try:
        create_table()
    except mysql.connector.Error as error:
        print("Cannot connect to MYSQL: ", error)
        return
    while True:
        print(Menu)
        try:
            choice = input("Choice(1-6): ").strip()

        except (EOFError, KeyboardInterrupt):
            print()
            break
        if choice == "6":
            print("See you soon.")
            break
        action = Action.get(choice)
        if action is None:
            print("Choose one of the listed options.")
            continue
        try:
            action()
        except Exception as error:
            print(f"Operation failed. {error}")


if __name__ == "__main__":
    main()