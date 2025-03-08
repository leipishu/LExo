# main.py 保持不变
import sys
from PySide6.QtWidgets import QApplication
from window.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
