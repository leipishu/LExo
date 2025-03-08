from qfluentwidgets import (
    Action, CommandBar, PrimaryPushButton, FluentIcon as FIF,
    TransparentPushButton, RoundMenu, PrimaryDropDownPushButton
)
from PySide6.QtWidgets import QHBoxLayout

class ToolbarManager:
    def create_toolbar(self):
        self.toolbar = CommandBar(self)

        # 文件操作按钮
        self.open_btn = PrimaryPushButton(FIF.FOLDER, "打开")
        self.save_btn = PrimaryDropDownPushButton(FIF.SAVE, "保存")

        # 编辑操作
        self.undo_btn = Action(FIF.LEFT_ARROW, "撤销")
        self.redo_btn = Action(FIF.RIGHT_ARROW, "重做")

        # 视图操作
        self.show_frame_btn = Action(FIF.VIEW, "显示面板")

        # 保存菜单
        self.save_menu = RoundMenu(parent=self.save_btn)
        self.save_as_action = Action(FIF.SAVE_AS, "另存为")
        self.save_copy_action = Action(FIF.SAVE_COPY, "保存并复制")

        return self.toolbar

    def create_format_toolbar(self):
        self.text_format_toolbar = QHBoxLayout()
        self.bold_btn = TransparentPushButton("加粗")
        self.highlight_btn = TransparentPushButton("高亮")
        self.italic_btn = TransparentPushButton("斜体")
        return self.text_format_toolbar

    def setup_toolbar_layout(self):
        self.save_menu.addActions([self.save_as_action, self.save_copy_action])
        self.save_btn.setMenu(self.save_menu)

        self.toolbar.addWidget(self.save_btn)
        self.toolbar.addWidget(self.open_btn)
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.undo_btn, self.redo_btn])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.show_frame_btn)

        self.text_format_toolbar.addWidget(self.bold_btn)
        self.text_format_toolbar.addWidget(self.italic_btn)
        self.text_format_toolbar.addWidget(self.highlight_btn)
        self.text_format_toolbar.addStretch(1)
