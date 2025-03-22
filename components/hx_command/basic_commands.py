from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import GroupHeaderCardWidget, PrimaryPushButton, PushButton, LineEdit, FluentIcon as FIF

def create_basic_commands_section(parent):
    """创建基础指令部分(独立组件)"""
    # 创建卡片容器
    card = GroupHeaderCardWidget(parent)
    card.setTitle("基础指令")

    # 1. hexo三连组
    hexo_btn = PrimaryPushButton(FIF.PLAY_SOLID, "执行三连", card)
    hexo_btn.clicked.connect(parent.on_hexo_three_link_clicked)
    card.addGroup(
        FIF.GLOBE,
        "Hexo三连",
        "执行 Hexo 三连操作",
        hexo_btn
    )

    # 2. 清除缓存组
    clear_btn = PushButton(FIF.PLAY, "清除", card)
    clear_btn.clicked.connect(parent.on_clear_cache_clicked)
    card.addGroup(
        FIF.DELETE,
        "清除缓存",
        "清除缓存文件",
        clear_btn
    )

    # 3. 生成文件组
    generate_btn = PushButton(FIF.PLAY, "生成", card)
    generate_btn.clicked.connect(parent.on_generate_files_clicked)
    card.addGroup(
        FIF.DEVELOPER_TOOLS,
        "生成文件",
        "生成静态文件",
        generate_btn
    )

    # 4. 本地服务组
    service_widget = QWidget(card)
    service_layout = QHBoxLayout(service_widget)
    service_layout.setContentsMargins(0, 0, 0, 0)

    parent.service_btn = PushButton(FIF.PLAY, "启动", card)
    parent.service_btn.clicked.connect(parent.on_local_service_clicked)
    parent.service_edit = LineEdit(card)
    parent.service_edit.setPlaceholderText("输入端口")

    service_layout.addWidget(parent.service_btn)
    service_layout.addWidget(parent.service_edit)
    card.addGroup(
        FIF.PROJECTOR,
        "本地服务",
        "启动本地服务",
        service_widget
    )

    # 5. 部署组
    deploy_btn = PushButton(FIF.PLAY, "部署", card)
    deploy_btn.clicked.connect(parent.on_deploy_clicked)
    card.addGroup(
        FIF.CLOUD,
        "部署",
        "部署网站",
        deploy_btn
    )

    # 6. 初始化组
    init_btn = PushButton(FIF.PLAY, "初始化", card)
    init_btn.clicked.connect(parent.on_init_clicked)
    card.addGroup(
        FIF.ADD,
        "初始化",
        "初始化项目",
        init_btn
    )

    return card
