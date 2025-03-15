from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from qfluentwidgets import PlainTextEdit, ScrollArea, PrimaryPushButton, SubtitleLabel, CardWidget, SwitchButton, SearchLineEdit
import yaml
from ruamel.yaml import YAML
from utils.hx_config.search_function import search_yaml

class HexoConfigPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.yaml_data = {}
        self.display_data = {}  # 用于界面显示的数据副本
        self.file_path = None  # 记录文件路径
        self.is_file_loaded = False  # 标记是否已加载文件

        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 创建提示标签（未加载文件时显示）
        self.no_file_label = QLabel("未加载YAML文件，请点击'打开'按钮选择文件")
        self.no_file_label.setStyleSheet("color: #666666;")
        self.no_file_label.setVisible(True)

        # 创建工具栏CardWidget
        self.toolbar_card = CardWidget(self)
        self.toolbar_card_layout = QVBoxLayout(self.toolbar_card)
        self.toolbar_card_layout.setContentsMargins(15, 15, 15, 15)

        # 创建搜索栏
        self.search_edit = SearchLineEdit(self)
        self.search_edit.setPlaceholderText("搜索...")
        self.search_edit.searchSignal.connect(self.search)
        self.search_edit.clearSignal.connect(self.clear_search)
        self.search_edit.setFixedWidth(200)  # 设置搜索栏宽度

        # 创建保存按钮
        self.save_btn = PrimaryPushButton("保存", self)
        self.save_btn.clicked.connect(self.save_yaml)
        self.save_btn.setEnabled(False)  # 默认禁用保存按钮

        # 创建工具栏
        self.toolbar = QHBoxLayout()
        self.open_btn = PrimaryPushButton("打开", self)
        self.toolbar.addWidget(self.open_btn)
        self.toolbar.addWidget(self.save_btn)  # 添加保存按钮到工具栏
        self.toolbar.addWidget(self.search_edit)  # 添加搜索栏到工具栏
        self.toolbar.addStretch()

        # 添加工具栏到工具栏CardWidget
        self.toolbar_card_layout.addLayout(self.toolbar)

        # 创建滚动区域外层的CardWidget
        self.scroll_card = CardWidget(self)
        self.scroll_card_layout = QVBoxLayout(self.scroll_card)
        self.scroll_card_layout.setContentsMargins(15, 15, 15, 15)

        # 创建滚动区域
        self.scroll_area = ScrollArea(self)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)  # 将 scroll_layout 定义为类的属性
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # 样式设置
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.scroll_area.setStyleSheet("background: transparent;")

        # 组装界面
        self.main_layout.addWidget(self.toolbar_card)
        self.main_layout.addWidget(self.scroll_card)
        self.scroll_card_layout.addWidget(self.no_file_label, 0, Qt.AlignCenter)
        self.scroll_card_layout.addWidget(self.scroll_area)

        # 信号连接
        self.open_btn.clicked.connect(self.load_yaml)

    def clear_text_edits(self):
        """清空现有内容"""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.no_file_label.setVisible(True)  # 重新显示提示标签
        self.save_btn.setEnabled(False)  # 禁用保存按钮

    def load_yaml(self):
        """加载YAML文件"""
        path, _ = QFileDialog.getOpenFileName(
            self, "打开YAML文件", "", "YAML Files (*.yml *.yaml)")
        if not path:
            return

        try:
            self.file_path = path  # 记录文件路径
            with open(path, 'r', encoding='utf-8') as f:
                self.yaml_data = yaml.safe_load(f) or {}
                self.display_data = {}  # 清空显示数据副本

            self.clear_text_edits()
            self.no_file_label.setVisible(False)  # 隐藏提示标签
            self.save_btn.setEnabled(True)  # 启用保存按钮

            # 动态创建带标题的编辑区
            self.add_yaml_section(self.yaml_data, self.scroll_layout, self.display_data)

        except Exception as e:
            print(f"Error loading YAML: {str(e)}")

    def add_yaml_section(self, data, parent_layout, display_data, parent_key=None):
        """递归添加YAML部分"""
        for section, content in data.items():
            full_key = f"{parent_key}.{section}" if parent_key else section

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
                self.add_yaml_section(content, inner_layout, display_data, full_key)
            elif isinstance(content, bool):
                # 如果内容是布尔值，使用 SwitchButton
                switch_button = SwitchButton(self)
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

    def search(self, text):
        """搜索功能"""
        search_yaml(self.yaml_data, text, self.scroll_layout)

    def clear_search(self):
        """清空搜索"""
        self.search_edit.clear()  # 清空搜索框
        self.clear_text_edits()  # 清空现有内容
        self.add_yaml_section(self.yaml_data, self.scroll_layout, self.display_data)  # 重新加载原始的 YAML 数据

    def save_yaml(self):
        """保存YAML文件"""
        if not self.file_path:
            return

        try:
            # 使用 ruamel.yaml 加载原始文件以保留格式和注释
            yaml = YAML()
            yaml.preserve_quotes = True
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.width = 4096  # 防止长行被拆分

            with open(self.file_path, 'r', encoding='utf-8') as f:
                original_data = yaml.load(f)

            # 提取界面中的数据
            self.extract_yaml_data(self.display_data, self.yaml_data)

            # 更新原始数据
            self.update_data(original_data, self.yaml_data)

            # 保存更新后的数据到原始文件
            with open(self.file_path, 'w', encoding='utf-8') as f:
                yaml.dump(original_data, f)

        except Exception as e:
            print(f"Error saving YAML: {str(e)}")

    def update_data(self, original_data, new_data):
        """递归更新原始数据以保持格式"""
        for key, value in new_data.items():
            if key in original_data:
                if isinstance(value, dict) and isinstance(original_data[key], dict):
                    self.update_data(original_data[key], value)
                else:
                    original_data[key] = value
            else:
                original_data[key] = value

    def extract_yaml_data(self, display_data, yaml_data):
        """从界面元素中提取数据"""
        for key, widget in display_data.items():
            keys = key.split('.')
            temp_dict = yaml_data
            for sub_key in keys[:-1]:
                if sub_key not in temp_dict:
                    temp_dict[sub_key] = {}
                temp_dict = temp_dict[sub_key]
            if isinstance(widget, SwitchButton):
                temp_dict[keys[-1]] = widget.isChecked()
            elif isinstance(widget, PlainTextEdit):
                temp_dict[keys[-1]] = widget.toPlainText()