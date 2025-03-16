# components/hx_config/toolbar_builder.py

from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QFileDialog, QLabel
from qfluentwidgets import PrimaryPushButton, SearchLineEdit, CardWidget, PushButton
from qfluentwidgets import FluentIcon as FIF

def build_toolbar(parent):
    toolbar_card = CardWidget(parent)
    toolbar_card_layout = QVBoxLayout(toolbar_card)
    toolbar_card_layout.setContentsMargins(10, 10, 10, 10)

    search_edit = SearchLineEdit(parent)
    search_edit.setPlaceholderText("搜索...")
    search_edit.setFixedWidth(200)  # 设置搜索栏宽度

    save_btn = PrimaryPushButton(FIF.SAVE, "保存", parent)
    save_btn.setEnabled(False)  # 默认禁用保存按钮

    toolbar = QHBoxLayout()
    open_btn = PrimaryPushButton(FIF.FOLDER, "打开", parent)
    add_entry_btn = PushButton(FIF.ADD, "添加条目", parent)
    toolbar.addWidget(open_btn)
    toolbar.addWidget(save_btn)  # 添加保存按钮到工具栏
    toolbar.addWidget(add_entry_btn)
    toolbar.addWidget(search_edit)  # 添加搜索栏到工具栏
    toolbar.addStretch()

    no_file_label = QLabel("未加载YAML文件，请点击'打开'按钮选择文件", parent)
    no_file_label.setStyleSheet("color: #666666;")
    no_file_label.setVisible(True)

    return toolbar, open_btn, save_btn, search_edit, no_file_label, toolbar_card, toolbar_card_layout, add_entry_btn