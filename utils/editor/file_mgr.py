from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition, InfoBarIcon
import re
from pathlib import Path

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
        try:
            _save_content(editor_page.current_file_path, editor, editor_page.frontmatter_manager)
            # 显示保存成功的提示
            InfoBar.success(
                title='保存成功',
                content="文件已成功保存。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
        except Exception as e:
            # 显示保存失败的提示
            InfoBar.error(
                title='保存失败',
                content=f"文件保存失败: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
    else:
        path, _ = QFileDialog.getSaveFileName(
            parent, "保存文件", "", "Markdown Files (*.md)")
        if path:
            try:
                _save_content(path, editor, editor_page.frontmatter_manager)
                editor_page.current_file_path = path
                # 显示保存成功的提示
                InfoBar.success(
                    title='保存成功',
                    content="文件已成功保存。",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )
            except Exception as e:
                # 显示保存失败的提示
                InfoBar.error(
                    title='保存失败',
                    content=f"文件保存失败: {str(e)}",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )

def save_as_markdown_file(parent, editor, editor_page):
    path, _ = QFileDialog.getSaveFileName(
        parent, "另存为", "", "Markdown Files (*.md)")
    if path:
        try:
            _save_content(path, editor, editor_page.frontmatter_manager)
            # 显示另存为成功的提示
            InfoBar.success(
                title='另存为成功',
                content="文件已成功另存为。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
        except Exception as e:
            # 显示另存为失败的提示
            InfoBar.error(
                title='另存为失败',
                content=f"文件另存为失败: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )

def save_copy_markdown_file(parent, editor, editor_page):
    def save_copy(path):
        """内部保存副本逻辑"""
        try:
            file_path = Path(path)
            file_name = file_path.stem
            file_extension = file_path.suffix
            file_dir = file_path.parent

            # 保存第一份文件
            _save_content(path, editor, editor_page.frontmatter_manager)

            # 保存第二份副本
            second_path = file_dir / f"{file_name}-2{file_extension}"
            _save_content(second_path, editor, editor_page.frontmatter_manager)

            # 显示保存并复制成功的提示
            InfoBar.success(
                title='保存并复制成功',
                content="文件已成功保存并复制。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
        except Exception as e:
            # 显示保存并复制失败的提示
            InfoBar.error(
                title='保存并复制失败',
                content=f"文件保存并复制失败: {str(e)}",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )

    if not editor_page.current_file_path:
        path, _ = QFileDialog.getSaveFileName(
            parent, "保存复制", "", "Markdown Files (*.md)")
        if path:
            save_copy(path)
            editor_page.current_file_path = path
    else:
        save_copy(editor_page.current_file_path)