from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QPlainTextEdit, QApplication
from PySide6.QtCore import Qt, QTimer, QByteArray, QBuffer, QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PySide6.QtGui import QColor
from qfluentwidgets import ScrollArea, PlainTextEdit, FluentIcon, CardWidget, ColorDialog, FluentIcon as FIF
import re

from components.editor.line_number import LineNumberEditor
from components.editor.preview_panel import PreviewPanel
from components.editor.toolbar_manager import ToolbarManager
from components.editor.frontmatter_editor import FrontmatterManager
from components.editor.markdown_highlighter import MarkdownHighlighter

from utils.editor.file_mgr import *
from utils.editor.text_edit import *
from utils.editor.md_renderer import *

class MarkdownEditorPage(QWidget, PreviewPanel, ToolbarManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.right_scroll = None
        self.current_file_path = None
        self.current_file = None
        self.show_frontmatter = None
        self.frontmatter_manager = FrontmatterManager()

        # 初始化界面
        self.network_manager = QNetworkAccessManager(self)
        self.image_cache = {}
        self.initUI()
        self.initConnections()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # 主编辑区域布局
        self.main_container = QSplitter(Qt.Vertical)
        self.main_container.setStyleSheet("QSplitter::handle { background: transparent; border: none; }")

        # 添加原有的编辑和预览区域
        self.editor_container = QSplitter(Qt.Horizontal)
        self.editor_container.setStyleSheet("QSplitter::handle { background: transparent; border: none; }")
        self.editor = LineNumberEditor()
        self.editor_container.addWidget(self.editor)

        # 创建frontmatter区域（使用manager）
        frontmatter_scroll = self.frontmatter_manager.create_editor_area(self)
        self.main_container.addWidget(self.editor_container)
        self.main_container.addWidget(frontmatter_scroll)

        # 将工具栏添加到CardWidget中
        toolbar_card = CardWidget(self)
        toolbar_layout = QVBoxLayout(toolbar_card)
        toolbar_layout.addWidget(self.create_toolbar())
        toolbar_layout.addLayout(self.create_format_toolbar())
        self.setup_toolbar_layout()

        # 将CardWidget添加到主布局中
        self.layout.addWidget(toolbar_card)
        self.layout.addWidget(self.main_container)

        # 应用 Markdown 语法高亮
        self.highlighter = MarkdownHighlighter(self.editor.document())

    def initConnections(self):
        self.open_btn.clicked.connect(lambda: open_markdown_file(self, self.editor, self))
        self.undo_btn.triggered.connect(self.editor.undo)
        self.redo_btn.triggered.connect(self.editor.redo)
        self.bold_btn.clicked.connect(lambda: wrap_bold(self.editor))
        self.italic_btn.clicked.connect(lambda: wrap_italic(self.editor))
        self.highlight_btn.clicked.connect(lambda: wrap_highlight(self.editor))
        self.underline_btn.clicked.connect(lambda: wrap_underline(self.editor))
        self.title_btn.clicked.connect(lambda: title_h1(self.editor))
        self.title_btn_h1.triggered.connect(lambda: title_h1(self.editor))
        self.title_btn_h2.triggered.connect(lambda: title_h2(self.editor))
        self.title_btn_h3.triggered.connect(lambda: title_h3(self.editor))
        self.title_btn_h4.triggered.connect(lambda: title_h4(self.editor))
        self.title_btn_h5.triggered.connect(lambda: title_h5(self.editor))
        self.title_btn_h6.triggered.connect(lambda: title_h6(self.editor))
        self.color_btn.clicked.connect(self.color_logic)
        self.show_frame_btn.triggered.connect(self.toggle_right_frame)
        self.save_btn.clicked.connect(lambda: save_markdown_file(self, self.editor, self))
        self.save_btn_2.triggered.connect(lambda: save_markdown_file(self, self.editor, self))
        self.save_as_action.triggered.connect(lambda: save_as_markdown_file(self, self.editor, self))
        self.save_copy_action.triggered.connect(lambda: save_copy_markdown_file(self, self.editor, self))
        self.editor.textChanged.connect(self.update_preview)
        self.image_load_switch.checkedChanged.connect(lambda: self.update_preview())
        self.toggle_frontmatter_btn.triggered.connect(self.toggle_frontmatter)

    def toggle_frontmatter(self):
        self.frontmatter_manager.toggle_visibility()

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

    def color_logic(self):
        self.color_dialog = ColorDialog(QColor(0, 255, 255), "Choose Color", self, enableAlpha=False)
        self.color_dialog.show()
        self.color_dialog.colorChanged.connect(lambda color: wrap_color(editor=self.editor, color=color.name()))
        # self.color_dialog.colorChanged.connect(lambda color: self.color_btn.setIcon(FIF.PALETTE.icon(color=color.name())))

    def async_image_load(self, html):
        """异步加载图片并替换为占位符"""
        if not self.image_load_switch.isEnabled():
            # 直接替换所有网络图片为占位符
            return re.sub(
                r'<img\s+([^>]*?)src=(["\'])(http[^\2]+?)\2',
                r'<img \1src="https://via.placeholder.com/600x200/eee/ccc?text=Image+Disabled"',
                html,
                flags=re.IGNORECASE
            )
        pattern = r'<img[^>]+src="(http[^"]+)"'
        matches = re.findall(pattern, html)
        for url in matches:
            if url not in self.image_cache:
                # 先替换为加载中占位符
                html = html.replace(url, "https://via.placeholder.com/600x200/eee/ccc?text=Loading...")
                # 发起异步请求
                request = QNetworkRequest(QUrl(url))
                reply = self.network_manager.get(request)
                reply.finished.connect(lambda r=reply, u=url: self._handle_image_response(r, u))
            else:
                # 使用缓存图片
                html = html.replace(url, self.image_cache[url])

        return html

    def _handle_image_response(self, reply, url):
        """处理图片响应"""
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            image = QImage.fromData(data)
            pixmap = QPixmap.fromImage(image)

            # 限制尺寸并转为base64
            scaled = pixmap.scaled(600, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            byte_array = QByteArray()
            buffer = QBuffer(byte_array)
            scaled.save(buffer, "PNG")
            base64_data = byte_array.toBase64().data().decode()

            # 缓存处理后的图片
            self.image_cache[url] = f"data:image/png;base64,{base64_data}"

            # 更新预览
            if self.right_scroll and self.right_scroll.isVisible():
                self.update_preview()
        reply.deleteLater()

    def update_preview(self):
        """带节流机制的预览更新"""
        if not self.right_scroll:
            return

        # 使用定时器实现延迟更新
        if hasattr(self, '_preview_timer'):
            self._preview_timer.stop()

        self._preview_timer = QTimer()
        self._preview_timer.setSingleShot(True)
        self._preview_timer.timeout.connect(self._do_update_preview)
        self._preview_timer.start(500)  # 500毫秒延迟

    def _do_update_preview(self):
        text = self.editor.toPlainText()
        html = convert_markdown(text)
        # 获取当前滚动位置
        if self.right_scroll:
            scroll = self.right_scroll.verticalScrollBar()
            old_pos = scroll.value()
            at_bottom = (scroll.maximum() - scroll.value()) <= 20  # 判断是否在底部
        # 先处理所有图片逻辑
        if self.image_load_switch.isChecked():
            # 处理真实图片加载（需要先清除之前的占位符）
            html = re.sub(r'<img[^>]+src="https://via\.placeholder\.com/[^"]+"',
                        '<img src', html)
            html = self.async_image_load(html)
        else:
            # 清除所有可能的缓存替换
            html = re.sub(r'<img[^>]+src="data:image/[^"]+"',
                        '<img src', html)
            # 替换所有网络图片为占位符（更严格的正则）
            html = re.sub(
                r'<img\s+([^>]*?)(src=([\"\']))(http[^\3]+?)\3',
                r'<img \1\2https://via.placeholder.com/600x200/eee/ccc?text=Image+Disabled\3',
                html,
                flags=re.IGNORECASE
            )

        # 最后统一应用尺寸限制
        html = html.replace('<img src', '<img style="max-width: 600px; height: auto;" src')
        PreviewPanel.update_preview_content(self, html)
        #恢复滚动位置
        if self.right_scroll:
            if at_bottom:  # 如果在底部则保持到底部
                scroll.setValue(scroll.maximum())
            else:  # 否则恢复原位置
                scroll.setValue(old_pos)
