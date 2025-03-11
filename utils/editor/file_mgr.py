# utils/editor/file_mgr.py
from PySide6.QtWidgets import QFileDialog
import re

def extract_frontmatter(content):
    """提取frontmatter内容和正文"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, content

def open_markdown_file(parent, editor, editor_page):
    path, _ = QFileDialog.getOpenFileName(
        parent, "打开文件", "", "Markdown Files (*.md)")
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            full_content = f.read()

        # 解析frontmatter
        frontmatter, body = extract_frontmatter(full_content)

        # 设置编辑器内容
        editor.setPlainText(body)

        # 设置frontmatter
        if frontmatter:
            editor_page.frontmatter_manager.set_content(frontmatter)
            editor_page.frontmatter_manager.toggle_visibility(True)
        else:
            # 新增清空操作
            editor_page.frontmatter_manager.set_content("")  # 清空内容
            editor_page.frontmatter_manager.toggle_visibility(False)  # 隐藏

        editor_page.current_file_path = path


def _save_content(path, editor, frontmatter_manager):
    """统一保存逻辑"""
    body = editor.toPlainText().strip()
    frontmatter = frontmatter_manager.get_content().strip()

    # 组装最终内容
    final_content = ""
    if frontmatter:
        final_content = f"---\n{frontmatter}\n---\n\n{body}"
    else:
        final_content = body

    with open(path, 'w', encoding='utf-8') as f:
        f.write(final_content)

def save_markdown_file(parent, editor, editor_page):
    if editor_page.current_file_path:
        _save_content(editor_page.current_file_path, editor, editor_page.frontmatter_manager)
    else:
        path, _ = QFileDialog.getSaveFileName(
            parent, "保存文件", "", "Markdown Files (*.md)")
        if path:
            _save_content(path, editor, editor_page.frontmatter_manager)
            editor_page.current_file_path = path

def save_as_markdown_file(parent, editor, frontmatter_manager):
    path, _ = QFileDialog.getSaveFileName(
        parent, "另存为", "", "Markdown Files (*.md)")
    if path:
        _save_content(path, editor, frontmatter_manager)

def save_copy_markdown_file(parent, editor, editor_page):
    def save_copy(path):
        """内部保存副本逻辑"""
        from pathlib import Path
        file_path = Path(path)
        file_name = file_path.stem
        file_extension = file_path.suffix
        file_dir = file_path.parent

        # 保存第一份文件
        _save_content(path, editor, editor_page.frontmatter_manager)

        # 保存第二份副本
        second_path = file_dir / f"{file_name}-2{file_extension}"
        _save_content(second_path, editor, editor_page.frontmatter_manager)

    if not editor_page.current_file_path:
        path, _ = QFileDialog.getSaveFileName(
            parent, "保存复制", "", "Markdown Files (*.md)")
        if path:
            save_copy(path)
            editor_page.current_file_path = path
    else:
        save_copy(editor_page.current_file_path)
