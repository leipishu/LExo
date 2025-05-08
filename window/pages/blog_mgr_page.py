from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QScrollArea, QFrame
from qfluentwidgets import CardWidget, BodyLabel, CaptionLabel, PushButton, ScrollArea
from utils.blog_mgr.folder_reader import get_blog_folders

class BlogMgrPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
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
        content_layout = QGridLayout(content_widget)
        content_layout.setSpacing(10)  # 设置卡片之间的间距
        content_layout.setContentsMargins(10, 10, 10, 10)  # 设置内容容器的外边距

        # 获取 ./app/sites 目录下的文件夹名称
        blog_folders = get_blog_folders("./app/sites")

        # 根据文件夹数量动态生成卡片
        row = 0
        col = 0
        for folder_name in blog_folders:
            card = CardWidget(self)
            card.setMinimumHeight(350)
            titleLabel = BodyLabel(folder_name, card)
            contentLabel = CaptionLabel("这是关于 " + folder_name + " 的博客", card)
            openButton = PushButton("打开", card)

            # 创建卡片的内部布局
            card_layout = QVBoxLayout()
            card_layout.addWidget(titleLabel)
            card_layout.addWidget(contentLabel)
            card_layout.addStretch(1)
            card_layout.addWidget(openButton)
            card.setLayout(card_layout)

            # 将卡片添加到网格布局中
            content_layout.addWidget(card, row, col)
            col += 1
            if col > 1:  # 每行最多放置2个卡片
                col = 0
                row += 1

        # 设置滚动区域的内容
        scroll_area.setWidget(content_widget)

        # 创建主布局并添加滚动区域
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # 设置主布局的外边距为0
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)