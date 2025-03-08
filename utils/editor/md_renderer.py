# utils/editor/md_renderer.py
import markdown2

def convert_markdown(text):
    """将Markdown文本转换为HTML（使用markdown2库）"""
    extras = [
        'cuddled-lists',    # 支持紧凑列表
        'fenced-code-blocks',  # 支持围栏代码块（替代codehilite）
        'footnotes',       # 脚注支持
        'header-ids',      # 自动添加标题ID（替代toc扩展）
        'tables',          # 表格支持
        'task_list'        # 任务列表
    ]

    html = markdown2.markdown(
        text,
        extras=extras
    )

    return f'''
    <html>
    <head>
        <style>
            /* 原有样式保留 */
            body {{
                font-family: Segoe UI, Arial, sans-serif;
                padding: 10px;
                font-size: 14px; 
                line-height: 1.6;
            }}
            pre {{
                background: #f5f5f5;
                padding: 14px;
                border-radius: 3px;
                font-size: 12px;  
            }}
            code {{
                font-family: Consolas, monospace;
                font-size: 14px;
            }}
            img {{
                max-width: 100%;
            }}
            /* 添加markdown2特有元素的样式 */
            .task-list-item {{
                list-style-type: none;
                margin-left: -1em;
            }}
            .header-link {{
                color: #666;
                margin-left: 5px;
                visibility: hidden;
            }}
            h1:hover .header-link,
            h2:hover .header-link,
            h3:hover .header-link,
            h4:hover .header-link,
            h5:hover .header-link,
            h6:hover .header-link {{
                visibility: visible;
            }}
        </style>
    </head>
    <body>
        <div class="markdown-body">
        {html}
        </div>
    </body>
    </html>
    '''
