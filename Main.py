import sys
from PySide6 import QtWidgets
from src.dashboard import DashboardWindow
from data.creat_db import create_database


if __name__ == "__main__":
    create_database()
    app = QtWidgets.QApplication(sys.argv)
    dashboard_app = DashboardWindow()
    dashboard_app.show()
    sys.exit(app.exec())