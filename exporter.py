import csv
from tkinter import messagebox, filedialog
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def export_csv(tree):
    filePath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
    if not filePath:
        return
    
    rows = [tree.item(i)["values"] for i in tree.get_children()]
    if not rows:
        messagebox.showwarning("No Data", "Nothing to export.")
        return

    with open(filePath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(['ID','Date','Category','Description','Amount'])
        w.writerows(rows)

    messagebox.showinfo("Success", "CSV exported successfully!")

def export_pdf(tree):
    filePath = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
    if not filePath:
        return
    
    rows = [tree.item(i)['values'] for i in tree.get_children()]
    if not rows:
        messagebox.showwarning("No Data", "Nothing to export.")
        return

    doc = SimpleDocTemplate(filePath, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("Expense Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    tableData = [['ID','Date','Category','Description','Amount']] + rows
    table = Table(tableData)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), colors.gray),
        ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('GRID',(0,0),(-1,-1),1,colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

    messagebox.showinfo("Success", "PDF exported successfully!")
