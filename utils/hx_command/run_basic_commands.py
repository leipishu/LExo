import os
from PySide6.QtCore import Qt
from qfluentwidgets import InfoBar, InfoBarPosition
import subprocess

def hexo_three_link_clicked(parent):
    """执行hexo三连操作"""
    try:
        selected_path = parent.init_line_edit.text() if parent.init_line_edit.text() else parent.current_file_path

        if not selected_path:
            InfoBar.warning(
                title='Hexo三连',
                content="请选择或输入博客路径",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        abs_path = os.path.abspath(os.path.join("app/sites", selected_path))
        if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
            InfoBar.warning(
                title='Hexo三连',
                content="指定的路径不存在或不是一个有效的目录。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        subprocess.run(["hexo", "clean"], cwd=abs_path,shell=True, check=True)
        subprocess.run(["hexo", "generate"], cwd=abs_path,shell=True, check=True)
        subprocess.run(["hexo", "server"], cwd=abs_path,shell=True, check=True)
        InfoBar.success(
            title='Hexo三连',
            content="执行了 Hexo 三连操作。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except FileNotFoundError:
        InfoBar.error(
            title='Hexo三连',
            content="系统找不到指定的文件。请确保Hexo已正确安装。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except subprocess.CalledProcessError:
        InfoBar.error(
            title='Hexo三连',
            content="Hexo命令执行失败。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )

def clear_cache_clicked(parent):
    """清除缓存操作"""
    try:
        selected_path = parent.init_line_edit.text() if parent.init_line_edit.text() else parent.current_file_path
        if not selected_path:
            InfoBar.warning(
                title='清除缓存',
                content="请选择或输入博客路径",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        abs_path = os.path.abspath(os.path.join("app/sites", selected_path))
        if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
            InfoBar.warning(
                title='清除缓存',
                content="指定的路径不存在或不是一个有效的目录。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        subprocess.run(["hexo", "clean"], cwd=abs_path, shell=True, check=True)
        InfoBar.info(
            title='清除缓存',
            content="缓存清除操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except FileNotFoundError:
        InfoBar.error(
            title='清除缓存',
            content="系统找不到指定的文件。请确保Hexo已正确安装。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except subprocess.CalledProcessError:
        InfoBar.error(
            title='清除缓存',
            content="清除缓存命令执行失败。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )

def generate_files_clicked(parent):
    """生成文件操作"""
    try:
        selected_path = parent.init_line_edit.text() if parent.init_line_edit.text() else parent.current_file_path
        if not selected_path:
            InfoBar.warning(
                title='生成文件',
                content="请选择或输入博客路径",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        abs_path = os.path.abspath(os.path.join("app/sites", selected_path))
        if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
            InfoBar.warning(
                title='生成文件',
                content="指定的路径不存在或不是一个有效的目录。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        subprocess.run(["hexo", "generate"], cwd=abs_path, shell=True, check=True)
        InfoBar.info(
            title='生成文件',
            content="文件生成操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except FileNotFoundError:
        InfoBar.error(
            title='生成文件',
            content="系统找不到指定的文件。请确保Hexo已正确安装。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except subprocess.CalledProcessError:
        InfoBar.error(
            title='生成文件',
            content="生成文件命令执行失败。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )

def local_service_clicked(parent):
    """本地服务操作"""
    try:
        selected_path = parent.init_line_edit.text() if parent.init_line_edit.text() else parent.current_file_path
        port = parent.service_edit.text()
        if not selected_path or not port:
            if not selected_path:
                InfoBar.warning(
                    title='本地服务',
                    content="请选择或输入博客路径",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )
            else:
                InfoBar.warning(
                    title='本地服务',
                    content="请输入服务地址",
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP_RIGHT,
                    duration=2000,
                    parent=parent
                )
            return

        abs_path = os.path.abspath(os.path.join("app/sites", selected_path))
        if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
            InfoBar.warning(
                title='本地服务',
                content="指定的路径不存在或不是一个有效的目录。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        subprocess.run(["hexo", "server", "-p", port], cwd=abs_path,shell=True, check=True)
        InfoBar.info(
            title='本地服务',
            content=f"服务端口: {port}",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except FileNotFoundError:
        InfoBar.error(
            title='本地服务',
            content="系统找不到指定的文件。请确保Hexo已正确安装。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except subprocess.CalledProcessError:
        InfoBar.error(
            title='本地服务',
            content="本地服务命令执行失败。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )

def deploy_clicked(parent):
    """部署操作"""
    try:
        selected_path = parent.init_line_edit.text() if parent.init_line_edit.text() else parent.current_file_path
        if not selected_path:
            InfoBar.warning(
                title='部署',
                content="请选择或输入博客路径",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        abs_path = os.path.abspath(os.path.join("app/sites", selected_path))
        if not os.path.exists(abs_path) or not os.path.isdir(abs_path):
            InfoBar.warning(
                title='部署',
                content="指定的路径不存在或不是一个有效的目录。",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2000,
                parent=parent
            )
            return

        subprocess.run(["hexo", "deploy"], cwd=abs_path,shell=True, check=True)
        InfoBar.info(
            title='部署',
            content="部署操作已执行。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except FileNotFoundError:
        InfoBar.error(
            title='部署',
            content="系统找不到指定的文件。请确保Hexo已正确安装。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )
    except subprocess.CalledProcessError:
        InfoBar.error(
            title='部署',
            content="部署命令执行失败。",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=parent
        )