from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition, Theme, setTheme, PushButton, Action
from qfluentwidgets import FluentIcon as FIF

from window.pages.editor_page import MarkdownEditorPage
from window.pages.about_page import AboutPage
from window.pages.hexo_config_page import HexoConfigPage
from window.pages.command_page import CommandPage
from window.pages.settings_page import SettingsPage

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        # 创建编辑器页面
        self.editor_page = MarkdownEditorPage(self)
        self.about_page = AboutPage(self)
        self.config_page = HexoConfigPage(self)
        self.command_page = CommandPage(self)
        self.settings_page = SettingsPage(self)
        self.editor_page.setObjectName("MD_Editor")
        self.about_page.setObjectName("About")
        self.config_page.setObjectName("Config")
        self.command_page.setObjectName("Command")
        self.settings_page.setObjectName("Settings")

        # 初始化导航栏
        # self.setupTheme(Theme.LIGHT)
        self.initNavigation()

        # 窗口设置
        self.setWindowTitle("LExo")
        self.setWindowIcon(QIcon('./resources/img/App_Icon.png'))
        self.resize(1200, 800)

    def setupTheme(self, theme):
        """设置主题"""
        setTheme(theme)
        # 其他主题相关的设置代码...
    def initNavigation(self):
        # 正确使用图标参数（使用FIF枚举或图标路径）
        self.addSubInterface(
            interface=self.editor_page,
            icon=FIF.EDIT,  # 使用内置图标
            text="Markdown 编辑器",
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.config_page,
            icon=FIF.GLOBE,  # 使用内置图标
            text="Hexo 配置",
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.command_page,
            icon=FIF.COMMAND_PROMPT,  # 使用内置图标
            text="Hexo 命令",
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.about_page,
            icon=FIF.INFO,  # 使用内置图标
            text="关于",
            position=NavigationItemPosition.BOTTOM
        )
        self.addSubInterface(
            interface=self.settings_page,
            icon=FIF.SETTING,  # 使用内置图标
            text="设置",
            position=NavigationItemPosition.BOTTOM
        )