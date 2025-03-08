from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFontMetrics
from PySide6.QtCore import Qt, QRect
from qfluentwidgets import PlainTextEdit

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
        painter.setPen(QColor(100, 100, 100))

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
