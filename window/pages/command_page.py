from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from qfluentwidgets import GroupHeaderCardWidget, PrimaryPushButton, PushButton, LineEdit, InfoBar, InfoBarPosition, FluentIcon as FIF
from components.hx_command.basic_commands import create_basic_commands_section

class CommandPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10,10,10,10)
        self.main_layout.setSpacing(15)

        # 创建基础指令卡片
        self.basic_commands_card = create_basic_commands_section(self)
        self.main_layout.addWidget(self.basic_commands_card)

    # 以下是各个按钮的槽函数，目前为空，可根据实际需求实现具体逻辑
    def on_hexo_three_link_clicked(self):
        """hexo三连按钮点击事件"""
        InfoBar.success(
            title='Hexo三连',
            content="执行了 Hexo 三连操作。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_clear_cache_clicked(self):
        """清除缓存按钮点击事件"""
        InfoBar.info(
            title='清除缓存',
            content="缓存清除操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_generate_files_clicked(self):
        """生成文件按钮点击事件"""
        InfoBar.info(
            title='生成文件',
            content="文件生成操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_local_service_clicked(self):
        """本地服务按钮点击事件"""
        if self.service_edit.text():
            InfoBar.info(
                title='本地服务',
                content=f"服务端口: {self.service_edit.text()}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
        else:
            InfoBar.warning(
                title='本地服务',
                content="请输入服务地址",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

    def on_deploy_clicked(self):
        """部署按钮点击事件"""
        InfoBar.info(
            title='部署',
            content="部署操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_init_clicked(self):
        """初始化按钮点击事件"""
        InfoBar.info(
            title='初始化',
            content="初始化操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )