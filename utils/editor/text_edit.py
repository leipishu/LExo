# utils/editor/text_edit.py
from PySide6.QtGui import QTextCursor

def wrap_selection_with_symbol(editor, symbol1, symbol2):
    cursor = editor.textCursor()
    if cursor.hasSelection():
        selected = cursor.selectedText()
        cursor.insertText(f"{symbol1}{selected}{symbol2}")
        # 直接移动光标到末尾
        cursor.movePosition(QTextCursor.End)
        cursor.clearSelection()
        editor.setTextCursor(cursor)

def wrap_bold(editor):
    wrap_selection_with_symbol(editor, "**", "**")

def wrap_italic(editor):
    wrap_selection_with_symbol(editor, "_", "_")

def wrap_highlight(editor):
    wrap_selection_with_symbol(editor, "`", "`")

def wrap_underline(editor):
    wrap_selection_with_symbol(editor, "<u>", "</u>")