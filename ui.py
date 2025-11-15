import customtkinter as ctk
from tkinter import *
from tkinter import ttk, messagebox
import datetime

from database import (
    connect_db,
    add_expense,
    delete_expense,
    get_all_expenses,
    get_categories,
    filter_expenses,
    total_amount
)

from exporter import export_csv, export_pdf
from charts import category_summary, monthly_trend


def run_app():
    # ---------------------- INIT APP ----------------------
    conn, cursor = connect_db()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Smart Expense Tracker")
    app.geometry("1000x600")

    # ======================================================
    # FUNCTIONS
    # ======================================================

    def clear_fields():
        dateEntry.delete(0, END)
        categoryEntry.delete(0, END)
        descEntry.delete(0, END)
        amountEntry.delete(0, END)

    def load_expenses():
        """Load all expenses into table"""
        for row in tree.get_children():
            tree.delete(row)

        data = get_all_expenses(cursor)
        for row in data:
            tree.insert("", END, values=row)

        total = total_amount(cursor)
        totalLabel.configure(text=f"💰 Total: ₹{total:.2f}")

        load_categories()

    def load_categories():
        cats = get_categories(cursor)
        categoryCombo.configure(values=["All"] + cats)
        categoryCombo.set("All")

    def add_expense_handler():
        date = dateEntry.get()
        if not date:
            date = datetime.date.today().strftime("%Y-%m-%d")

        category = categoryEntry.get()
        desc = descEntry.get()
        amount = amountEntry.get()

        if not category or not amount:
            messagebox.showwarning("Input Error", "Please fill all required fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number!")
            return

        add_expense(cursor, conn, date, category, desc, amount)
        messagebox.showinfo("Success", "Expense added successfully!")
        clear_fields()
        load_expenses()

    def delete_handler():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row")
            return

        item = tree.item(selected[0])
        exp_id = item["values"][0]

        delete_expense(cursor, conn, exp_id)
        messagebox.showinfo("Success", "Expense deleted!")
        load_expenses()

    def apply_filter_handler():
        month = monthVar.get()
        category = categoryVar.get()

        data = filter_expenses(cursor, month, category)

        for row in tree.get_children():
            tree.delete(row)

        for row in data:
            tree.insert("", END, values=row)

        total = sum(float(r[4]) for r in data) if data else 0
        totalLabel.configure(text=f"💰 Total: ₹{total:.2f}")

    def show_summary_handler():
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = cursor.fetchall()
        if not data:
            messagebox.showinfo("Info", "No expenses to show.")
            return
        category_summary(data)

    def show_trend_handler():
        cursor.execute(
            "SELECT strftime('%m', date) as month, SUM(amount) FROM expenses GROUP BY month ORDER BY month"
        )
        data = cursor.fetchall()
        if not data:
            messagebox.showinfo("Info", "Not enough data")
            return
        monthly_trend(data)

    # ======================================================
    # UI COMPONENTS
    # ======================================================

    title = ctk.CTkLabel(app, text="Smart Expense Tracker", font=ctk.CTkFont(size=24, weight="bold"))
    title.pack(pady=10)

    # ---------- INPUT FRAME ----------
    inputFrame = ctk.CTkFrame(app)
    inputFrame.pack(pady=10)

    # Date
    ctk.CTkLabel(inputFrame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
    dateEntry = ctk.CTkEntry(inputFrame, width=150)
    dateEntry.grid(row=0, column=1, padx=5, pady=5)

    # Category
    ctk.CTkLabel(inputFrame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
    categoryEntry = ctk.CTkEntry(inputFrame, width=150)
    categoryEntry.grid(row=1, column=1, padx=5, pady=5)

    # Description
    ctk.CTkLabel(inputFrame, text="Description:").grid(row=2, column=0, padx=5, pady=5)
    descEntry = ctk.CTkEntry(inputFrame, width=150)
    descEntry.grid(row=2, column=1, padx=5, pady=5)

    # Amount
    ctk.CTkLabel(inputFrame, text="Amount (₹):").grid(row=3, column=0, padx=5, pady=5)
    amountEntry = ctk.CTkEntry(inputFrame, width=150)
    amountEntry.grid(row=3, column=1, padx=5, pady=5)

    # ---------- BUTTONS ----------
    buttonFrame = ctk.CTkFrame(app)
    buttonFrame.pack(pady=10)

    ctk.CTkButton(buttonFrame, text="➕ Add Expense", command=add_expense_handler).grid(row=0, column=0, padx=10)

    ctk.CTkButton(buttonFrame, text="🗑 Delete Expense", fg_color="red", command=delete_handler).grid(row=0, column=1, padx=10)

    ctk.CTkButton(buttonFrame, text="📊 Expense Summary", fg_color="#2196f3", command=show_summary_handler).grid(row=0, column=2, padx=10)

    ctk.CTkButton(buttonFrame, text="📈 Monthly Trend", fg_color="#ff9800", command=show_trend_handler).grid(row=0, column=3, padx=10)

    ctk.CTkButton(buttonFrame, text="📤 Export CSV", fg_color="#009688", command=lambda: export_csv(tree)).grid(row=0, column=4, padx=10)

    ctk.CTkButton(buttonFrame, text="📑 Export PDF", fg_color="#795548", command=lambda: export_pdf(tree)).grid(row=0, column=5, padx=10)

    # ---------- FILTERS ----------
    filterFrame = ctk.CTkFrame(app)
    filterFrame.pack(pady=10)

    monthVar = StringVar()
    categoryVar = StringVar()

    ctk.CTkLabel(filterFrame, text="Month:").grid(row=0, column=0, padx=5)
    monthCombo = ctk.CTkComboBox(
        filterFrame,
        variable=monthVar,
        values=["All", "01-Jan", "02-Feb", "03-Mar", "04-Apr", "05-May",
                "06-Jun", "07-Jul", "08-Aug", "09-Sep", "10-Oct", "11-Nov", "12-Dec"],
        width=120
    )
    monthCombo.set("All")
    monthCombo.grid(row=0, column=1, padx=5)

    ctk.CTkLabel(filterFrame, text="Category:").grid(row=0, column=2, padx=5)
    categoryCombo = ctk.CTkComboBox(filterFrame, variable=categoryVar, width=120)
    categoryCombo.grid(row=0, column=3, padx=5)

    ctk.CTkButton(filterFrame, text="🔍 Filter", fg_color="#673ab7", command=apply_filter_handler).grid(row=0, column=4, padx=10)
    ctk.CTkButton(filterFrame, text="🧹 Clear", fg_color="#607d8b", command=load_expenses).grid(row=0, column=5, padx=10)

    # ---------- TOTAL LABEL ----------
    totalLabel = ctk.CTkLabel(app, text="Total: ₹0.00", font=ctk.CTkFont(size=16, weight="bold"))
    totalLabel.pack(pady=5)

    # ---------- EXPENSE TABLE ----------
    tableFrame = ctk.CTkFrame(app)
    tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("ID", "Date", "Category", "Description", "Amount")
    tree = ttk.Treeview(tableFrame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True)

    # Load initial data
    load_expenses()

    # -------- RUN APP ----------
    app.mainloop()
    conn.close()

