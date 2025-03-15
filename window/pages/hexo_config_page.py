from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from qfluentwidgets import PlainTextEdit, ScrollArea, PrimaryPushButton, SubtitleLabel, CardWidget, SwitchButton
from pathlib import Path
import yaml

class HexoConfigPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.yaml_data = {}
        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 顶部工具栏
        self.toolbar = QHBoxLayout()
        self.open_btn = PrimaryPushButton("打开", self)
        self.toolbar.addWidget(self.open_btn)
        self.toolbar.addStretch()

        # 滚动区域
        self.scroll_area = ScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)  # 将 scroll_layout 定义为类的属性
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # 样式设置
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.scroll_area.setStyleSheet("background: transparent;")

        # 创建卡片包裹滚动区域
        scroll_card = CardWidget(self)
        scroll_card_layout = QVBoxLayout(scroll_card)
        scroll_card_layout.addWidget(self.scroll_area)

        # 组装界面
        self.main_layout.addLayout(self.toolbar)
        self.main_layout.addWidget(scroll_card)

        # 信号连接
        self.open_btn.clicked.connect(self.load_yaml)

    def clear_text_edits(self):
        """清空现有内容"""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_yaml(self):
        """加载YAML文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "打开YAML文件", "", "YAML Files (*.yml *.yaml)")
        if not path:
            return

        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.yaml_data = yaml.safe_load(f) or {}

            self.clear_text_edits()

            # 动态创建带标题的编辑区
            self.add_yaml_section(self.yaml_data, self.scroll_layout)

        except Exception as e:
            print(f"Error loading YAML: {str(e)}")

    def add_yaml_section(self, data, parent_layout):
        """递归添加YAML部分"""
        for section, content in data.items():
            # 创建卡片作为最外层容器
            card = CardWidget(self)
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
                self.add_yaml_section(content, inner_layout)
            elif isinstance(content, bool):
                # 如果内容是布尔值，使用 SwitchButton
                switch_button = SwitchButton(self)
                switch_button.setOnText(str(True))
                switch_button.setOffText(str(False))
                switch_button.setChecked(content)
                card_layout.addWidget(switch_button)
            else:
                # 添加文本编辑区
                text_edit = PlainTextEdit()
                text_edit.setPlainText(str(content))
                text_edit.setMinimumHeight(150)
                card_layout.addWidget(text_edit)

            # 将卡片添加到父布局
            parent_layout.addWidget(card)
