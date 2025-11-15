import matplotlib.pyplot as plt

def category_summary(data):
    if not data:
        return

    categories = [x[0] for x in data]
    amounts = [x[1] for x in data]

    plt.bar(categories, amounts)
    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount")
    plt.show()

def monthly_trend(data):
    if not data:
        return

    months = [int(row[0]) for row in data]
    totals = [row[1] for row in data]

    months_label = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

    plt.plot([months_label[m-1] for m in months], totals, marker='o')
    plt.title("Monthly Expense Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Amount")
    plt.grid(True)
    plt.show()
