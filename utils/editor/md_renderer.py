from markdown import markdown

def convert_markdown(text):
    """将Markdown文本转换为HTML"""
    html = markdown(text, extensions=[
        'extra',
        'codehilite',
        'toc'
    ])
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
                font-size: 14px;  #
            }}
            img {{
                max-width: 100%;
            }}
        </style>
    </head>
    <body>{html}</body>
    </html>
    '''
