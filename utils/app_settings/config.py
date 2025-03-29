# config.py

from qfluentwidgets import (
    OptionsConfigItem,
    OptionsValidator,
    qconfig,
    QConfig,
    Theme,
    ConfigItem,
)


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
        group="App",
        name="DownloadFolder",
        default="D:/Users/下载",
    )

    packageMgr = OptionsConfigItem(
        group="App",
        name="PackageMgr",
        default="npm",
        validator=OptionsValidator(["npm", "cnpm", "pnpm"]),
        restart=True,
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
