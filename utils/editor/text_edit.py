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

def _insert_heading(editor, level):
    cursor = editor.textCursor()
    mark = '#' * level + ' '

    if cursor.hasSelection():
        # 处理选区内容
        selected = cursor.selectedText()
        cursor.insertText(f"{mark}{selected}")
    else:
        # 直接插入标题标记并定位光标
        cursor.insertText(mark)
        # 移动光标到标题内容起始位置
        cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, len(mark))
        cursor.movePosition(QTextCursor.Right, QTextCursor.MoveAnchor, len(mark))

    editor.setTextCursor(cursor)

def title_h1(editor):
    _insert_heading(editor, 1)

def title_h2(editor):
    _insert_heading(editor, 2)

def title_h3(editor):
    _insert_heading(editor, 3)

def title_h4(editor):
    _insert_heading(editor, 4)

def title_h5(editor):
    _insert_heading(editor, 5)

def title_h6(editor):
    _insert_heading(editor, 6)
