# utils/hx_config/file_mgr.py

import yaml
from ruamel.yaml import YAML
from qfluentwidgets import SwitchButton, PlainTextEdit

def load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error loading YAML: {str(e)}")
        return None

def save_yaml(file_path, display_data, original_data):
    try:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.width = 4096  # 防止长行被拆分

        # 提取界面中的数据
        extract_yaml_data(display_data, original_data)

        # 保存更新后的数据到原始文件
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(original_data, f)
    except Exception as e:
        print(f"Error saving YAML: {str(e)}")

def extract_yaml_data(display_data, yaml_data):
    """从界面元素中提取数据"""
    for key, widget in display_data.items():
        keys = key.split('.')
        temp_dict = yaml_data
        for sub_key in keys[:-1]:
            if sub_key not in temp_dict:
                temp_dict[sub_key] = {}
            temp_dict = temp_dict[sub_key]
        if isinstance(widget, SwitchButton):
            temp_dict[keys[-1]] = widget.isChecked()
        elif isinstance(widget, PlainTextEdit):
            temp_dict[keys[-1]] = widget.toPlainText()
