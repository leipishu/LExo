from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import GroupHeaderCardWidget, PrimaryPushButton, PushButton, LineEdit, FluentIcon as FIF

def create_init_commands_section(parent):
    """创建添加博客部分(独立组件)"""
    # 创建卡片容器
    init_card = GroupHeaderCardWidget(parent)
    init_card.setTitle("添加博客")
    init_card.setFixedHeight(270)

    # 设置固定高度
    max_height = 30  # 根据需要调整高度

    # 1. hexo三连组
    init_btn = PrimaryPushButton(FIF.PLAY_SOLID, "开始初始化", init_card)
    init_btn.setMaximumHeight(max_height)
    init_btn.clicked.connect(parent.on_init_clicked)
    init_card.addGroup(
        FIF.ADD,
        "初始化",
        "新建一个hexo博客",
        init_btn
    )

    parent.init_line_edit = LineEdit(init_card)
    parent.init_line_edit.setMaximumHeight(max_height)
    init_card.addGroup(
        FIF.TAG,
        "名称",
        "输入你的博客名称",
        parent.init_line_edit
    )

    init_emergency_btn = PushButton("急救包", init_card)
    init_emergency_btn.setMaximumHeight(max_height)
    init_emergency_btn.clicked.connect(parent.on_emergency_btn_clicked)
    init_card.addGroup(
        FIF.EMOJI_TAB_SYMBOLS,
        "急救包",
        "如果在中国大陆安装依赖失败可以尝试使用急救包",
        init_emergency_btn
    )

    return init_card