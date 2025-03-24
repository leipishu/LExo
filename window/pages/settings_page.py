from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import OptionsSettingCard, HyperlinkCard, PushSettingCard, FluentIcon, SettingCardGroup, OptionsConfigItem, OptionsValidator

class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置页面")
        self.resize(800, 600)

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

        # 添加 HyperlinkCard
        self.help_card = HyperlinkCard(
            url="https://qfluentwidgets.com",
            text="打开帮助页面",
            icon=FluentIcon.HELP,
            title="帮助",
            content="发现 PyQt-Fluent-Widgets 的最佳实践"
        )
        self.setting_group.addSettingCard(self.help_card)

        self.feedback_card = HyperlinkCard(
            url="https://github.com/PyQt-Fluent-Widgets/PyQt-Fluent-Widgets/issues",
            text="提交反馈",
            icon=FluentIcon.FEEDBACK,
            title="反馈",
            content="帮助我们改进产品"
        )
        self.setting_group.addSettingCard(self.feedback_card)

        # 添加 PushSettingCard
        self.download_dir_card = PushSettingCard(
            text="选择文件夹",
            icon=FluentIcon.DOWNLOAD,
            title="下载目录",
            content="D:/Users/下载"
        )
        self.setting_group.addSettingCard(self.download_dir_card)

        # 将设置卡片组添加到布局
        self.layout.addWidget(self.setting_group)

        # 伸展布局，使组件居中显示
        self.layout.addStretch(1)