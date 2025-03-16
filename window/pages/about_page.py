from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from qfluentwidgets import TitleLabel, CaptionLabel, BodyLabel, HyperlinkButton, FluentIcon, LargeTitleLabel,SubtitleLabel, StrongBodyLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 30)
        layout.setSpacing(15)  # 修正了这里的语法错误

        # 应用图标
        icon_label = QLabel(self)
        pixmap = QPixmap('./resources/img/App_Icon.png')  # 替换为实际图标路径
        icon_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(icon_label)

        # 应用名称
        title_label = LargeTitleLabel("LExo")
        layout.addWidget(title_label, 0, Qt.AlignHCenter)

        # 版本信息
        version_label = SubtitleLabel("版本: indev 1.1")
        layout.addWidget(version_label, 0, Qt.AlignHCenter)

        # 作者信息
        author_label = SubtitleLabel("作者: Leipishu")
        layout.addWidget(author_label, 0, Qt.AlignHCenter)

        # 简介
        description = BodyLabel()
        description.setText("Hexo 博客配置与主题编辑器")
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)

        more_description = BodyLabel()
        more_description.setText("LExo 是一个基于 Python 的桌面应用程序，旨在为 Hexo 博客框架及其主题（如 Butterfly）提供便捷的配置文件编辑功能。")
        more_description.setAlignment(Qt.AlignCenter)
        layout.addWidget(more_description)

        more_description2 = BodyLabel()
        more_description2.setText("该项目结合了 Markdown 编辑器和配置文件管理工具，帮助用户更高效地管理和编辑 Hexo 博客的相关配置。")
        more_description2.setAlignment(Qt.AlignCenter)
        layout.addWidget(more_description2)

        # 链接按钮
        button_layout = QHBoxLayout()

        github_btn = HyperlinkButton(
            url="https://github.com/leipishu/LExo",
            text="GitHub",
            icon=FluentIcon.GITHUB
        )

        website_btn = HyperlinkButton(
            url="https://www.leipishu.top",
            text="Website",
            icon=FluentIcon.LINK
        )

        button_layout.addStretch(1)
        button_layout.addWidget(github_btn)
        button_layout.addWidget(website_btn)
        button_layout.addStretch(1)

        layout.addLayout(button_layout)

        # 有Bug？和贡献代码？
        bug_contribution_layout = QHBoxLayout()

        # 有Bug？部分
        bug_label = LargeTitleLabel("有Bug？")
        bug_layout = QVBoxLayout()
        bug_layout.addWidget(bug_label)
        bug_label.setAlignment(Qt.AlignCenter)

        bug_description = BodyLabel()
        bug_description.setText("如果您发现了任何问题或Bug，请报告Issues")
        bug_layout.addWidget(bug_description)
        bug_description.setAlignment(Qt.AlignCenter)

        bug_report_btn = HyperlinkButton(
            url="https://github.com/leipishu/LExo/issues",
            text="报告Bug",
            icon=FluentIcon.MEGAPHONE
        )
        bug_layout.addWidget(bug_report_btn)

        bug_contribution_layout.addLayout(bug_layout)

        # 贡献代码？部分
        contribution_label = LargeTitleLabel("贡献代码？")
        contribution_layout = QVBoxLayout()
        contribution_layout.addWidget(contribution_label)
        contribution_label.setAlignment(Qt.AlignCenter)

        contribution_description = BodyLabel()
        contribution_description.setText("如果您想为项目贡献代码，请提交PR。")
        contribution_layout.addWidget(contribution_description)
        contribution_description.setAlignment(Qt.AlignCenter)

        contribution_btn = HyperlinkButton(
            url="https://github.com/leipishu/LExo/pulls",
            text="贡献指南",
            icon=FluentIcon.CODE
        )
        contribution_layout.addWidget(contribution_btn)

        bug_contribution_layout.addLayout(contribution_layout)

        layout.addLayout(bug_contribution_layout)

        # 底部留白
        layout.addStretch(1)
