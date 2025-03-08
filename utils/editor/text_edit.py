# utils/editor/text_edit.py
from PySide6.QtGui import QTextCursor

def wrap_selection_with_symbol(editor, symbol):
    cursor = editor.textCursor()
    if cursor.hasSelection():
        selected = cursor.selectedText()
        cursor.insertText(f"{symbol}{selected}{symbol}")
        # 自动选中新加的内容
        cursor.setPosition(cursor.position() - len(symbol)*2)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(selected) + len(symbol)*2)
        editor.setTextCursor(cursor)

def wrap_bold(editor):
    wrap_selection_with_symbol(editor, "**")
