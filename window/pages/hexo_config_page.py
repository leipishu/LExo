from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QLabel, QPushButton, QDialog, QFormLayout, QHBoxLayout
from qfluentwidgets import CardWidget, PushButton, MessageBoxBase, LineEdit, MessageBox, SubtitleLabel, InfoBar, InfoBarPosition, InfoBarIcon

from utils.hx_config.search_function import search_yaml
from utils.hx_config.file_mgr import load_yaml, save_yaml
from components.hx_config.toolbar_builder import build_toolbar
from components.hx_config.content_builder import build_content_area, add_yaml_section
from ruamel.yaml import YAML


class CustomMessageBox(MessageBoxBase):
    """ Custom message box for adding YAML entries """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.key_edit = LineEdit()
        self.value_edit = LineEdit()

        self.key_edit.setPlaceholderText("输入键")
        self.key_edit.setClearButtonEnabled(True)
        self.value_edit.setPlaceholderText("输入值")
        self.value_edit.setClearButtonEnabled(True)

        self.viewLayout.addWidget(SubtitleLabel('添加自定义条目'))
        self.viewLayout.addWidget(self.key_edit)
        self.viewLayout.addWidget(self.value_edit)

        self.widget.setMinimumWidth(400)
        self.warningLabel = None  # 用于存储警告标签

    def validate(self):
        """ Validate the input data """
        if not self.key_edit.text().strip() or not self.value_edit.text().strip():
            # 检查是否已经存在警告标签
            if self.warningLabel is None:
                self.warningLabel = QLabel("键和值都不能为空")
                self.warningLabel.setStyleSheet("color: red")
                self.viewLayout.addWidget(self.warningLabel)
            else:
                # 如果已经存在，确保它可见
                self.warningLabel.setVisible(True)
            return False
        else:
            # 如果输入有效，隐藏警告标签（如果存在）
            if self.warningLabel is not None:
                self.warningLabel.setVisible(False)
        return True

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
         self.no_file_label, self.toolbar_card, self.toolbar_card_layout, self.add_entry_btn) = build_toolbar(self)
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
        self.add_entry_btn.clicked.connect(self.add_custom_entry)

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

        # 显示保存成功的消息条
        InfoBar.success(
            title='保存成功',
            content="YAML 文件已成功保存。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,  # 显示在右上角
            duration=2000,  # 2秒后自动消失
            parent=self
        )

    def add_custom_entry(self):
        """弹出对话框让用户添加自定义的 YAML 条目"""
        w = CustomMessageBox(self)
        if w.exec():
            key = w.key_edit.text().strip()
            value = w.value_edit.text().strip()

            if not key or not value:
                InfoBar.error(
                    title='输入错误',
                    content="键和值都不能为空",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=self
                )
                return

            if self.file_path:
                if key not in self.yaml_data:
                    self.yaml_data[key] = value
                    self.display_data[key] = value
                    add_yaml_section({key: value}, self.scroll_layout, self.display_data)
                    InfoBar.success(
                        title='添加成功',
                        content="条目已成功添加。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=2000,
                        parent=self
                    )
                else:
                    InfoBar.warning(
                        title='键已存在',
                        content="该键已存在于 YAML 文件中",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=2000,
                        parent=self
                    )
            else:
                InfoBar.info(
                    title='文件未加载',
                    content="请先加载一个 YAML 文件",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=self
                )

    def add_entry(self, dialog):
        """添加新的 YAML 条目"""
        key = self.key_edit.text().strip()
        value = self.value_edit.text().strip()

        if not key or not value:
            InfoBar.error(
                title='输入错误',
                content="键和值都不能为空",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
            return

        if self.file_path:
            if key not in self.yaml_data:
                self.yaml_data[key] = value
                self.display_data[key] = value
                add_yaml_section({key: value}, self.scroll_layout, self.display_data)
                InfoBar.success(
                    title='添加成功',
                    content="条目已成功添加。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=self
                )
            else:
                InfoBar.warning(
                    title='键已存在',
                    content="该键已存在于 YAML 文件中",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=self
                )
        else:
            InfoBar.info(
                title='文件未加载',
                content="请先加载一个 YAML 文件",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

        self.key_edit.clear()
        self.value_edit.clear()
        dialog.close()