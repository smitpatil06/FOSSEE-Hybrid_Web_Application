import sys
from PyQt5.QtWidgets import QApplication
from core.api_client import APIClient
from ui.views.login_window import LoginWindow
from ui.views.upload_window import UploadWindow

def main():
    # Force 'Fusion' style for better look on Linux/Windows
    QApplication.setStyle("Fusion")
    app = QApplication(sys.argv)
    
    # Initialize API client
    api_client = APIClient()
    
    # Show login window
    while True:
        login_window = LoginWindow(api_client)
        
        if login_window.exec_() == LoginWindow.Accepted:
            # Login successful, show main window
            user_data = login_window.user_data
            main_window = UploadWindow(api_client, user_data)
            main_window.show()
            
            # Run the app
            result = app.exec_()
            
            # Check if user logged out (main window closed)
            # If token is still set, user closed app, so exit
            if api_client.token:
                sys.exit(result)
            # Otherwise, user logged out, show login again
        else:
            # Login cancelled
            sys.exit(0)

if __name__ == '__main__':
    main()
