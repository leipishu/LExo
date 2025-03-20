from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import QDate, QTime
from qfluentwidgets import ScrollArea, PlainTextEdit, LineEdit, CardWidget, BodyLabel, DatePicker, TimePicker
import re
from datetime import datetime

class FrontmatterManager:
    def __init__(self):
        self.editor = PlainTextEdit()
        self.scroll_area = None
        self.is_visible = False
        self.title_label = BodyLabel("title")
        self.title_editor = LineEdit()
        self.date_label = BodyLabel("date")
        self.date_picker = DatePicker()
        self.time_picker = TimePicker(showSeconds=True)

    def create_editor_area(self, parent):
        # 创建 CardWidget 容器
        self.card_widget = CardWidget(parent)  # 将 CardWidget 添加到父部件中
        self.card_widget.setObjectName("frontmatterCard")  # 可选：设置对象名称以便后续样式定制
        self.card_widget.hide()

        # 创建 ScrollArea
        self.scroll_area = ScrollArea(self.card_widget)  # 将 ScrollArea 添加到 CardWidget 中
        self.scroll_area.setMinimumHeight(150)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color:transparent; border:none;")
        self.scroll_area.hide()

        # 创建容器和布局
        container = QWidget()
        layout = QVBoxLayout(container)

        # 创建水平布局用于标题和日期时间
        header_layout = QHBoxLayout()

        # 添加标题部分
        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_editor)
        header_layout.addLayout(title_layout, stretch=2)  # 标题部分占更大空间

        # 添加日期时间部分
        datetime_layout = QHBoxLayout()

        # 日期选择器
        date_layout = QHBoxLayout()
        date_layout.addWidget(self.date_label)
        date_layout.addWidget(self.date_picker)
        datetime_layout.addLayout(date_layout)

        # 时间选择器
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_picker)
        datetime_layout.addLayout(time_layout)

        header_layout.addLayout(datetime_layout, stretch=1)

        # 将标题和日期时间添加到主布局
        layout.addLayout(header_layout)

        # 其他 frontmatter 内容
        layout.addWidget(self.editor)

        self.scroll_area.setWidget(container)

        # 将 ScrollArea 添加到 CardWidget 的布局中
        card_layout = QHBoxLayout(self.card_widget)
        card_layout.addWidget(self.scroll_area)

        return self.card_widget  # 返回 CardWidget 作为编辑区域的最外层容器

    def set_content(self, frontmatter_without_title_and_date, title, date):
        # 设置 title
        self.title_editor.setText(title)
        # 设置 date 和 time
        if date:
            try:
                dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                self.date_picker.setDate(QDate(dt.year, dt.month, dt.day))
                self.time_picker.setTime(QTime(dt.hour, dt.minute, dt.second))
            except ValueError:
                pass
        # 设置 frontmatter 中除 title 和 date 之外的其他内容
        self.editor.setPlainText(frontmatter_without_title_and_date.strip())

    def clear_content(self):
        self.editor.setPlainText("")
        self.title_editor.setText("")
        self.date_picker.setDate(QDate.currentDate())
        self.time_picker.setTime(QTime.currentTime())

    def get_content(self):
        title = self.title_editor.text().strip()

        # 修改日期获取方式
        qdate = self.date_picker.getDate()
        date_str = qdate.toString("yyyy-MM-dd") if qdate.isValid() else ""

        # 修改时间获取方式
        qtime = self.time_picker.getTime()
        time_str = qtime.toString("HH:mm:ss") if qtime.isValid() else ""

        frontmatter = self.editor.toPlainText().strip()

        combined_frontmatter = []
        if title:
            combined_frontmatter.append(f"title: {title}")
        if date_str and time_str:
            combined_frontmatter.append(f"date: {date_str} {time_str}")
        if frontmatter:
            combined_frontmatter.append(frontmatter)

        return f"---\n{'\n'.join(combined_frontmatter)}\n---\n"

    def toggle_visibility(self, force=None):
        if force is not None:
            self.is_visible = force
        else:
            self.is_visible = not self.is_visible  # <--- 修改切换逻辑

        if self.scroll_area:
            self.scroll_area.setVisible(self.is_visible)

        # 额外控制 CardWidget 的可见性
        self.card_widget.setVisible(self.is_visible)