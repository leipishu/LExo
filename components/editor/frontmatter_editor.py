from PySide6.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QLabel, QLineEdit
from qfluentwidgets import ScrollArea, PlainTextEdit, LineEdit, CardWidget, BodyLabel # 导入 CardWidget
import re

class FrontmatterManager:
    def __init__(self):
        self.editor = PlainTextEdit()
        self.scroll_area = None
        self.is_visible = False  # 新增可见状态跟踪
        self.title_label = BodyLabel("title")
        self.title_editor = LineEdit()

    def create_editor_area(self, parent):
        # 创建 CardWidget 容器
        self.card_widget = CardWidget(parent)  # 将 CardWidget 添加到父部件中
        self.card_widget.setObjectName("frontmatterCard")  # 可选：设置对象名称以便后续样式定制
        self.card_widget.hide()

        # 创建 ScrollArea
        self.scroll_area = ScrollArea(self.card_widget)  # 将 ScrollArea 添加到 CardWidget 中
        self.scroll_area.setMinimumHeight(150)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color:transparent; border:none;")
        self.scroll_area.hide()

        # 创建容器和布局
        container = QWidget()
        layout = QVBoxLayout(container)

        # 添加 title 编辑部分
        title_layout = QHBoxLayout()  # 更改为 QHBoxLayout
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_editor)
        layout.addLayout(title_layout)

        # 添加原有的 frontmatter 编辑区域
        layout.addWidget(self.editor)

        self.scroll_area.setWidget(container)

        # 将 ScrollArea 添加到 CardWidget 的布局中
        card_layout = QVBoxLayout(self.card_widget)
        card_layout.addWidget(self.scroll_area)

        return self.card_widget  # 返回 CardWidget 作为编辑区域的最外层容器

    # 新增清空方法
    def clear_content(self):
        self.editor.setPlainText("")
        self.title_editor.setText("")

    def set_content(self, text):
        # 解析 frontmatter
        frontmatter_match = re.match(r'^---\s*([\s\S]*?)\s*---\s*', text)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            title_match = re.search(r'^title:\s*(.*)$', frontmatter, re.MULTILINE)
            if title_match:
                self.title_editor.setText(title_match.group(1).strip())

            # 移除 frontmatter 部分，只设置 markdown 内容
            markdown_content = text[frontmatter_match.end():]
            self.editor.setPlainText(markdown_content)
        else:
            # 如果没有 frontmatter，直接设置整个文本到 editor 中
            self.editor.setPlainText(text)


    def get_content(self):
        title = self.title_editor.text().strip()
        frontmatter = self.editor.toPlainText().strip()
        # 合并 title 和其他 frontmatter 内容
        combined_frontmatter = f"title: {title}\n{frontmatter}" if title else frontmatter
        # 确保只有一对 ---
        return f"{combined_frontmatter}\n"

    def toggle_visibility(self, force=None):
        if force is not None:
            self.is_visible = force
        else:
            self.is_visible = not self.is_visible  # <--- 修改切换逻辑

        if self.scroll_area:
            self.scroll_area.setVisible(self.is_visible)

        # 额外控制 CardWidget 的可见性
        self.card_widget.setVisible(self.is_visible)