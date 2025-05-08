import os


def get_blog_folders(path):
    """
    获取指定目录下的所有文件夹名称
    :param path: 目录路径
    :return: 文件夹名称列表
    """
    print(f"Checking path: {path}")  # 调试信息
    if not os.path.exists(path):
        print(f"Path does not exist: {path}")  # 调试信息
        return []

    try:
        folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
        print(f"Found folders: {folders}")  # 调试信息
        return folders
    except PermissionError as e:
        print(f"Permission error: {e}")  # 调试信息
        return []