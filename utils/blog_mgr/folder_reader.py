import os


def get_blog_folders(path):
    """
    获取指定目录下的所有文件夹名称
    :param path: 目录路径
    :return: 文件夹名称列表
    """
    if not os.path.exists(path):
        return []

    try:
        folders = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
        return folders
    except PermissionError as e:
        return []