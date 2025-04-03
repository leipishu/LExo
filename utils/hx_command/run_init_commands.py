# run_init_commands.py
from PySide6 import QtWidgets
from PySide6.QtCore import QThread, Signal, QTimer
from PySide6.QtWidgets import QApplication
from qfluentwidgets import StateToolTip
from utils.app_settings.config import cfg
import subprocess
import os
from pathlib import Path

class InitHexoThread(QThread):
    success_signal = Signal(str)  # 成功信号
    error_signal = Signal(str)    # 错误信号
    progress_signal = Signal(str)  # 进度更新

    def __init__(self, blog_name, parent=None):
        super().__init__(parent)
        self.blog_name = blog_name
        self.working_dir = Path(cfg.downloadFolder.value)

    def run(self):
        try:
            if not self.blog_name:
                raise ValueError("博客名称不能为空")

            # 创建目标目录
            target_dir = self.working_dir / self.blog_name
            target_dir.mkdir(parents=True, exist_ok=True)

            # 执行命令
            command = f"hexo init {self.blog_name}"
            process = subprocess.Popen(
                command,
                cwd=str(self.working_dir),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    self.progress_signal.emit(output.strip())

            if process.returncode != 0:
                error = process.stderr.read()
                raise subprocess.CalledProcessError(process.returncode, command, error)

            self.success_signal.emit(f"博客 {self.blog_name} 初始化成功！")

        except Exception as e:
            self.error_signal.emit(str(e))

class EmergencyInstallThread(QThread):
    success_signal = Signal(str)  # 成功信号
    error_signal = Signal(str)    # 错误信号
    progress_signal = Signal(str) # 进度更新

    def __init__(self, target_dir, parent=None):
        super().__init__(parent)
        self.target_dir = target_dir

    def run(self):
        try:
            # 确保目录存在
            os.makedirs(self.target_dir, exist_ok=True)

            # 获取配置中的包管理器
            package_manager = getattr(cfg, "packageMgr", None)
            if package_manager is not None:
                package_manager = package_manager.value  # 获取 packageMgr 的值
            else:
                package_manager = "npm"  # 默认使用 npm

            # 构建命令
            command = f"{package_manager} install"
            self.progress_signal.emit(f"正在使用 {package_manager} 安装依赖...")

            # 执行命令
            process = subprocess.Popen(
                command,
                cwd=self.target_dir,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            while True:
                output = process.stdout.readline()
                if not output and process.poll() is not None:
                    break
                if output:
                    self.progress_signal.emit(output.strip())

            if process.returncode != 0:
                error = process.stderr.read()
                raise subprocess.CalledProcessError(process.returncode, command, error)

            self.success_signal.emit(f"依赖安装成功！")

        except Exception as e:
            # 打印详细的错误信息
            print(f"Error in EmergencyInstallThread: {str(e)}")
            self.error_signal.emit(str(e))

def on_init_clicked(parent):
    """处理初始化按钮点击"""
    try:
        # 获取博客名称
        blog_name = parent.init_line_edit.text().strip()

        # 创建状态提示（关键修改：使用parent作为父级控件）
        window = QtWidgets.QApplication.activeWindow()
        state_tooltip = StateToolTip(
            title='初始化中',
            content='正在准备...',
            parent=window
        )

        # 设置出现在右上角
        state_tooltip.move(state_tooltip.getSuitablePos())
        state_tooltip.show()

        # 创建线程
        thread = InitHexoThread(blog_name)

        # 信号连接
        def on_success(message):
            state_tooltip.setTitle('完成')
            state_tooltip.setContent(message)
            state_tooltip.setState(True)
            # 2秒后自动关闭
            QTimer.singleShot(2000, state_tooltip.hide)

        def on_error(error):
            state_tooltip.setTitle('错误')
            state_tooltip.setContent(str(error))
            state_tooltip.setState(False)
            # 5秒后自动关闭
            QTimer.singleShot(5000, state_tooltip.hide)

        thread.success_signal.connect(on_success)
        thread.error_signal.connect(on_error)

        # 进度更新处理
        def on_progress():
            state_tooltip.setContent(f"正在初始化博客 {blog_name} 中...")

        thread.progress_signal.connect(on_progress)

        # 启动线程
        thread.start()

        # 保持线程引用
        if not hasattr(parent, '_init_threads'):
            parent._init_threads = []
        parent._init_threads.append(thread)

    except Exception as e:
        tooltip = StateToolTip(
            title='初始化错误',
            content=str(e),
            parent=parent
        )
        tooltip.setState(False)
        tooltip.show()

def on_emergency_clicked(parent):
    """处理紧急安装按钮点击"""
    try:
        # 获取博客名称
        blog_name = parent.init_line_edit.text().strip()

        if not blog_name:
            StateToolTip(
                title='安装错误',
                content='请输入有效的博客名称',
                parent=parent
            ).show()
            return

        # 构建目标目录路径
        download_folder = getattr(cfg, "downloadFolder", None)
        if download_folder is not None:
            download_folder = download_folder.value  # 获取 downloadFolder 的值
        else:
            download_folder = os.getcwd()  # 默认使用当前工作目录

        target_dir = os.path.join(download_folder, blog_name)

        # 检查目录是否存在，如果不存在则创建
        os.makedirs(target_dir, exist_ok=True)

        # 创建状态提示
        window = QApplication.activeWindow()
        state_tooltip = StateToolTip(
            title='安装中',
            content='正在准备...',
            parent=window
        )
        state_tooltip.move(state_tooltip.getSuitablePos())
        state_tooltip.show()

        # 创建线程
        thread = EmergencyInstallThread(target_dir)

        # 信号连接
        def on_success(message):
            state_tooltip.setTitle('完成')
            state_tooltip.setState(True)
            state_tooltip.setContent(message)
            QTimer.singleShot(2000, state_tooltip.hide)

        def on_error(error):
            state_tooltip.setTitle('错误')
            state_tooltip.setState(False)
            state_tooltip.setContent(str(error))
            QTimer.singleShot(5000, state_tooltip.hide)

        thread.success_signal.connect(on_success)
        thread.error_signal.connect(on_error)

        # 进度更新处理
        def on_progress(message):
            state_tooltip.setContent(message)

        thread.progress_signal.connect(on_progress)

        # 启动线程
        thread.start()

        # 保持线程引用
        if not hasattr(parent, '_emergency_threads'):
            parent._emergency_threads = []
        parent._emergency_threads.append(thread)

    except Exception as e:
        # 打印详细的错误信息
        print(f"Error in on_emergency_clicked: {str(e)}")
        # 显示错误提示
        tooltip = StateToolTip(
            title='安装错误',
            content=str(e),
            parent=parent
        )
        tooltip.setState(False)
        tooltip.show()