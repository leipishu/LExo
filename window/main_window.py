from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition
from qfluentwidgets import FluentIcon as FIF

from window.pages.editor_page import MarkdownEditorPage
from window.pages.about_page import AboutPage
from window.pages.config_page import ConfigPage

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        # 创建编辑器页面
        self.editor_page = MarkdownEditorPage(self)
        self.about_page = AboutPage(self)
        self.config_page = ConfigPage(self)
        self.editor_page.setObjectName("MD_Editor")
        self.about_page.setObjectName("About")
        self.config_page.setObjectName("Config")

        # 初始化导航栏
        self.initNavigation()

        # 窗口设置
        self.setWindowTitle("LExo")
        self.setWindowIcon(QIcon('./resources/img/App_Icon.png'))
        self.resize(1200, 800)

    def initNavigation(self):
        # 正确使用图标参数（使用FIF枚举或图标路径）
        self.addSubInterface(
            interface=self.editor_page,
            icon=FIF.EDIT,  # 使用内置图标
            text="Markdown 编辑器",
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.about_page,
            icon=FIF.INFO,  # 使用内置图标
            text="关于",
            position=NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(
            interface=self.config_page,
            icon=FIF.GLOBE,  # 使用内置图标
            text="Hexo配置",
            position=NavigationItemPosition.TOP
        )
