# components/editor/frontmatter_editor.py
from qfluentwidgets import ScrollArea,PlainTextEdit

class FrontmatterManager:
    def __init__(self):
        self.editor = PlainTextEdit()
        self.scroll_area = None
        self.is_visible = False  # 新增可见状态跟踪

    def create_editor_area(self, parent):
        self.scroll_area = ScrollArea()
        self.scroll_area.setMinimumHeight(150)
        self.scroll_area.setWidget(self.editor)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.hide()
        return self.scroll_area

    # 新增清空方法
    def clear_content(self):
        self.editor.setPlainText("")

    def set_content(self, text):
        self.editor.setPlainText(text)

    def get_content(self):
        return self.editor.toPlainText()

    def toggle_visibility(self, force=None):
        if force is not None:
            self.is_visible = force
        else:
            self.is_visible = not self.is_visible  # <--- 修改切换逻辑

        if self.scroll_area:
            self.scroll_area.setVisible(self.is_visible)
