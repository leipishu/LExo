from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QPoint
from window.main_window import MainWindow
import sys
import os


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    # 计算屏幕中心点
    screen_geometry = app.primaryScreen().geometry()
    screen_width = screen_geometry.width()
    screen_height = screen_geometry.height()

    # 计算窗口的左上角位置
    window_width = window.width()
    window_height = window.height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # 将窗口移动到计算的位置
    window.move(QPoint(x, y))

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()