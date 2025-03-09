import markdown2
import requests
from base64 import b64encode

def convert_markdown(text):
    """将Markdown文本转换为HTML（使用markdown2库）"""
    extras = [
        'cuddled-lists',  # 支持紧凑列表
        'fenced-code-blocks',  # 支持围栏代码块
        'footnotes',  # 脚注支持
        'header-ids',  # 自动添加标题ID
        'tables',  # 表格支持
        'task_list'  # 任务列表
    ]

    # 将 Markdown 转换为 HTML
    html = markdown2.markdown(text, extras=extras)

    # 替换图片 URL 为 Base64 编码
    import re
    def replace_image_url(match):
        url = match.group(1)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                base64_data = b64encode(response.content).decode('utf-8')
                return f'data:image/jpeg;base64,{base64_data}'
            else:
                return url  # 如果无法加载图片，保留原始 URL
        except Exception as e:
            print(f"Error loading image {url}: {e}")
            return url  # 如果发生错误，保留原始 URL

    html = re.sub(r'src="([^"]+)"', lambda match: f'src="{replace_image_url(match)}"', html)

    return f'''
    <html>
    <head>
        <style>
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
                max-width: 60%;  # 调整为最大宽度60%
                height: auto;
                display: block;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 4px;
                margin: 5px 0;  # 修改边距为上下5px
                border: 1px solid #eee;  # 添加浅色边框
            }}
            h1 {{
                font-size: 28px;
                font-weight: bold;
                margin: 20px 0 10px;
            }}
            h2 {{
                font-size: 24px;
                font-weight: bold;
                margin: 18px 0 10px;
            }}
            h3 {{
                font-size: 20px;
                font-weight: bold;
                margin: 16px 0 10px;
            }}
            h4 {{
                font-size: 18px;
                font-weight: bold;
                margin: 14px 0 10px;
            }}
            h5 {{
                font-size: 16px;
                font-weight: bold;
                margin: 12px 0 10px;
            }}
            h6 {{
                font-size: 14px;
                font-weight: bold;
                margin: 10px 0 10px;
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