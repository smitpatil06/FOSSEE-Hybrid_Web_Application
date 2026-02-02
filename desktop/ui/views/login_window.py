from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QMessageBox, QTabWidget, QWidget)
from PyQt5.QtCore import Qt
import requests

class LoginWindow(QDialog):
    def __init__(self, api_client, parent=None):
        super().__init__(parent)
        self.api_client = api_client
        self.user_data = None
        
        self.setWindowTitle("ChemLabViz - Login")
        self.setFixedSize(480, 480)
        self.setStyleSheet("""
            QDialog { 
                background-color: #f5f7fa; 
            }
            QLabel { 
                font-size: 13px; 
                color: #333; 
            }
            QLineEdit { 
                padding: 8px 10px; 
                border: 1px solid #cbd5e1; 
                border-radius: 4px;
                background-color: white;
                color: #111827;
                font-size: 13px;
                min-height: 22px;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
            QLineEdit:focus {
                border: 2px solid #3B82F6;
                outline: none;
            }
            QPushButton { 
                background-color: #2563EB; 
                color: white; 
                border: none;
                border-radius: 5px; 
                padding: 10px 16px; 
                font-weight: bold;
                font-size: 14px;
                min-height: 32px;
            }
            QPushButton:hover { 
                background-color: #1D4ED8; 
            }
            QPushButton:pressed {
                background-color: #1E40AF;
            }
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                background-color: white;
                border-radius: 5px;
                padding: 0px;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                padding: 10px 24px;
                border: 1px solid #e2e8f0;
                border-bottom: none;
                color: #334155;
                font-size: 13px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #1e293b;
                border-bottom: 2px solid white;
            }
            QTabBar::tab:hover {
                background-color: #e2e8f0;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #3B82F6;
                color: #1e293b;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(12)
        
        # Logo/Title
        title = QLabel("⚗️ ChemLabViz")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #1e293b;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Chemical Data Visualization Platform")
        subtitle.setStyleSheet("font-size: 12px; color: #64748b; margin-bottom: 5px;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        # Add some spacing before tabs
        layout.addSpacing(8)
        
        # Tab Widget for Login/Register
        tabs = QTabWidget()
        tabs.addTab(self.create_login_tab(), "Login")
        tabs.addTab(self.create_register_tab(), "Register")
        layout.addWidget(tabs)
        
        # Footer
        footer = QLabel("Powered by FOSSEE")
        footer.setStyleSheet("color: #94a3b8; font-size: 12px; margin-top: 10px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
        
        self.setLayout(layout)
    
    def create_login_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(6)
        
        # Username field with label
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-weight: bold; margin-bottom: 1px;")
        layout.addWidget(username_label)
        
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        layout.addWidget(self.login_username)
        
        # Spacing between fields
        layout.addSpacing(8)
        
        # Password field with label
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold; margin-bottom: 1px;")
        layout.addWidget(password_label)
        
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.returnPressed.connect(self.handle_login)
        layout.addWidget(self.login_password)
        
        # Spacing before button
        layout.addSpacing(12)
        
        # Login Button
        btn_login = QPushButton("Login")
        btn_login.setCursor(Qt.PointingHandCursor)
        btn_login.clicked.connect(self.handle_login)
        layout.addWidget(btn_login)
        
        # Spacing before demo hint
        layout.addSpacing(8)
        
        # Demo credentials hint
        demo_hint = QLabel("Demo: demo/demo123")
        demo_hint.setStyleSheet("color: #64748b; font-size: 10px; font-style: italic;")
        demo_hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(demo_hint)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def create_register_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(6)
        
        # Username field with label
        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-weight: bold; margin-bottom: 1px;")
        layout.addWidget(username_label)
        
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        layout.addWidget(self.register_username)
        
        # Spacing between fields
        layout.addSpacing(8)
        
        # Email field with label
        email_label = QLabel("Email:")
        email_label.setStyleSheet("font-weight: bold; margin-bottom: 1px;")
        layout.addWidget(email_label)
        
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("your@email.com")
        layout.addWidget(self.register_email)
        
        # Spacing between fields
        layout.addSpacing(8)
        
        # Password field with label
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-weight: bold; margin-bottom: 1px;")
        layout.addWidget(password_label)
        
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setPlaceholderText("Choose a password")
        self.register_password.returnPressed.connect(self.handle_register)
        layout.addWidget(self.register_password)
        
        # Spacing before button
        layout.addSpacing(12)
        
        # Register Button
        btn_register = QPushButton("Register")
        btn_register.setCursor(Qt.PointingHandCursor)
        btn_register.clicked.connect(self.handle_register)
        layout.addWidget(btn_register)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        try:
            self.user_data = self.api_client.login(username, password)
            QMessageBox.information(self, "Success", f"Welcome back, {self.user_data['user']['username']}!")
            self.accept()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code in [400, 401]:
                error_data = e.response.json()
                error_msg = error_data.get('error', 'Invalid credentials')
                QMessageBox.warning(self, "Login Failed", error_msg)
            else:
                QMessageBox.warning(self, "Error", f"Login failed: {e.response.status_code}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", 
                "Cannot connect to server. Please ensure:\n"
                "• Backend server is running on http://127.0.0.1:8000\n"
                "• Run: python manage.py runserver")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unexpected error: {str(e)}")
    
    def handle_register(self):
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            QMessageBox.warning(self, "Error", "Please enter a valid email address")
            return
        
        try:
            self.user_data = self.api_client.register(username, email, password)
            QMessageBox.information(self, "Success", f"Account created! Welcome, {username}!")
            self.accept()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 400:
                error_data = e.response.json()
                # Extract specific error messages
                if 'username' in error_data:
                    QMessageBox.warning(self, "Registration Failed", 
                        f"Username error: {error_data['username'][0]}")
                elif 'email' in error_data:
                    QMessageBox.warning(self, "Registration Failed", 
                        f"Email error: {error_data['email'][0]}")
                elif 'password' in error_data:
                    QMessageBox.warning(self, "Registration Failed", 
                        f"Password error: {error_data['password'][0]}")
                else:
                    error_msg = error_data.get('error', 'Registration failed. Please try again.')
                    QMessageBox.warning(self, "Registration Failed", error_msg)
            else:
                QMessageBox.warning(self, "Error", f"Server error: {e.response.status_code}")
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Connection Error", 
                "Cannot connect to server. Please ensure:\n"
                "• Backend server is running on http://127.0.0.1:8000\n"
                "• Run: python manage.py runserver")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Unexpected error: {str(e)}")
