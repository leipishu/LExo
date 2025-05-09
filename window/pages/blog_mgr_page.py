from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QLabel, QSpacerItem, QSizePolicy
from qfluentwidgets import CardWidget, BodyLabel, CaptionLabel, PushButton, ScrollArea, StrongBodyLabel,TitleLabel
from utils.blog_mgr.folder_reader import get_blog_folders
from utils.blog_mgr.config_reader import read_blog_config
import os

class BlogMgrPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # 创建工具栏卡片
        toolbar_card = CardWidget(self)
        toolbar_layout = QHBoxLayout(toolbar_card)
        toolbar_layout.addWidget(BodyLabel("工具栏", self))
        toolbar_layout.addStretch(1)  # 添加弹性空间以填充剩余空间
        # 设置工具栏的外边距
        toolbar_card.setContentsMargins(0, 0, 0, 0)  # 去掉默认的外边距

        # 将工具栏添加到主布局中
        main_layout.addWidget(toolbar_card)
        for _ in range(3):  # 添加几个空的PushButton
           toolbar_layout.addWidget(PushButton("按钮", self))

        # 创建一个 QSpacerItem 来增加 toolbar_card 和 scroll_area 之间的间距
        spacer = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        main_layout.addItem(spacer)

        # 创建滚动区域
        scroll_area = ScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 确保滚动区域可以调整大小
        scroll_area.setFrameShape(QFrame.NoFrame)  # 去掉边框
        scroll_area.setMinimumHeight(600)  # 设置滚动区域的最小高度
        scroll_area.setStyleSheet("background-color: transparent;")
        scroll_area.setContentsMargins(0, 0, 0, 0)  # 设置滚动区域的内边距为0

        # 创建滚动区域的内容容器
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)  # 设置卡片之间的间距
        content_layout.setContentsMargins(0, 0, 0, 0)  # 设置内容容器的外边距

        # 获取 ./app/sites 目录下的文件夹名称
        blog_folders = get_blog_folders("./app/sites")

        # 根据文件夹数量动态生成卡片
        for folder_name in blog_folders:
            # 替换路径中的反斜杠为正斜杠
            folder_path = os.path.join("./app/sites", folder_name).replace("\\", "/")
            config = read_blog_config(folder_path)

            # 创建卡片
            card = CardWidget(self)
            card_layout = QVBoxLayout(card)

            # 上半部分：标题和描述
            upper_part_layout = QVBoxLayout()
            titleLabel = TitleLabel(folder_name, card)
            contentLabel = BodyLabel("这是关于 " + folder_name + " 的博客", card)
            upper_part_layout.addWidget(titleLabel)
            upper_part_layout.addWidget(contentLabel)
            upper_part_layout.addStretch(1)

            # 下半部分：基础配置
            lower_part_layout = QHBoxLayout()  # 使用水平布局
            config_card = CardWidget(self)  # 创建一个新卡片用于基础配置
            config_card_layout = QVBoxLayout(config_card)
            config_title = StrongBodyLabel("基本配置", config_card)
            config_card_layout.addWidget(config_title)

            if config:
                # 显示配置信息
                for key, value in config.items():
                   if key in ["title", "subtitle", "description", "keywords", "author", "language"]:
                        key_label = BodyLabel(key.capitalize() + ":", config_card)
                        value_label = BodyLabel(str(value) if value else "", config_card)
                        value_label.setWordWrap(True)  # 允许换行

                        # 创建水平布局来对齐键和值
                        key_value_layout = QHBoxLayout()
                        key_value_layout.addWidget(key_label)
                        key_value_layout.addWidget(value_label)
                        key_value_layout.addStretch(1)

                        config_card_layout.addLayout(key_value_layout)
            else:
                # 显示错误信息
                error_label = CaptionLabel("读取配置文件失败", config_card)
                config_card_layout.addWidget(error_label)

            config_card.setLayout(config_card_layout)
            lower_part_layout.addWidget(config_card)  # 将基础配置卡片添加到布局中

            # 添加几个空卡片
            for _ in range(3):
               empty_card = CardWidget(self)
               empty_card.setMinimumHeight(50)
               empty_card_layout = QVBoxLayout()
               empty_card_layout.addWidget(BodyLabel("空卡片", empty_card))
               empty_card.setLayout(empty_card_layout)
               lower_part_layout.addWidget(empty_card)  # 将空卡片添加到布局中

            card_layout.addLayout(upper_part_layout)
            card_layout.addLayout(lower_part_layout)

            card.setLayout(card_layout)
            content_layout.addWidget(card)

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 将滚动区域添加到主布局
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
