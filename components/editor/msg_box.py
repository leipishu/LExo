from PySide6.QtWidgets import QHBoxLayout, QLabel
from qfluentwidgets import (
    LineEdit,
    BodyLabel,
    MessageBoxBase,
    MessageBox
)
from datetime import datetime

class AddMsgBox(MessageBoxBase):
    """自定义对话框，用于输入标签名称"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加标签")

        # 创建输入框
        self.tag_input = LineEdit()
        self.tag_input.setPlaceholderText("请输入标签名称")
        self.tag_input.setClearButtonEnabled(True)
        self.yesButton.setText("添加")
        self.cancelButton.setText("取消")

        # 创建布局
        self.viewLayout.addWidget(BodyLabel('添加新标签'))
        self.viewLayout.addWidget(self.tag_input)

        # 添加按钮布局
        button_layout = QHBoxLayout()
        self.viewLayout.addLayout(button_layout)

        # 设置对话框的最小宽度
        self.widget.setMinimumWidth(350)
        self.warningLabel = None  # 用于存储警告标签

    def validate(self):
        """ Validate the input data """
        tag_name = self.tag_input.text().strip()
        if not tag_name:
            # 检查是否已经存在警告标签
            if self.warningLabel is None:
                self.warningLabel = QLabel("标签名称不能为空")
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

    def exec(self):
        """执行对话框并验证输入"""
        super().exec()
        return self.tag_input.text().strip() if self.validate() else None

class DeleteMsgBox(MessageBox):
    """自定义对话框，用于确认删除标签"""
    def __init__(self, tag_name, parent=None):
        super().__init__(
            title="删除标签",
            content=f"确定要删除标签 '{tag_name}' 吗？",
            parent=parent
        )
        self.tag_name = tag_name

        # 修改按钮文本
        self.yesButton.setText("删除")
        self.cancelButton.setText("取消")