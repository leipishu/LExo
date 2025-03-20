from PySide6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QLabel, QLineEdit
from qfluentwidgets import ScrollArea, PlainTextEdit, LineEdit, CardWidget, BodyLabel # 导入 CardWidget
import re

class FrontmatterManager:
    def __init__(self):
        self.editor = PlainTextEdit()
        self.scroll_area = None
        self.is_visible = False
        self.title_label = BodyLabel("title")
        self.title_editor = LineEdit()
        self.date_label = BodyLabel("date")
        self.date_editor = LineEdit()

    def create_editor_area(self, parent):
        self.card_widget = CardWidget(parent)
        self.card_widget.setObjectName("frontmatterCard")
        self.card_widget.hide()

        self.scroll_area = ScrollArea(self.card_widget)
        self.scroll_area.setMinimumHeight(150)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color:transparent; border:none;")
        self.scroll_area.hide()

        container = QWidget()
        layout = QVBoxLayout(container)

        # 将 title 和 date 放置在同一行
        title_date_layout = QHBoxLayout()
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_editor)
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_editor)
        title_date_layout.addLayout(title_layout)
        title_date_layout.addLayout(date_layout)
        layout.addLayout(title_date_layout)

        layout.addWidget(self.editor)

        self.scroll_area.setWidget(container)

        card_layout = QVBoxLayout(self.card_widget)
        card_layout.addWidget(self.scroll_area)

        return self.card_widget

    def set_content(self, frontmatter_without_title_and_date, title, date):
        # 设置 title 和 date
        self.title_editor.setText(title)
        self.date_editor.setText(date)
        # 设置 frontmatter 中除 title 和 date 之外的其他内容
        self.editor.setPlainText(frontmatter_without_title_and_date.strip())

    def clear_content(self):
        self.editor.setPlainText("")
        self.title_editor.setText("")
        self.date_editor.setText("")

    def get_content(self):
        title = self.title_editor.text().strip()
        date = self.date_editor.text().strip()
        frontmatter = self.editor.toPlainText().strip()
        # 合并 title 和 date 以及其他 frontmatter 内容
        combined_frontmatter = []
        if title:
            combined_frontmatter.append(f"title: {title}")
        if date:
            combined_frontmatter.append(f"date: {date}")
        if frontmatter:
            combined_frontmatter.append(frontmatter)
        combined_frontmatter = "\n".join(combined_frontmatter)
        return f"{combined_frontmatter}\n"

    def toggle_visibility(self, force=None):
        if force is not None:
            self.is_visible = force
        else:
            self.is_visible = not self.is_visible  # <--- 修改切换逻辑

        if self.scroll_area:
            self.scroll_area.setVisible(self.is_visible)

        # 额外控制 CardWidget 的可见性
        self.card_widget.setVisible(self.is_visible)