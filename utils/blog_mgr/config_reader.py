import os
from ruamel.yaml import YAML

def read_blog_config(folder_path):
    """
    从指定文件夹中的 _config.yml 文件读取配置信息
    :param folder_path: 文件夹路径
    :return: 配置信息字典，如果读取失败返回 None
    """
    # 替换路径中的反斜杠为正斜杠
    folder_path = folder_path.replace("\\", "/")
    config_path = os.path.join(folder_path, '_config.yml').replace("\\", "/")

    # 打印路径，确保路径正确
    print(f"尝试读取配置文件: {config_path}")

    if not os.path.exists(config_path):
        print(f"配置文件不存在: {config_path}")
        return None

    try:
        yaml = YAML()
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.load(file)
            print(f"成功读取配置文件: {config_path}")
            return config
    except Exception as e:
        print(f"读取 {config_path} 时出错: {e}")
        return None