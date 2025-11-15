# 💰 Expense Tracker App (Python + Tkinter + SQLite)

A clean, modern, and beginner-friendly **desktop application** to track daily expenses.  
Built using **Python, Tkinter, SQLite, and Matplotlib** — this project is perfect for our portfolios in  
**B.Tech CSE / AIML**, showing skills in:

✔️ GUI development  
✔️ Database integration  
✔️ Data visualization  
✔️ Modular Python project structure  
✔️ CRUD operations  
✔️ Basic analytics  

---

## 🚀 Features

### 🖥️ User Interface
- Modern Tkinter UI  
- Add, view, and delete expenses  
- Dropdown filtering  
- Category selection  
- Monthly filters  

### 📊 Analytics
- Total monthly spending  
- Category-wise insights  
- **Monthly expense trend (line chart)**  
- **Categorywise expense (Bar graph chart)**  

### 🗄️ Database
- SQLite for persistent local storage  
- Auto-created tables  
- Clean, modular DB handling  

---

## 📂 Project Structure

expense-tracker/
│
├── main.py                    # Main application (Launches the UI)
├── database.py                # Database initialization (Handles all SQLite operations)
├── ui.py                      # Tkinter/CustomTkinter UI layouts
├── exporter.py                # CSV + PDF export
├── charts.py                  # matplotlib reports
├── README.md                  # Project documentation for GitHub
├── requirements.txt           # Python dependencies
├── .gitignore                 # Ignore unwanted files
│
├── data/
│   ├── expenses.db            # SQLite database
│
├── exports/
│   ├── sample.csv             # Export folder for CSV/PDF
│   ├── sample.pdf
│
└── screenshots/
    ├── uiHome.png            # UI screenshot for README
    ├── summaryChart.png
    ├── monthlyTrendChart.png

---

## 🛠️ Installation & Setup

### **1. Clone the Repository**
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker

markdown
Copy code

### **2. Install Dependencies**
pip install -r requirements.txt

markdown
Copy code

### **3. Run the Application**
python main.py

yaml
Copy code

---

## 📦 Requirements

tkinter
matplotlib
sqlite3 (built-in)
reportlab
customtkinter

---

<!-- ## 📸 Screenshots

> Add your UI screenshots under `assets/` and embed them: -->

---

## 🔮 Future Improvements

- Login system  
- AI-powered budget advice (future AIML add-on)  

---

## 👨‍💻 Author
**Manoranjan Gope**  
B.Tech CSE (AI & ML)
First year

---

## ⭐ Contribute
Pull requests are welcome!  
If you like this project, please ⭐ the repo.
