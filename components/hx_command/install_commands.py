from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import GroupHeaderCardWidget, PrimaryPushButton, PushButton, LineEdit, FluentIcon as FIF
from utils.hx_command.run_install_commands import on_install_nodejs_clicked, on_install_hexo_clicked

def create_install_commands_section(parent):
    """创建环境安装部分(独立组件)"""
    # 创建卡片容器
    card_install = GroupHeaderCardWidget(parent)
    card_install.setTitle("环境安装")
    card_install.setFixedHeight(180)

    # 设置固定高度
    max_height = 30  # 根据需要调整高度

    # 1, 安装node,js
    install_nodejs_btn = PushButton(FIF.LINK, "前往", card_install)
    install_nodejs_btn.setMaximumHeight(max_height)
    install_nodejs_btn.clicked.connect(on_install_nodejs_clicked)
    card_install.addGroup(
        FIF.DOWNLOAD,
        "安装node.js",
        "node.js官网安装页面",
        install_nodejs_btn
    )

    # 2. 安装 Hexo-cli
    install_hexo_btn = PushButton(FIF.DOWNLOAD, "安装", card_install)
    install_hexo_btn.setMaximumHeight(max_height)
    install_hexo_btn.clicked.connect(on_install_hexo_clicked)
    card_install.addGroup(
        FIF.DEVELOPER_TOOLS,
        "安装Hexo",
        "通过npm安装hexo-cli",
        install_hexo_btn
    )

    return card_install