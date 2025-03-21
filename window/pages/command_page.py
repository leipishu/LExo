from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit
from qfluentwidgets import GroupHeaderCardWidget, PrimaryPushButton, PushButton, LineEdit, InfoBar, InfoBarPosition, FluentIcon as FIF

class CommandPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)

        # 创建基础指令卡片
        self._create_basic_commands_section()

    def _create_basic_commands_section(self):
        """创建基础指令部分"""
        # 创建 GroupHeaderCardWidget
        self.basic_commands_card = GroupHeaderCardWidget(self)
        self.basic_commands_card.setTitle("基础指令")  # 设置卡片标题
        self.main_layout.addWidget(self.basic_commands_card)

        # 1. hexo三连组
        self.hexo_three_link_btn = PrimaryPushButton(FIF.PLAY_SOLID,"执行三连", self.basic_commands_card)
        self.hexo_three_link_btn.clicked.connect(self.on_hexo_three_link_clicked)
        self.hexo_three_link_group = self.basic_commands_card.addGroup(
            FIF.GLOBE,  # 图标路径
            "Hexo三连",            # 标题
            "执行 Hexo 三连操作",  # 内容描述
            self.hexo_three_link_btn  # 组件
        )

        # 2. 清除缓存组
        self.clear_cache_btn = PushButton(FIF.PLAY,"清除", self.basic_commands_card)
        self.clear_cache_btn.clicked.connect(self.on_clear_cache_clicked)
        self.clear_cache_group = self.basic_commands_card.addGroup(
            FIF.DELETE,
            "清除缓存",
            "清除缓存文件",
            self.clear_cache_btn
        )

        # 3. 生成文件组
        self.generate_files_btn = PushButton(FIF.PLAY,"生成", self.basic_commands_card)
        self.generate_files_btn.clicked.connect(self.on_generate_files_clicked)
        self.generate_files_group = self.basic_commands_card.addGroup(
            FIF.DEVELOPER_TOOLS,
            "生成文件",
            "生成静态文件",
            self.generate_files_btn
        )

        # 4. 本地服务组（PushButton + LineEdit）
        self.local_service_empty_widget = QWidget(self.basic_commands_card)
        self.local_service_group = self.basic_commands_card.addGroup(
            FIF.PROJECTOR,
            "本地服务",
            "启动本地服务",
            self.local_service_empty_widget  # 初始组件设为一个空的 QWidget
        )
        self.local_service_layout = QHBoxLayout()
        self.local_service_layout.setContentsMargins(0, 0, 0, 0)
        self.local_service_layout.setSpacing(5)

        self.local_service_btn = PushButton(FIF.PLAY,"启动", self.basic_commands_card)
        self.local_service_btn.clicked.connect(self.on_local_service_clicked)
        self.local_service_layout.addWidget(self.local_service_btn)

        self.local_service_edit = LineEdit(self.basic_commands_card)
        self.local_service_edit.setPlaceholderText("输入端口")
        self.local_service_layout.addWidget(self.local_service_edit)

        self.local_service_empty_widget.setLayout(self.local_service_layout)

        # 5. 部署组
        self.deploy_btn = PushButton(FIF.PLAY,"部署", self.basic_commands_card)
        self.deploy_btn.clicked.connect(self.on_deploy_clicked)
        self.deploy_group = self.basic_commands_card.addGroup(
            FIF.CLOUD,
            "部署",
            "部署网站",
            self.deploy_btn
        )

        # 6. 初始化组
        self.init_btn = PushButton(FIF.PLAY,"初始化", self.basic_commands_card)
        self.init_btn.clicked.connect(self.on_init_clicked)
        self.init_group = self.basic_commands_card.addGroup(
            FIF.ADD,
            "初始化",
            "初始化项目",
            self.init_btn
        )

    # 以下是各个按钮的槽函数，目前为空，可根据实际需求实现具体逻辑
    def on_hexo_three_link_clicked(self):
        """hexo三连按钮点击事件"""
        InfoBar.success(
            title='Hexo三连',
            content="执行了 Hexo 三连操作。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_clear_cache_clicked(self):
        """清除缓存按钮点击事件"""
        InfoBar.info(
            title='清除缓存',
            content="缓存清除操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_generate_files_clicked(self):
        """生成文件按钮点击事件"""
        InfoBar.info(
            title='生成文件',
            content="文件生成操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_local_service_clicked(self):
        """本地服务按钮点击事件"""
        if self.local_service_edit.text():
            InfoBar.info(
                title='本地服务',
                content=f"服务端口: {self.local_service_edit.text()}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )
        else:
            InfoBar.warning(
                title='本地服务',
                content="请输入服务地址",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=self
            )

    def on_deploy_clicked(self):
        """部署按钮点击事件"""
        InfoBar.info(
            title='部署',
            content="部署操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def on_init_clicked(self):
        """初始化按钮点击事件"""
        InfoBar.info(
            title='初始化',
            content="初始化操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )