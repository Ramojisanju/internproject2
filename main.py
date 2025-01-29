import sqlite3
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


def create_db():
    conn=sqlite3.connect('finanace.db')
    c=conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS transactions(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             type  TEXT,
             amount  REAL,
             description  TEXT)""")
    conn.commit()
    conn.close()

def add_data(amount,type,description):
    conn=sqlite3.connect('finance.db')
    c=conn.cursor()
    c.execute("INSERT INTO transactions(amount,type,description) VALUES(?,?,?)",(amount,type,description))
    conn.commit()
    conn.close()

def get_data():
    conn=sqlite3.connect('finance.db')
    c=conn.cursor()
    c.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    data=c.fetchall()
    conn.close()
    return data


            
class FinanceApp():
    def __init__(self,root):
        self.root=root
        self.root.title="Personal Finance management tool"

        self.amount_label=tk.Label(root,text="Amount:")
        self.amount_label.pack(pady=5)

        self.amount_entry=tk.Entry(root)
        self.amount_entry.pack(pady=5)

        self.type_label=tk.Label(root,text="income/expense")
        self.type_label.pack(pady=5)
        
        self.type_entry=tk.Entry(root)
        self.type_entry.pack(pady=5)

        self.description_label=tk.Label(root,text="description:")
        self.description_label.pack(pady=5)

        self.description_entry=tk.Entry(root)
        self.description_entry.pack(pady=5)

        self.add_transaction_button=tk.Button(root,text="add_transaction",command=self.add_transaction)
        self.add_transaction_button.pack(pady=20)

        self.show_budget_button=tk.Button(root,text="show_budget",command=self.show_budget)
        self.show_budget_button.pack(pady=20)

        self.visualize_data_button=tk.Button(root,text="visualize_data",command=self.visualize_data)
        self.visualize_data_button.pack(pady=20)

    def add_transaction(self):
        amount=self.amount_entry.get()
        type=self.type_entry.get()
        description=self.description_entry.get()
        if amount and type and description:
            add_data(float(amount),type,description)
            messagebox.showinfo(title="add_transaction",message="sucessfully added")
        else:
            messagebox.showerror(title="add_transaction",message="error occured")

    def show_budget(self):
        data=get_data()
        income=sum(amount for type,amount in data  if type=="income")
        expense=sum(amount for type,amount in data if type=="expense")
        balance = income-expense
        message=f"INCOME:{income}\nEXPENSE:{expense}\nBALANCE:{balance}"
        messagebox.showinfo("show_budget",message)

    def visualize_data(self):
        data=get_data()

        types=[type for type,_ in data]
        amounts=[amount for _,amount in data]
        plt.bar(types,amounts)
        plt.title("income vs expense")
        plt.xlabel("type")
        plt.ylabel("amount ($)")
        plt.show()


def main():
    create_db()
    root=tk.Tk()
    app=FinanceApp(root)
    root.mainloop()

if __name__=="__main__":
    main()