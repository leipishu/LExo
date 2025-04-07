from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QFileDialog
from qfluentwidgets import GroupHeaderCardWidget, PrimaryPushButton, PushButton, LineEdit, FluentIcon as FIF
import os
from utils.hx_command.run_basic_commands import hexo_three_link_clicked, clear_cache_clicked, generate_files_clicked, local_service_clicked, deploy_clicked

def create_basic_commands_section(parent):
    """创建基础指令部分(独立组件)"""
    # 确保 parent 对象有 current_file_path 属性
    if not hasattr(parent, 'current_file_path'):
        parent.current_file_path = None

    # 创建卡片容器
    card = GroupHeaderCardWidget(parent)
    card.setTitle("基础指令")
    card.setFixedHeight(540)

    # 设置固定高度
    max_height = 30  # 根据需要调整高度

    # 0. 选择组
    browse_widget = QWidget(card)
    browse_layout = QHBoxLayout(browse_widget)
    browse_layout.setContentsMargins(0, 0, 0, 0)

    browse_btn = PushButton(FIF.FOLDER, "浏览", card)
    browse_btn.setMaximumHeight(max_height)
    browse_line_edit = LineEdit(card)
    browse_line_edit.setPlaceholderText("选择或输入路径")
    browse_line_edit.setMaximumHeight(max_height)
    browse_btn.clicked.connect(lambda: on_browse_btn_clicked(card, browse_line_edit, parent))
    browse_layout.addWidget(browse_line_edit)
    browse_layout.addWidget(browse_btn)
    card.addGroup(
        FIF.FOLDER,
        "选择组",
        "选择或输入路径",
        browse_widget
    )

    # 1. hexo三连组
    hexo_btn = PrimaryPushButton(FIF.PLAY_SOLID, "执行三连", card)
    hexo_btn.setMaximumHeight(max_height)
    hexo_btn.clicked.connect(lambda: hexo_three_link_clicked(parent))
    card.addGroup(
        FIF.GLOBE,
        "Hexo三连",
        "执行 Hexo 三连操作",
        hexo_btn
    )

    # 2. 清除缓存组
    clear_btn = PushButton(FIF.PLAY, "清除", card)
    clear_btn.setMaximumHeight(max_height)
    clear_btn.clicked.connect(lambda: clear_cache_clicked(parent))
    card.addGroup(
        FIF.DELETE,
        "清除缓存",
        "清除缓存文件",
        clear_btn
    )

    # 3. 生成文件组
    generate_btn = PushButton(FIF.PLAY, "生成", card)
    generate_btn.setMaximumHeight(max_height)
    generate_btn.clicked.connect(lambda: generate_files_clicked(parent))
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
    parent.service_btn.setMaximumHeight(max_height)
    parent.service_btn.clicked.connect(lambda: local_service_clicked(parent))
    parent.stop_service_btn = PushButton(FIF.PAUSE, "停止", card)
    parent.stop_service_btn.setMaximumHeight(max_height)
    parent.service_edit = LineEdit(card)
    parent.service_edit.setMaximumHeight(max_height)
    parent.service_edit.setPlaceholderText("输入端口")

    service_layout.addWidget(parent.service_btn)
    service_layout.addWidget(parent.stop_service_btn)
    service_layout.addWidget(parent.service_edit)
    card.addGroup(
        FIF.PROJECTOR,
        "本地服务",
        "启动本地服务",
        service_widget
    )

    # 5. 部署组
    deploy_btn = PushButton(FIF.PLAY, "部署", card)
    deploy_btn.setMaximumHeight(max_height)
    deploy_btn.clicked.connect(lambda: deploy_clicked(parent))
    card.addGroup(
        FIF.CLOUD,
        "部署",
        "部署网站",
        deploy_btn
    )

    return card

def on_browse_btn_clicked(card, browse_line_edit, parent):
    """打开文件对话框选择路径，并将路径显示在browse_line_edit中"""
    default_path = "app/sites"
    selected_path = QFileDialog.getExistingDirectory(card, "选择路径", default_path)
    if selected_path:
        # 判断是否在默认路径下
        common_path = os.path.commonpath([os.path.abspath(selected_path), os.path.abspath(default_path)])
        if common_path == os.path.abspath(default_path):
            # 获取默认路径后的第一个目录名称（即博客名称）
            relative_path = os.path.relpath(selected_path, default_path)
            if relative_path:
                blog_name = relative_path.split(os.path.sep)[0]
                browse_line_edit.setText(blog_name)
                parent.current_file_path = selected_path
            else:
                # 如果选择的是默认路径本身，则清空输入框
                browse_line_edit.setText("")
                parent.current_file_path = None
        else:
            # 显示完整路径
            browse_line_edit.setText(selected_path)
            parent.current_file_path = selected_path
