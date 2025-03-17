from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel
from qfluentwidgets import MessageBoxBase, LineEdit, SubtitleLabel, InfoBar, InfoBarPosition

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
