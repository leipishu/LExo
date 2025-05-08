from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from qfluentwidgets import FluentWindow, NavigationItemPosition, Theme, setTheme, PushButton, Action
from qfluentwidgets import FluentIcon as FIF

from window.pages.editor_page import MarkdownEditorPage
from window.pages.hexo_config_page import HexoConfigPage
from window.pages.command_page import CommandPage
from window.pages.settings_page import SettingsPage
from window.pages.blog_mgr_page import BlogMgrPage

class MainWindow(FluentWindow):
    def __init__(self):
        super().__init__()

        # 创建编辑器页面
        self.editor_page = MarkdownEditorPage(self)
        self.config_page = HexoConfigPage(self)
        self.command_page = CommandPage(self)
        self.settings_page = SettingsPage(self)
        self.blog_mgr_page = BlogMgrPage(self)
        self.editor_page.setObjectName("MD_Editor")
        self.config_page.setObjectName("Config")
        self.command_page.setObjectName("Command")
        self.settings_page.setObjectName("Settings")
        self.blog_mgr_page.setObjectName("Blog")

        # 初始化导航栏
        self.initNavigation()

        # 窗口设置
        self.setWindowTitle("LExo")
        self.setWindowIcon(QIcon('./resources/img/App_Icon.png'))
        self.resize(1300,900)

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
            interface=self.blog_mgr_page,
            icon=FIF.DOCUMENT,  # 使用内置图标
            text="博客管理",
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.command_page,
            icon=FIF.COMMAND_PROMPT,  # 使用内置图标
            text="Hexo 命令",
            position=NavigationItemPosition.TOP
        )

        self.addSubInterface(
            interface=self.settings_page,
            icon=FIF.SETTING,  # 使用内置图标
            text="设置",
            position=NavigationItemPosition.BOTTOM
        )