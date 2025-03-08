# utils/editor/file_mgr.py
from PySide6.QtWidgets import QFileDialog

def open_markdown_file(parent, editor):
    path, _ = QFileDialog.getOpenFileName(
        parent, "打开文件", "", "Markdown Files (*.md)")
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            editor.setPlainText(f.read())

def save_markdown_file(parent, editor):
    path, _ = QFileDialog.getSaveFileName(
        parent, "保存文件", "", "Markdown Files (*.md)")
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(editor.toPlainText())
