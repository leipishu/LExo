from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QDialog, QFormLayout, QHBoxLayout
from qfluentwidgets import CardWidget, PushButton, MessageBoxBase, LineEdit, MessageBox, SubtitleLabel, InfoBar, InfoBarPosition, InfoBarIcon

from components.hx_config.toolbar_builder import build_toolbar
from components.hx_config.content_builder import build_content_area


class CommandPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(7)

        # 创建工具栏
        self.toolbar_card = CardWidget(self)
        self.toolbar_card_layout = QVBoxLayout(self.toolbar_card)
        self.toolbar_card_layout.setContentsMargins(0, 0, 0, 0)
        self.toolbar_card_layout.setSpacing(0)

        # 创建滚动区域
        self.scroll_card, self.scroll_card_layout, self.scroll_area, self.scroll_layout = build_content_area(self)

        # 组装界面
        self.main_layout.addWidget(self.toolbar_card)
        self.main_layout.addWidget(self.scroll_card)

        # 信号连接