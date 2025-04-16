import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

DATA_FILE = "expenses.csv"

def init_data_file():
    if not os.path.exists(DATA_FILE):  # Check if the file exists
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
        df.to_csv(DATA_FILE, index=False)  # Create an empty CSV file with headers

def add_expense():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    else:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return
    
    category = input("Enter category (e.g., Food, Transport, Bills): ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return
    description = input("Enter description (optional): ")

    new_expense = pd.DataFrame([{
        "Date": date,
        "Category": category,
        "Amount": amount,
        "Description": description
    }])

    new_expense.to_csv(DATA_FILE, mode='a', header=not os.path.exists(DATA_FILE), index=False)
    print("Expense added successfully!")

def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    return pd.read_csv(DATA_FILE, parse_dates=["Date"])

def summarize_by_period(df, period):
    df[period] = df["Date"].dt.to_period(period[0].upper())
    summary = df.groupby(period)["Amount"].sum()
    print(f"\n{period.capitalize()} Summary:")
    print(summary)
    return summary

MONTHLY_BUDGET = 20000  # Set your desired monthly budget here


def check_overspending(df):
    current_month = datetime.today().strftime('%Y-%m')
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    month_total = df[df['Month'] == current_month]["Amount"].sum()
    print(f"\n Total spent this month ({current_month}): ${month_total:.2f}")

    if month_total > MONTHLY_BUDGET:
        print(" ALERT: You've exceeded your monthly budget!")
    elif month_total > MONTHLY_BUDGET * 0.9:
        print(" Warning: You're close to reaching your monthly budget.")



def summarize_expenses():
    df = load_data()
    if df.empty:
        print("No data to analyze.")
        return

    print("\n Total Spent by Category:")
    print(df.groupby("Category")["Amount"].sum())

    summarize_by_period(df, "week")
    summarize_by_period(df, "month")
    check_overspending(df)


def visualize_expenses():
    df = load_data()
    if df.empty:
        print("No data to visualize.")
        return

    df["Week"] = df["Date"].dt.to_period('W')
    df["Month"] = df["Date"].dt.to_period('M')

    monthly = df.groupby("Month")["Amount"].sum()
    category = df.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(14, 6))

    plt.subplot(1, 2, 1)
    monthly.plot(kind='bar', title="📆 Monthly Expenses", color='skyblue')
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45)

    plt.subplot(1, 2, 2)
    category.plot(kind='pie', title="💰 Spending by Category", autopct='%1.1f%%', startangle=140)
    plt.ylabel("")

    plt.tight_layout()
    plt.show()

def view_expenses():
    df = load_data()
    print("\n🧾 Recent Expenses:")
    print(df.sort_values("Date", ascending=False).head(10))

def main():
    init_data_file()

    while True:
        print("\n Personal Finance Tracker ")
        print("1. Log Expense")
        print("2. View Recent Expenses")
        print("3. Generate Weekly/Monthly Summaries")
        print("4. Visualize Spending")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            summarize_expenses()
        elif choice == '4':
            visualize_expenses()
        elif choice == '5':
            print("👋 Exiting. Stay financially smart!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
