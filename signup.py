from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector as mysql
import hashlib

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "gb"
        self.port = 3306
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connect(host=self.host, user=self.user, password=self.password, database=self.database, port=self.port)
            self.cursor = self.conn.cursor()
            print("connected")
        except mysql.Error as e:
            print(e)

database = Database()
database.connect()

class SignupWidget(QDialog):
    def __init__(self):
        super().__init__()

        # Add signup widgets
        layout = QVBoxLayout()

        label_username = QLabel("Username:")
        self.line_edit_username = QLineEdit()
        layout.addWidget(label_username)
        layout.addWidget(self.line_edit_username)

        label_password = QLabel("Password:")
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password)
        layout.addWidget(self.line_edit_password)

        # Add signup button
        self.btn_signup = QPushButton('Sign Up')
        self.btn_signup.clicked.connect(self.signup)
        layout.addWidget(self.btn_signup)

        # Set the layout
        self.setLayout(layout)

        # Set the window properties
        self.setWindowTitle('Sign Up')

    def signup(self):
        # Implement logic for signing up
        username = self.line_edit_username.text()
        password = self.line_edit_password.text()

        # Use the specific salt value
        salt = 'eee27ffc9bd140c954e4ffedc10a86a5'

        # Hash the password using SHA256 and the salt
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()

        # Check if the username already exists in the database
        sql = "SELECT * FROM user WHERE username=%s"
        val = (username,)
        database.cursor.execute(sql, val)
        result = database.cursor.fetchone()

        if result:
            # Display an error message if the username already exists
            QMessageBox.warning(self, 'Error', 'Username already exists.')
        else:
            # Insert the new user into the database
            sql = "INSERT INTO user (username, password, salt) VALUES (%s, %s, %s)"
            val = (username, hashed_password, salt)
            database.cursor.execute(sql, val)
            database.conn.commit()
            QMessageBox.information(self, 'Success', 'User added successfully.')
            self.close()
