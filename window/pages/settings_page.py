from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from qfluentwidgets import (
    ComboBoxSettingCard,
    HyperlinkCard,
    PushSettingCard,
    FluentIcon,
    SettingCardGroup,
    OptionsConfigItem,
    OptionsValidator,
    qconfig,
    QConfig,
    Theme,
    setTheme,
    FluentStyleSheet,
    ConfigItem,
)

# 定义配置类
class Config(QConfig):
    # 主题模式配置项
    themeMode = OptionsConfigItem(
        group="MainWindow",
        name="ThemeMode",
        default=Theme.LIGHT,
        validator=OptionsValidator([Theme.LIGHT, Theme.DARK, Theme.AUTO]),
        restart=True,
    )
    # 下载目录配置项
    downloadFolder = ConfigItem(
        group="Paths",
        name="DownloadFolder",
        default="D:/Users/下载",
    )
    def toDict(self):
        cfg_dict = super().toDict()
        # 将 Theme 枚举类型转换为字符串
        if "MainWindow" in cfg_dict and "ThemeMode" in cfg_dict["MainWindow"]:
            theme_value = cfg_dict["MainWindow"]["ThemeMode"]
            if isinstance(theme_value, Theme):
                cfg_dict["MainWindow"]["ThemeMode"] = theme_value.name
        return cfg_dict

    @classmethod
    def fromDict(cls, cfg_dict):
        config = cls()
        # 将字符串转换回 Theme 枚举类型
        if "MainWindow" in cfg_dict and "ThemeMode" in cfg_dict["MainWindow"]:
            theme_mode = cfg_dict["MainWindow"]["ThemeMode"]
            if isinstance(theme_mode, str):
                cfg_dict["MainWindow"]["ThemeMode"] = Theme[theme_mode]
        super().fromDict(cfg_dict)
        return config

cfg = Config()
qconfig.load("app/config/config.json", cfg)


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建布局
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 20, 30, 20)
        self.layout.setSpacing(15)

        # 创建设置卡片组
        self.setting_group = SettingCardGroup("常规设置", self)

        # 主题设置卡片
        self.theme_card = ComboBoxSettingCard(
            configItem=cfg.themeMode,
            icon=FluentIcon.BRUSH,
            title="应用主题",
            content="调整你的应用外观",
            texts=["Light", "Dark", "Auto"],  # 保持与 validator 的选项一致
        )
        self.setting_group.addSettingCard(self.theme_card)

        # 文件夹选择卡片
        self.download_dir_card = PushSettingCard(
            text="选择文件夹",
            icon=FluentIcon.DOWNLOAD,
            title="下载目录",
            content=cfg.downloadFolder.value,  # 使用正确的方式获取值
        )
        self.setting_group.addSettingCard(self.download_dir_card)

        # 关于与反馈卡片组
        self.report_group = SettingCardGroup("关于与反馈", self)

        # 帮助卡片
        self.help_card = HyperlinkCard(
            url="https://www.leipishu.top/",
            text="打开帮助页面",
            icon=FluentIcon.HELP,
            title="帮助(暂未完成)",
            content="发现 LExo 的最佳实践",
        )
        self.report_group.addSettingCard(self.help_card)

        # BUG反馈卡片
        self.issue_card = HyperlinkCard(
            url="https://github.com/leipishu/LExo/issues",
            text="提交ISSUES",
            icon=FluentIcon.FEEDBACK,
            title="BUG反馈",
            content="帮助我们修复BUG",
        )
        self.report_group.addSettingCard(self.issue_card)

        # 贡献代码卡片
        self.pr_card = HyperlinkCard(
            url="https://github.com/leipishu/LExo/pulls",
            text="提交PR",
            icon=FluentIcon.CODE,
            title="贡献代码",
            content="帮助我们改进软件",
        )
        self.report_group.addSettingCard(self.pr_card)

        # 绑定信号槽
        self.theme_card.comboBox.currentIndexChanged.connect(self.on_theme_changed)
        self.download_dir_card.clicked.connect(self.on_download_dir_clicked)

        # 将设置卡片组添加到布局
        self.layout.addWidget(self.setting_group)
        self.layout.addWidget(self.report_group)

        # 伸展布局，使组件居中显示
        self.layout.addStretch(1)

        # 应用 Fluent StyleSheet
        FluentStyleSheet.FLUENT_WINDOW.apply(self)

    def on_theme_changed(self, index):
        """主题切换槽函数"""
        # 获取当前选中的主题字符串
        theme = self.theme_card.comboBox.itemText(index)

        # 更新配置
        cfg.themeMode.value = Theme[theme.upper()]

        # 应用主题
        if theme == "Light":
            setTheme(Theme.LIGHT)
        elif theme == "Dark":
            setTheme(Theme.DARK)
        else:  # 跟随系统设置
            setTheme(Theme.AUTO)

        # 保存配置
        qconfig.save()

    def on_download_dir_clicked(self):
        """下载目录按钮点击槽函数"""
        # 弹出文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(
            self, "选择下载目录", cfg.downloadFolder.value  # 使用正确的方式获取值
        )

        if folder:
            # 更新配置
            cfg.downloadFolder.value = folder

            # 更新卡片内容
            self.download_dir_card.setContent(folder)

            # 保存配置
            qconfig.save()
