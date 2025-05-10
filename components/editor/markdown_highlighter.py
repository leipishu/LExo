from PySide6.QtCore import QRegularExpression, Qt
from PySide6.QtGui import QTextCharFormat, QFont, QBrush, QSyntaxHighlighter, QColor


class MarkdownHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rules = []

        # 设置标题高亮
        header_format = QTextCharFormat()
        header_format.setFontWeight(QFont.Bold)
        header_format.setForeground(QBrush(QColor("#25d9e6")))  # 设置标题颜色为 #25d9e6
        self.rules.append((QRegularExpression(r'^\s*(#{1,6})\s*(.*)'), header_format))

        # 设置加粗和斜体高亮
        bold_format = QTextCharFormat()
        bold_format.setFontWeight(QFont.Bold)
        self.rules.append((QRegularExpression(r'\*\*(.+?)\*\*'), bold_format))

        italic_format = QTextCharFormat()
        italic_format.setFontItalic(True)
        self.rules.append((QRegularExpression(r'\*(.+?)\*'), italic_format))
        self.rules.append((QRegularExpression(r'_(.+?)_'), italic_format))  # 支持 _asd_ 格式

        # 设置链接高亮
        link_format = QTextCharFormat()
        link_format.setForeground(QBrush(Qt.magenta))
        self.rules.append((QRegularExpression(r'\[([^\]]+)\]\(([^)]+)\)'), link_format))

        # 设置代码块高亮
        code_block_format = QTextCharFormat()
        code_block_format.setBackground(QBrush(Qt.lightGray))
        code_block_format.setForeground(QBrush(Qt.black))
        self.rules.append((QRegularExpression(r'`{3}.*?`{3}', QRegularExpression.DotMatchesEverythingOption), code_block_format))

        # 设置行内代码高亮
        inline_code_format = QTextCharFormat()
        inline_code_format.setBackground(QBrush(QColor("#25d9e6")))
        inline_code_format.setForeground(QBrush(Qt.black))
        self.rules.append((QRegularExpression(r'`([^`]+)`'), inline_code_format))

        # 设置引用高亮
        quote_format = QTextCharFormat()
        self.rules.append((QRegularExpression(r'>\s*(.*)'), quote_format))

        # 设置 HTML 标签高亮
        html_tag_format = QTextCharFormat()
        html_tag_format.setForeground(QBrush(QColor("#25d9e6")))  # 设置 HTML 标签颜色为 #25d9e6
        self.rules.append((QRegularExpression(r'<[^>]+>'), html_tag_format))  # 高亮 HTML 标签

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = expression.match(text, match.capturedEnd())