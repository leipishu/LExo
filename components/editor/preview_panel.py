from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from qfluentwidgets import ScrollArea

class PreviewPanel:
    def create_preview_area(self):
        self.right_scroll = ScrollArea()
        self.right_scroll.setObjectName("RightPanel")
        self.preview = QTextBrowser()
        self.preview.setOpenExternalLinks(True)
        self.preview.setMinimumWidth(200)

        # 样式设置
        self.right_scroll.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border-left: 1px solid #eeeeee;
                border-radius: 5px;
            }
            QScrollBar:vertical {
                background: #f5f5f5;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #cccccc;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
        """)

        self.preview.setStyleSheet("""
            QTextBrowser {
                background-color: white;
                border-radius: 5px;
                color: black;
                border: none;
                padding: 10px;
            }
        """)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.addWidget(self.preview)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content.setStyleSheet("background-color: transparent;")

        self.right_scroll.setWidget(content)
        self.right_scroll.setWidgetResizable(True)
        return self.right_scroll
