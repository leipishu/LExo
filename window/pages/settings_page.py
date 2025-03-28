from PySide6.QtWidgets import QWidget,QFileDialog
from qfluentwidgets import (
    qconfig,
    Theme,
    setTheme,
)
from components.app_settings import settings_ui
from utils.app_settings.config import cfg


# 定义配置类
# 定义配置类
class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cfg = cfg

        # 调用独立的 UI 构建函数
        settings_ui.setup_ui(self)

        # 绑定信号槽
        self.theme_card.comboBox.currentIndexChanged.connect(self.on_theme_changed)
        self.download_dir_card.clicked.connect(self.on_download_dir_clicked)

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

            self.download_dir_card.setContent(folder)

            # 保存配置
            qconfig.save()