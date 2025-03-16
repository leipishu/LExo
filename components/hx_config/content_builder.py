# components/hx_config/content_builder.py

from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import PlainTextEdit, ScrollArea, CardWidget, SubtitleLabel, SwitchButton

def build_content_area(parent):
    scroll_card = CardWidget(parent)
    scroll_card_layout = QVBoxLayout(scroll_card)
    scroll_card_layout.setContentsMargins(10, 10, 10, 10)

    scroll_area = ScrollArea(parent)
    scroll_widget = QWidget(parent)
    scroll_layout = QVBoxLayout(scroll_widget)  # 将 scroll_layout 定义为类的属性
    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)

    scroll_widget.setStyleSheet("background: transparent;")
    scroll_area.setStyleSheet("background: transparent;")

    return scroll_card, scroll_card_layout, scroll_area, scroll_layout

def add_yaml_section(data, parent_layout, display_data, parent_key=None):
    """递归添加YAML部分"""
    for section, content in data.items():
        full_key = f"{parent_key}.{section}" if parent_key else section

        # 创建卡片作为最外层容器
        card = CardWidget()
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)

        # 添加标题
        title_label = SubtitleLabel(section)
        title_label.setStyleSheet("padding-bottom: 8px; color: black;")
        card_layout.addWidget(title_label)

        if isinstance(content, dict):
            # 如果内容是字典，创建新的布局递归添加
            inner_layout = QVBoxLayout()
            card_layout.addLayout(inner_layout)
            add_yaml_section(content, inner_layout, display_data, full_key)
        elif isinstance(content, bool):
            # 如果内容是布尔值，使用 SwitchButton
            switch_button = SwitchButton()
            switch_button.setOnText("True")
            switch_button.setOffText("False")
            switch_button.setChecked(content)
            card_layout.addWidget(switch_button)
            # 保存关联
            display_data[full_key] = switch_button
        else:
            # 添加文本编辑区
            text_edit = PlainTextEdit()
            text_edit.setPlainText(str(content))
            text_edit.setMinimumHeight(150)
            card_layout.addWidget(text_edit)
            # 保存关联
            display_data[full_key] = text_edit

        # 将卡片添加到父布局
        parent_layout.addWidget(card)