from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import OptionsSettingCard, HyperlinkCard, PushSettingCard, FluentIcon, SettingCardGroup, OptionsConfigItem, OptionsValidator

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 20, 30, 20)
        self.layout.setSpacing(15)

        # 创建设置卡片组
        self.setting_group = SettingCardGroup("常规设置", self)

        # 创建一个 OptionsConfigItem 类型的配置项
        self.theme_config = OptionsConfigItem(
            group="MainWindow",
            name="ThemeMode",
            default="Light",
            validator=OptionsValidator(["Light", "Dark", "Auto"]),
            restart=True
        )

        # 添加 OptionsSettingCard
        self.theme_card = OptionsSettingCard(
            configItem=self.theme_config,  # 使用 OptionsConfigItem 类型的配置项
            icon=FluentIcon.BRUSH,
            title="应用主题",
            content="调整你的应用外观",
            texts=["浅色", "深色", "跟随系统设置"]
        )
        self.setting_group.addSettingCard(self.theme_card)

        # 添加 PushSettingCard
        self.download_dir_card = PushSettingCard(
            text="选择文件夹",
            icon=FluentIcon.DOWNLOAD,
            title="下载目录",
            content="D:/Users/下载"
        )
        self.setting_group.addSettingCard(self.download_dir_card)

        self.report_group = SettingCardGroup("关于与反馈", self)

        # 添加 HyperlinkCard
        self.help_card = HyperlinkCard(
            url="https://www.leipishu.top/",
            text="打开帮助页面",
            icon=FluentIcon.HELP,
            title="帮助(暂未完成)",
            content="发现 LExo 的最佳实践"
        )
        self.report_group.addSettingCard(self.help_card)

        self.issue_card = HyperlinkCard(
            url="https://github.com/leipishu/LExo/issues",
            text="提交ISSUES",
            icon=FluentIcon.FEEDBACK,
            title="BUG反馈",
            content="帮助我们修复BUG"
        )
        self.report_group.addSettingCard(self.issue_card)

        self.pr_card = HyperlinkCard(
            url="https://github.com/leipishu/LExo/pulls",
            text="提交PR",
            icon=FluentIcon.CODE,
            title="贡献代码",
            content="帮助我们改进软件"
        )
        self.report_group.addSettingCard(self.pr_card)

        # 将设置卡片组添加到布局
        self.layout.addWidget(self.setting_group)
        self.layout.addWidget(self.report_group)

        # 伸展布局，使组件居中显示
        self.layout.addStretch(1)