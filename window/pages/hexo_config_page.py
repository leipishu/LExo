from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from qfluentwidgets import PlainTextEdit, ScrollArea, PrimaryPushButton, SubtitleLabel
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
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # 样式设置
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.scroll_area.setStyleSheet("background: transparent;")

        # 组装界面
        self.main_layout.addLayout(self.toolbar)
        self.main_layout.addWidget(self.scroll_area)

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
            for section, content in self.yaml_data.items():
                # 创建区块容器
                section_widget = QWidget()
                section_layout = QVBoxLayout(section_widget)
                section_layout.setContentsMargins(0, 10, 0, 10)

                # 添加标题
                title_label = SubtitleLabel(section)
                title_label.setStyleSheet("padding-bottom: 8px; color: black;")
                section_layout.addWidget(title_label)

                # 添加文本编辑区
                text_edit = PlainTextEdit()
                text_edit.setPlainText(str(content))
                text_edit.setMinimumHeight(150)
                section_layout.addWidget(text_edit)

                self.scroll_layout.addWidget(section_widget)

        except Exception as e:
            print(f"Error loading YAML: {str(e)}")
