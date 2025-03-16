from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from qfluentwidgets import CardWidget
from utils.hx_config.search_function import search_yaml
from utils.hx_config.file_mgr import load_yaml, save_yaml
from components.hx_config.toolbar_builder import build_toolbar
from components.hx_config.content_builder import build_content_area, add_yaml_section
from ruamel.yaml import YAML

class HexoConfigPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.yaml_data = {}
        self.display_data = {}  # 用于界面显示的数据副本
        self.file_path = None  # 记录文件路径
        self.is_file_loaded = False  # 标记是否已加载文件

        # 主布局
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(7)

        # 创建工具栏
        (self.toolbar, self.open_btn, self.save_btn, self.search_edit, 
         self.no_file_label, self.toolbar_card, self.toolbar_card_layout) = build_toolbar(self)
        self.toolbar_card_layout.addLayout(self.toolbar)

        # 创建滚动区域
        self.scroll_card, self.scroll_card_layout, self.scroll_area, self.scroll_layout = build_content_area(self)

        # 组装界面
        self.main_layout.addWidget(self.toolbar_card)
        self.main_layout.addWidget(self.scroll_card)
        self.scroll_card_layout.addWidget(self.no_file_label, 0, Qt.AlignCenter)
        self.scroll_card_layout.addWidget(self.scroll_area)

        # 信号连接
        self.open_btn.clicked.connect(self.load_yaml)
        self.search_edit.searchSignal.connect(self.search)
        self.search_edit.clearSignal.connect(self.clear_search)
        self.save_btn.clicked.connect(self.save_yaml)

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

        self.file_path = path  # 记录文件路径
        self.yaml_data = load_yaml(path)
        if self.yaml_data is None:
            return

        self.clear_text_edits()
        self.no_file_label.setVisible(False)  # 隐藏提示标签
        self.save_btn.setEnabled(True)  # 启用保存按钮

        # 动态创建带标题的编辑区
        add_yaml_section(self.yaml_data, self.scroll_layout, self.display_data)

    def search(self, text):
        """搜索功能"""
        search_yaml(self.yaml_data, text, self.scroll_layout)

    def clear_search(self):
        """清空搜索"""
        self.search_edit.clear()  # 清空搜索框
        # 清空现有内容并重新加载原始的 YAML 数据
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        self.no_file_label.setVisible(False)  # 隐藏提示标签
        add_yaml_section(self.yaml_data, self.scroll_layout, self.display_data)  # 重新加载原始的 YAML 数据

    def save_yaml(self):
        """保存YAML文件"""
        if not self.file_path:
            return

        with open(self.file_path, 'r', encoding='utf-8') as f:
            original_data = YAML().load(f)

        save_yaml(self.file_path, self.display_data, original_data)
