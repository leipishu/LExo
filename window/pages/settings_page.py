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
import json
import os
from components.app_settings import settings_ui


# 定义配置类
class Config(QConfig):
    # 主题模式配置项
    themeMode = OptionsConfigItem(
        group="QFluentWidgets",  # 修改组为 QFluentWidgets
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
        if "QFluentWidgets" in cfg_dict and "ThemeMode" in cfg_dict["QFluentWidgets"]:
            theme_value = cfg_dict["QFluentWidgets"]["ThemeMode"]
            if isinstance(theme_value, Theme):
                cfg_dict["QFluentWidgets"]["ThemeMode"] = theme_value.name
        return cfg_dict

    @classmethod
    def fromDict(cls, cfg_dict):
        config = cls()
        # 将字符串转换回 Theme 枚举类型
        if "QFluentWidgets" in cfg_dict and "ThemeMode" in cfg_dict["QFluentWidgets"]:
            theme_mode = cfg_dict["QFluentWidgets"]["ThemeMode"]
            if isinstance(theme_mode, str):
                cfg_dict["QFluentWidgets"]["ThemeMode"] = Theme[theme_mode]
        super().fromDict(cfg_dict)
        return config


cfg = Config()
qconfig.load("app/config/config.json", cfg)


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = cfg  # 将配置对象传递给实例变量

        # 调用独立的 UI 构建函数
        settings_ui.setup_ui(self)

        # 绑定信号槽
        self.theme_card.comboBox.currentIndexChanged.connect(self.on_theme_changed)
        self.download_dir_card.clicked.connect(self.on_download_dir_clicked)

    def on_theme_changed(self, index):
        """主题切换槽函数"""
        # 获取当前选中的主题字符串
        theme_text = self.theme_card.comboBox.itemText(index)
        theme = settings_ui.theme_text_to_enum(theme_text)  # 使用映射函数

        # 更新配置
        self.cfg.themeMode.value = theme

        # 应用主题
        setTheme(theme)

        # 保存配置
        qconfig.save()

    def on_download_dir_clicked(self):
        """下载目录按钮点击槽函数"""
        # 弹出文件夹选择对话框
        folder = QFileDialog.getExistingDirectory(
            self, "选择下载目录", self.cfg.downloadFolder.value  # 使用正确的方式获取值
        )

        if folder:
            # 更新配置
            self.cfg.downloadFolder.value = folder

            # 更新卡片内容
            self.download_dir_card.setContent(folder)

            # 保存配置
            qconfig.save()
