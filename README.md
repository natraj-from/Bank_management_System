# 🏦 Python & MySQL Bank Management System

A robust, console-based banking application built with Python and MySQL. This project emphasizes financial accuracy, database integrity, concurrency control, and clean software architecture.

## 🚀 Features

- **Account Management**: Create new bank accounts with customer names and contact details, automatically assigning unique account numbers.
- **Financial Transactions**: Perform secure **Deposits** and **Withdrawals** with live balance updates.
- **Floating-Point Precision Safety**: Utilizes Python's `Decimal` module and scales currency values into integers (multiplied by 100) to completely avoid floating-point math inaccuracies.
- **Concurrency & Row-Level Locking**: Implements SQL `FOR UPDATE` transaction locking during updates to prevent race conditions.
- **Transaction Ledger**: Automatically logs every transaction type (`Opening`, `Deposit`, `Withdrawal`) with timestamps, amounts, new balances, and custom notes.
- **Account Statements & Views**: View detailed transaction histories ordered chronologically and check live account details.
- **Robust Input Validation**: Strict validation rules for account numbers, text constraints, and currency formats.

---

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Database**: MySQL (InnoDB Engine)
- **Library**: `mysql-connector-python`
- **Built-in Modules**: `os`, `decimal`

---

## ⚙️ Database Schema

The application automatically creates and manages two related relational tables:
1. **`Accounts`**: Stores primary account information (`Account_No`, `Customer_Name`, `Phone`, `Balance` with a `CHECK (Balance >= 0)` constraint).
2. **`Transactions`**: Stores immutable audit logs of all monetary movements linked via a Foreign Key to `Accounts`.

---

## 📦 Getting Started & Setup

### 1. Prerequisites
Make sure you have Python installed along with the MySQL connector:
```bash
pip install mysql-connector-python
```

### 2. Configure Environment Variables (Optional)
The app looks for MySQL credentials via environment variables, defaulting to local settings:
DB_HOST (default: localhost)
DB_PORT (default: 3306)
DB_USER (default: root)
DB_PASSWORD (default: "")
DB_NAME (default: Bank_Management_System)

### ​3. Run the Application
​Navigate to the project folder and run:
```bash
python main_file.py
```

### 4. 📂 Project Structure
Bank_management_System/
│
├── .gitignore          # Excludes local environments, cache, and binaries
├── README.md           # Project documentation
└── main_file.py        # Core application and database logic