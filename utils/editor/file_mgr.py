# utils/editor/file_mgr.py
from PySide6.QtWidgets import QFileDialog

# file_mgr.py 修改部分
def open_markdown_file(parent, editor, editor_page):
    path, _ = QFileDialog.getOpenFileName(
        parent, "打开文件", "", "Markdown Files (*.md)")
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            editor.setPlainText(f.read())
        editor_page.current_file_path = path  # 记录打开路径

def save_markdown_file(parent, editor, editor_page):
    if editor_page.current_file_path:
        # 直接保存到已有路径
        with open(editor_page.current_file_path, 'w', encoding='utf-8') as f:
            f.write(editor.toPlainText())
    else:
        # 首次保存弹出对话框
        path, _ = QFileDialog.getSaveFileName(
            parent, "保存文件", "", "Markdown Files (*.md)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            editor_page.current_file_path = path  # 记录新保存路径

def save_as_markdown_file(parent, editor):
    path, _ = QFileDialog.getSaveFileName(
        parent, "另存为", "", "Markdown Files (*.md)")
    if path:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(editor.toPlainText())

def save_copy_markdown_file(parent, editor, editor_page):
    if not editor_page.current_file_path:
        # 如果尚未保存过，弹出对话框让用户选择保存路径
        path, _ = QFileDialog.getSaveFileName(
            parent, "保存复制", "", "Markdown Files (*.md)"
        )
        if path:
            # 获取文件名和路径
            from pathlib import Path
            file_path = Path(path)
            file_name = file_path.stem
            file_extension = file_path.suffix
            file_dir = file_path.parent

            # 第一份文件
            first_file_path = file_path
            with open(first_file_path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())

            # 第二份文件
            second_file_name = f"{file_name}-2{file_extension}"
            second_file_path = file_dir / second_file_name
            with open(second_file_path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())

            # 更新当前文件路径
            editor_page.current_file_path = str(first_file_path)
    else:
        # 如果已经保存过，直接在当前路径下保存两份文件
        from pathlib import Path
        current_path = Path(editor_page.current_file_path)
        file_name = current_path.stem
        file_extension = current_path.suffix
        file_dir = current_path.parent

        # 第一份文件（覆盖原文件）
        with open(current_path, 'w', encoding='utf-8') as f:
            f.write(editor.toPlainText())

        # 第二份文件
        second_file_name = f"{file_name}-2{file_extension}"
        second_file_path = file_dir / second_file_name
        with open(second_file_path, 'w', encoding='utf-8') as f:
            f.write(editor.toPlainText())