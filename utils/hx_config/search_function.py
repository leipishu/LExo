from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import CardWidget, SubtitleLabel, PlainTextEdit, SwitchButton
import yaml

def search_yaml(data, text, parent_layout):
    def clear_layout(layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_section(section, content, layout):
        # 创建卡片作为最外层容器
        card = CardWidget(parent_layout.parent())
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)

        # 添加标题
        title_label = SubtitleLabel(section)
        title_label.setStyleSheet("padding-bottom: 8px; color: black;")
        card_layout.addWidget(title_label)

        if isinstance(content, dict):
            # 如果内容是字典，创建新的布局递归添加
            inner_layout = QVBoxLayout()
            card_layout.addLayout(inner_layout)
            add_section_recursive(content, inner_layout)
        elif isinstance(content, bool):
            # 如果内容是布尔值，使用 SwitchButton
            switch_button = SwitchButton(parent_layout.parent())
            switch_button.setOnText("True")
            switch_button.setOffText("False")
            switch_button.setChecked(content)
            card_layout.addWidget(switch_button)
        else:
            # 添加文本编辑区
            text_edit = PlainTextEdit(parent_layout.parent())
            text_edit.setPlainText(str(content))
            text_edit.setMinimumHeight(150)
            card_layout.addWidget(text_edit)

        # 将卡片添加到父布局
        layout.addWidget(card)

    def add_section_recursive(data, layout):
        for section, content in data.items():
            if search_text_in_data(section, content, text):
                add_section(section, content, layout)

    def search_text_in_data(section, content, text):
        if text.lower() in section.lower():
            return True
        if isinstance(content, dict):
            for sub_section, sub_content in content.items():
                if search_text_in_data(sub_section, sub_content, text):
                    return True
        elif isinstance(content, str):
            if text.lower() in content.lower():
                return True
        elif isinstance(content, bool):
            if text.lower() in str(content).lower():
                return True
        return False

    clear_layout(parent_layout)
    add_section_recursive(data, parent_layout)
