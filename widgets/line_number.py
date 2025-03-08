from PySide6.QtWidgets import QWidget, QPlainTextEdit
from PySide6.QtGui import QPainter, QColor, QFontMetrics, QFont
from PySide6.QtCore import Qt, QRect
from qfluentwidgets import setStyleSheet, setTheme, Theme, LineEdit, FluentStyleSheet  # 引入 qfluentwidgets 相关组件[^1^][^2^]

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        FluentStyleSheet.LINE_EDIT.apply(self)
        self.setFont(editor.font())

        # 设置字体样式为 qfluentwidgets 的默认字体
        self.font = QFont("Microsoft YaHei", 10)  # 使用微软雅黑字体，大小为10
        self.setFont(self.font)

    def width(self):
        digits = len(str(max(1, self.editor.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 使用 qfluentwidgets 的背景和文字颜色
        painter.fillRect(event.rect(), QColor(245, 245, 245))  # 浅灰色背景
        painter.setPen(QColor(100, 100, 100))  # 灰色文字[^1^]

        block = self.editor.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
        bottom = top + self.editor.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    0, int(top),
                    self.width() - 5, self.fontMetrics().height(),
                    Qt.AlignRight, number
                )

            block = block.next()
            top = bottom
            bottom = top + self.editor.blockBoundingRect(block).height()
            block_number += 1


class LineNumberEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)

        # 使用 qfluentwidgets 的样式表
        setStyleSheet(self, "qfluentwidgets/style.qss")  # 设置整体样式[^1^]
        setTheme(Theme.LIGHT)  # 设置主题为浅色[^2^]

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth()

    def updateLineNumberAreaWidth(self):
        self.setViewportMargins(self.lineNumberArea.width(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(),
                                       self.lineNumberArea.width(), rect.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            cr.left(), cr.top(),
            self.lineNumberArea.width(), cr.height()
        )