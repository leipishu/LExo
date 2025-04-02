from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QLabel, QPushButton, QDialog, QFormLayout, QHBoxLayout
from qfluentwidgets import CardWidget, PushButton, MessageBoxBase, LineEdit, MessageBox, SubtitleLabel, InfoBar, InfoBarPosition, InfoBarIcon

from utils.hx_config.search_function import search_yaml
from utils.hx_config.file_mgr import load_yaml, save_yaml
from components.hx_config.toolbar_builder import build_toolbar
from components.hx_config.content_builder import build_content_area, add_yaml_section
from components.hx_config.custon_msg_box import CustomMessageBox
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
        add_yaml_section(self.yaml_data, self.scroll_layout, self.display_data, None, self)

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
        add_yaml_section(self.yaml_data, self.scroll_layout, self.display_data, None, self)

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
                    add_yaml_section({key: value}, self.scroll_layout, self.display_data, None, self)
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

    def remove_entry(self, key):
        """删除指定键的条目"""
        if self.file_path:
            # 检查键是否存在
            if self._key_exists(key, self.yaml_data):
                # 创建MessageBox弹窗
                w = MessageBox(
                    title="确认删除",
                    content=f"确定要删除条目 '{key}' 吗？",
                    parent=self
                )
                w.yesButton.setText("删除")
                w.cancelButton.setText("取消")

                # 连接信号槽
                def confirm_delete():
                    # 删除键
                    self._delete_key(key, self.yaml_data)
                    # 从 display_data 中删除对应的键
                    if key in self.display_data:
                        del self.display_data[key]
                    # 刷新界面
                    self.clear_text_edits()
                    add_yaml_section(self.yaml_data, self.scroll_layout, self.display_data, None, self)
                    # 显示删除成功的消息
                    InfoBar.success(
                        title='删除成功',
                        content=f"条目 '{key}' 已成功删除。",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=2000,
                        parent=self
                    )

                w.yesButton.clicked.connect(confirm_delete)
                w.exec_()
            else:
                InfoBar.warning(
                    title='条目不存在',
                    content=f"条目 '{key}' 不存在。",
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
    def _key_exists(self, key, data):
        """检查键是否存在"""
        if '.' in key:
            parent_key, child_key = key.split('.', 1)
            if parent_key in data and isinstance(data[parent_key], dict):
                return self._key_exists(child_key, data[parent_key])
            return False
        return key in data

    def _delete_key(self, key, data):
        """递归删除键"""
        if '.' in key:
            parent_key, child_key = key.split('.', 1)
            if parent_key in data and isinstance(data[parent_key], dict):
                self._delete_key(child_key, data[parent_key])
                # 如果父键的字典变为空，也删除父键
                if not data[parent_key]:
                    del data[parent_key]
        else:
            if key in data:
                del data[key]
