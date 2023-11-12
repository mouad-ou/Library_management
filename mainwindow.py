import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget, QDialog
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from login import LoginWidget
from signup import SignupWidget


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Create buttons
        self.btn_login = QPushButton('Login')
        self.btn_signup = QPushButton('Sign Up')
        self.btn_about = QPushButton('About')

        # Connect buttons to slots
        self.btn_login.clicked.connect(self.show_login_dialog)
        self.btn_signup.clicked.connect(self.show_signup_page)
        self.btn_about.clicked.connect(self.show_about_page)

        # Create layout
        v_layout = QVBoxLayout()
        v_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        v_layout.addWidget(self.btn_login, alignment=Qt.AlignCenter)
        self.btn_login.setFixedSize(300, 50)
        self.btn_login.setStyleSheet(
            "background-color: #474A56; color: white; font-size: 20px; font-weight: bold; border-radius: 10px;")
        v_layout.addWidget(self.btn_signup, alignment=Qt.AlignCenter)
        self.btn_signup.setFixedSize(300, 50)
        self.btn_signup.setStyleSheet(
            "background-color: #474A56; color: white; font-size: 20px; font-weight: bold; border-radius: 10px;")
        v_layout.addWidget(self.btn_about, alignment=Qt.AlignCenter)
        self.btn_about.setStyleSheet(
            "background-color: #474A56; color: white; font-size: 20px; font-weight: bold; border-radius: 10px;")
        self.btn_about.setFixedSize(300, 50)

        v_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the layout
        self.setLayout(v_layout)

        # Set the window properties
        self.setWindowTitle('Welcome')
        self.setGeometry(550, 200, 900, 600)
        # Set the background image
        palette = self.palette()
        pixmap = QPixmap("bg.jpg")
        palette.setBrush(QPalette.Background, QBrush(pixmap))
        self.setPalette(palette)

    def show_login_dialog(self):
        login_dialog = LoginWidget()
        result = login_dialog.exec_()
        if result == QDialog.Accepted:
            print("Login accepted")
        else:
            print("Login canceled")
        
        self.close()

    def show_signup_page(self):
        print("Showing signup page")
        signup_dialog = SignupWidget()
        result = signup_dialog.exec_()
        if result == QDialog.Accepted:
            print("Signup accepted")
        else:
            print("Signup canceled")
    def show_about_page(self):
        print("Showing about page")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
