# settings_ui.py
from PySide6.QtWidgets import QVBoxLayout, QFileDialog
from qfluentwidgets import (
    ComboBoxSettingCard,
    HyperlinkCard,
    PushSettingCard,
    FluentIcon,
    SettingCardGroup,
    FluentStyleSheet,
    setTheme,
    Theme
)
import json
import os


def setup_ui(self):
    # 创建布局
    self.layout = QVBoxLayout(self)
    self.layout.setContentsMargins(30, 20, 30, 20)
    self.layout.setSpacing(15)

    # 创建设置卡片组
    self.setting_group = SettingCardGroup("常规设置", self)

    # 主题设置卡片
    self.theme_card = ComboBoxSettingCard(
        configItem=self.cfg.themeMode,
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
        content=self.cfg.downloadFolder.value,  # 使用正确的方式获取值
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

    # 将设置卡片组添加到布局
    self.layout.addWidget(self.setting_group)
    self.layout.addWidget(self.report_group)

    # 伸展布局，使组件居中显示
    self.layout.addStretch(1)

    # 应用 Fluent StyleSheet
    FluentStyleSheet.FLUENT_WINDOW.apply(self)

    # 读取 config.json 文件并设置初始主题
    config_path = "app/config/config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)
            theme_mode_str = config_data.get("QFluentWidgets", {}).get("ThemeMode", "LIGHT")
            if theme_mode_str.upper() == "DARK":
                initial_theme_index = 1
            elif theme_mode_str.upper() == "AUTO":
                initial_theme_index = 2
            else:
                initial_theme_index = 0
            self.theme_card.comboBox.setCurrentIndex(initial_theme_index)
            setTheme(self.cfg.themeMode.value)
