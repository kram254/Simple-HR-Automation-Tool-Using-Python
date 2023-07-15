import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QTextEdit, QPushButton

class PerformanceEvaluationUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Performance Evaluation Tool")
        self.setGeometry(100, 100, 400, 400)

        self.industry_label = QLabel("Industry:", self)
        self.industry_label.setGeometry(50, 50, 100, 30)

        self.industry_combo = QComboBox(self)
        self.industry_combo.setGeometry(160, 50, 180, 30)
        self.industry_combo.addItem("Engineering")
        self.industry_combo.addItem("Medical")
        self.industry_combo.addItem("Manufacturing")
        self.industry_combo.addItem("Customer Care")
        self.industry_combo.addItem("Transport")
        self.industry_combo.addItem("Software Industry")
        self.industry_combo.addItem("Construction")
        self.industry_combo.addItem("Agriculture")
        self.industry_combo.addItem("Real Estate")
        self.industry_combo.addItem("Tourism")
        self.industry_combo.addItem("Media")
        self.industry_combo.currentIndexChanged.connect(self.load_kpis)

        self.kpi_label = QLabel("KPIs:", self)
        self.kpi_label.setGeometry(50, 100, 100, 30)

        self.kpi_entry = QTextEdit(self)
        self.kpi_entry.setGeometry(160, 100, 180, 150)

        self.evaluate_button = QPushButton("Evaluate Performance", self)
        self.evaluate_button.setGeometry(50, 280, 290, 30)
        self.evaluate_button.clicked.connect(self.evaluate_performance)

        self.db_connection = None
        try:
            self.db_connection = sqlite3.connect("performance.db")
            self.create_table()
        except sqlite3.Error as e:
            print("Database connection error:", str(e))

        self.show()

    def create_table(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS industries (name TEXT PRIMARY KEY, kpis TEXT)")
            self.db_connection.commit()
        except sqlite3.Error as e:
            print("Database error:", str(e))

    def load_kpis(self):
        selected_industry = self.industry_combo.currentText()
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT kpis FROM industries WHERE name = ?", (selected_industry,))
            result = cursor.fetchone()
            if result:
                kpis = result[0]
                self.kpi_entry.setPlainText(kpis)
            else:
                self.kpi_entry.clear()
        except sqlite3.Error as e:
            print("Database error:", str(e))

    def evaluate_performance(self):
        selected_industry = self.industry_combo.currentText()
        kpis = self.kpi_entry.toPlainText()
        performance_data = {}  # Replace with actual performance evaluation logic
        performance_data["KPI 1"] = 80
        performance_data["KPI 2"] = 75
        performance_data["KPI 3"] = 90

        report_text = f"Performance Evaluation for {selected_industry}:\n\n"
        for kpi, score in performance_data.items():
            report_text += f"{kpi}: {score}\n"
        print(report_text)

        try:
            cursor = self.db_connection.cursor()
            cursor.execute("INSERT OR REPLACE INTO industries (name, kpis) VALUES (?, ?)",
                           (selected_industry, kpis))
            self.db_connection.commit()
        except sqlite3.Error as e:
            print("Database error:", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PerformanceEvaluationUI()
    sys.exit(app.exec_())
