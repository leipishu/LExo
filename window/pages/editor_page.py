from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QSplitter
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QColor, QFontMetrics, QFont, QTextCursor
from qfluentwidgets import (
    Action, CommandBar, PrimaryPushButton,
    FluentIcon as FIF, PlainTextEdit, setTheme, Theme, ScrollArea, FluentStyleSheet, TransparentPushButton, RoundMenu, PrimaryDropDownPushButton
)
from utils.editor.text_edit import *
from utils.editor.file_mgr import *
from PySide6.QtWidgets import QTextBrowser
from utils.editor.md_renderer import convert_markdown

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.editor.blockCountChanged.connect(self.updateWidth)
        self.editor.updateRequest.connect(self.updateContents)
        self.updateWidth()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor(100, 100, 100))  # 灰色文字

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    QRect(0, int(top) + 2, self.width(), self.fontMetrics().height()),
                    Qt.AlignLeft | Qt.AlignVCenter,
                    number
                )
            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1

    def updateWidth(self):
        self.editor.setViewportMargins(self.width(), 0, 0, 0)

    def updateContents(self, rect, dy):
        if dy:
            self.scroll(0, dy)
        else:
            self.update(0, rect.y(), self.width(), rect.height())

    def width(self):
        digits = len(str(max(1, self.editor.blockCount())))
        return self.fontMetrics().horizontalAdvance('9') * digits + 10


class LineNumberEditor(PlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            cr.left(), cr.top(),
            self.lineNumberArea.width(), cr.height()
        )


class MarkdownEditorPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MarkdownEditor")
        self.right_scroll = None
        self.initUI()
        self.initConnections()
        self.editor.textChanged.connect(self.update_preview)
        self.current_file_path = None  # 新增文件路径跟踪
        self.current_file = None  # 新增文件路径跟踪

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # 顶部工具栏（保留图标按钮）
        self.toolbar = CommandBar(self)
        self.open_btn = PrimaryPushButton(FIF.FOLDER, "打开")
        self.undo_btn = Action(FIF.LEFT_ARROW, "撤销")
        self.redo_btn = Action(FIF.RIGHT_ARROW, "重做")
        self.show_frame_btn = Action(FIF.VIEW, "显示面板")
        self.save_btn = PrimaryDropDownPushButton(FIF.SAVE, "保存")
        # 创建带有下拉菜单的保存按钮
        self.save_menu = RoundMenu(parent=self.save_btn)
        self.save_as_action = Action(FIF.SAVE_AS, "另存为")
        self.save_copy_action = Action(FIF.SAVE_COPY, " 保存并复制")
        self.save_menu.addAction(self.save_as_action)
        self.save_menu.addAction(self.save_copy_action)

        self.save_btn.setMenu(self.save_menu)  # 将下拉菜单设置到按钮上

        self.toolbar.addWidget(self.save_btn)  # 添加主按钮控件
        self.toolbar.addWidget(self.open_btn)
        self.toolbar.addSeparator()
        self.toolbar.addActions([self.undo_btn, self.redo_btn])
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.show_frame_btn)

        # 第二排普通文字按钮
        self.text_format_toolbar = QHBoxLayout()
        self.bold_btn = TransparentPushButton("加粗")
        self.highlight_btn = TransparentPushButton("高亮")
        self.italic_btn = TransparentPushButton("斜体")

        self.text_format_toolbar.addWidget(self.bold_btn)
        self.text_format_toolbar.addWidget(self.italic_btn)
        self.text_format_toolbar.addWidget(self.highlight_btn)
        self.text_format_toolbar.addStretch(1)

        # 编辑器区域
        self.editor_container = QSplitter(Qt.Horizontal)
        self.editor = LineNumberEditor()
        self.editor_container.addWidget(self.editor)

        # 组合布局
        self.layout.addWidget(self.toolbar)
        self.layout.addLayout(self.text_format_toolbar)
        self.layout.addWidget(self.editor_container)

        setTheme(Theme.LIGHT)

    def initConnections(self):
        self.open_btn.clicked.connect(lambda: open_markdown_file(self, self.editor, self))
        self.undo_btn.triggered.connect(self.editor.undo)
        self.redo_btn.triggered.connect(self.editor.redo)
        self.bold_btn.clicked.connect(lambda: wrap_bold(self.editor))
        self.italic_btn.clicked.connect(lambda: wrap_italic(self.editor))
        self.highlight_btn.clicked.connect(lambda: wrap_highlight(self.editor))
        self.show_frame_btn.triggered.connect(self.toggle_right_frame)
        self.save_btn.clicked.connect(lambda: save_markdown_file(self, self.editor, self))
        self.save_as_action.triggered.connect(lambda: save_as_markdown_file(self, self.editor))
        self.save_copy_action.triggered.connect(lambda: save_copy_markdown_file(self, self.editor, self))

    # 其他方法保持不变...


    def toggle_right_frame(self):
        """切换右侧滚动面板的显示状态"""
        if not self.right_scroll:
            # 创建滚动区域并添加内容
            self.right_scroll = ScrollArea()
            self.right_scroll.setObjectName("RightPanel")

            # 创建预览区域
            self.preview = QTextBrowser()
            self.preview.setOpenExternalLinks(True)
            self.preview.setMinimumWidth(200)

            # 设置预览区域样式
            self.right_scroll.setStyleSheet("""
                QScrollArea {
                    background-color: transparent; /* 设置滚动区域背景为白色 */
                    border-left: 1px solid #eeeeee; /* 添加左侧边框 */
                    border-radius: 5px; /* 添加圆角 */
                }
                QScrollBar:vertical {
                    background: #f5f5f5; /* 滚动条背景 */
                    width: 10px;
                }
                QScrollBar::handle:vertical {
                    background: #cccccc; /* 滚动条滑块颜色 */
                    min-height: 20px;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    background: none; /* 隐藏滚动条上下按钮 */
                }
            """)

            self.preview.setStyleSheet("""
                QTextBrowser {
                    background-color: white; /* 设置预览区域背景为白色 */
                    border-radius: 5px; /* 添加圆角 */
                    color: black; /* 文字颜色 */
                    border: none; /* 去掉边框 */
                    padding: 10px; /* 内边距 */
                }
            """)

            # 设置布局
            content = QWidget()
            content_layout = QVBoxLayout(content)
            content_layout.addWidget(self.preview)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content.setStyleSheet("""
                background-color: transparent;
            """)

            self.right_scroll.setWidget(content)
            self.right_scroll.setWidgetResizable(True)

            # 添加到分割器
            self.editor_container.addWidget(self.right_scroll)
            self.update_preview()

            # 设置 QSplitter 的样式表
            self.editor_container.setStyleSheet("""
                QSplitter::handle {
                    background: transparent;
                    border: none;
                }
            """)

            # 设置滚动面板的最小宽度
            self.right_scroll.setMinimumWidth(200)

        else:
            # 切换显示状态前确保对象存在
            visible = self.right_scroll.isVisible()
            self.right_scroll.setVisible(not visible)

        # 调整 QSplitter 的初始比例
        if self.right_scroll and self.right_scroll.isVisible():
            self.editor_container.setSizes([300, 100])  # 左侧编辑器宽度为 300，右侧面板宽度为 100
        else:
            self.editor_container.setSizes([400])  # 只有编辑器时的宽度

    def update_preview(self):
        """更新Markdown预览"""
        if self.right_scroll and self.right_scroll.isVisible():
            text = self.editor.toPlainText()
            html = convert_markdown(text)
            self.preview.setHtml(html)