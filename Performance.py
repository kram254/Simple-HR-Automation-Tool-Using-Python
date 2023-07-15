import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit


class PerformanceEvaluationUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Performance Evaluation Tool")
        self.setGeometry(100, 100, 400, 400)

        self.name_label = QLabel("Employee Name:", self)
        self.name_label.setGeometry(50, 50, 100, 30)

        self.name_entry = QLineEdit(self)
        self.name_entry.setGeometry(160, 50, 180, 30)

        self.goal_label = QLabel("Goal:", self)
        self.goal_label.setGeometry(50, 100, 100, 30)

        self.goal_entry = QLineEdit(self)
        self.goal_entry.setGeometry(160, 100, 180, 30)

        self.goal_button = QPushButton("Set Goal", self)
        self.goal_button.setGeometry(50, 150, 290, 30)
        self.goal_button.clicked.connect(self.set_goal)

        self.feedback_label = QLabel("Feedback:", self)
        self.feedback_label.setGeometry(50, 200, 100, 30)

        self.feedback_entry = QTextEdit(self)
        self.feedback_entry.setGeometry(160, 200, 180, 100)

        self.feedback_button = QPushButton("Add Feedback", self)
        self.feedback_button.setGeometry(50, 320, 290, 30)
        self.feedback_button.clicked.connect(self.add_feedback)

        self.report_button = QPushButton("Generate Report", self)
        self.report_button.setGeometry(50, 360, 290, 30)
        self.report_button.clicked.connect(self.generate_report)

        self.db_connection = sqlite3.connect("performance.db")
        self.create_table()

        self.show()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, goal TEXT, feedback TEXT)")
        self.db_connection.commit()

    def set_goal(self):
        employee_name = self.name_entry.text()
        goal = self.goal_entry.text()
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO employees VALUES (?, ?, '')", (employee_name, goal))
        self.db_connection.commit()
        self.goal_entry.clear()

    def add_feedback(self):
        employee_name = self.name_entry.text()
        feedback = self.feedback_entry.toPlainText()
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE employees SET feedback = ? WHERE name = ?", (feedback, employee_name))
        self.db_connection.commit()
        self.feedback_entry.clear()

    def generate_report(self):
        employee_name = self.name_entry.text()
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT goal, feedback FROM employees WHERE name = ?", (employee_name,))
        result = cursor.fetchone()
        if result:
            goal, feedback = result
            print(f"Performance Report for {employee_name}:")
            print("Goal:", goal)
            print("Feedback:", feedback)
        else:
            print(f"Employee '{employee_name}' not found.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PerformanceEvaluationUI()
    sys.exit(app.exec_())
