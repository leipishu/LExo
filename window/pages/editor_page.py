from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt
from qfluentwidgets import setTheme, Theme
from utils.editor.md_renderer import convert_markdown

from components.editor.line_number import LineNumberEditor
from components.editor.preview_panel import PreviewPanel
from components.editor.toolbar_manager import ToolbarManager

from utils.editor.file_mgr import *
from utils.editor.text_edit import *
from utils.editor.md_renderer import *

class MarkdownEditorPage(QWidget, PreviewPanel, ToolbarManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("MarkdownEditor")
        self.right_scroll = None
        self.current_file_path = None
        self.current_file = None

        # 初始化界面
        self.setup_theme()
        self.initUI()
        self.initConnections()

    def setup_theme(self):
        setTheme(Theme.LIGHT)

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # 工具栏
        self.layout.addWidget(self.create_toolbar())
        self.layout.addLayout(self.create_format_toolbar())
        self.setup_toolbar_layout()

        # 编辑器区域
        self.editor_container = QSplitter(Qt.Horizontal)
        self.editor = LineNumberEditor()
        self.editor_container.addWidget(self.editor)
        self.layout.addWidget(self.editor_container)

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
        self.editor.textChanged.connect(self.update_preview)

    def toggle_right_frame(self):
        if not self.right_scroll:
            self.right_scroll = self.create_preview_area()
            self.editor_container.addWidget(self.right_scroll)
            self.editor_container.setStyleSheet("QSplitter::handle { background: transparent; border: none; }")
            self.right_scroll.setMinimumWidth(200)
            self.update_preview()
        else:
            self.right_scroll.setVisible(not self.right_scroll.isVisible())

        if self.right_scroll and self.right_scroll.isVisible():
            self.editor_container.setSizes([300, 100])
        else:
            self.editor_container.setSizes([400])

    def update_preview(self):
        if self.right_scroll and self.right_scroll.isVisible():
            text = self.editor.toPlainText()
            html = convert_markdown(text)
            self.preview.setHtml(html)
