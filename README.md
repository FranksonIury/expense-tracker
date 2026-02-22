# Expense Tracker CLI

A simple Command Line Interface (CLI) application built in Python to manage and track personal expenses.

This project allows users to add, update, list, delete, calculate totals, and export expenses using a structured JSON file for storage.

It is inspired from the Expense Tracker project featured in Backend Roadmap from roadmap.sh

---

##  Features

- Add new expenses
- Update existing expenses
- List all expenses
- Delete expenses (with confirmation)
- Calculate total expenses
- Calculate expenses by month
- Export expenses to a CSV file
- Automatic JSON file creation and validation

---

##  Technologies Used

- Python 3
- argparse (CLI argument parsing)
- JSON (data persistence)
- CSV (data export)
- os (file handling)

---

##  Data Storage

All expenses are stored in a local file:
dados.json

If the file does not exist, it will be automatically created.

Structure example:

```json
{
    "last_id": 2,
    "despesas": {
        "1": {
            "name": "Rent",
            "value": 1200,
            "description": "Monthly apartment rent",
            "month": 1
        }
    }
}
```
## Installation
1. Clone the repository:
   git clone https://github.com/FranksonIury/expense-tracker.git
2. Navigate into the project folder:
   cd expense-tracker
3. Run the script using python:
   python expense.py

##  Usage

###  Add an expense

```bash
python expense.py add "Rent" 1200 1 -d "Monthly apartment rent"
```
Arguments:

-`name` → Expense name

-`value` → Expense value (integer)

-`month` → Month number (1–12)

-`-d or --description` → Optional description

## Update an expense
```bash
python expense.py up 1 value 1500
```
## List all expenses
```bash
python expense.py list
```
## Show total amount
```bash
python expense.py amount -t
```
## Show amount by month
```bash
python expense.py amount -m 1
```
## Delete an expense
```bash
python expense.py delete 1 --yes
```
The flag --yes is required to confirm deletion
## Export to CSV
```bash
python expense.py export
```
this will generate a file called:
despesas.csv

## Author
  Built as a backend practice project to improve Python and CLI development skills.
  
