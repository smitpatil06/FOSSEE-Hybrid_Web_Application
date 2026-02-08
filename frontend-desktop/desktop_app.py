import sys
from PyQt5.QtWidgets import QApplication
from core.api_client import APIClient
from ui.views.login_window import LoginWindow
from ui.views.upload_window import UploadWindow


def main():
    QApplication.setStyle("Fusion")
    app = QApplication(sys.argv)

    api_client = APIClient()

    while True:
        login_window = LoginWindow(api_client)

        if login_window.exec_() == LoginWindow.Accepted:
            user_data = login_window.user_data
            main_window = UploadWindow(api_client, user_data)
            main_window.show()

            result = app.exec_()
            if api_client.token:
                sys.exit(result)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
