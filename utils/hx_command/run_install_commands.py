from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QUrl, QThread, Signal, QProcess
from PySide6.QtGui import QDesktopServices
from qfluentwidgets import InfoBar, InfoBarPosition, StateToolTip
from utils.app_settings.config import cfg
import subprocess
import os

class InstallHexoThread(QThread):
    """安装线程（使用subprocess实现）"""
    success_signal = Signal(str, str)  # 包管理器名称, 命令
    error_signal = Signal(str)
    progress_signal = Signal(str, str)  # 标题, 内容

    def __init__(self, package_mgr, command):
        super().__init__()
        self.package_mgr = package_mgr
        self.command = command
        self.working_dir = self.get_user_dir()

    def get_user_dir(self):
        """获取用户目录"""
        try:
            username = os.getenv('USERNAME') or os.getenv('USER')
            return f"C:/Users/{username}"
        except Exception as e:
            print(f"获取用户目录失败: {str(e)}")
            return os.path.expanduser("~")  # 备用方案

    def run(self):
        try:
            # 确保目录存在
            if not os.path.exists(self.working_dir):
                raise FileNotFoundError(f"目录不存在: {self.working_dir}")

            # 使用subprocess.Popen执行命令
            process = subprocess.Popen(
                self.command,
                shell=True,
                cwd=self.working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                bufsize=1  # 设置缓冲区大小为1，确保实时输出
            )

            # 捕获输出并更新状态
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
                    # 更新状态提示
                    self.progress_signal.emit(
                        "安装中...",
                        f"正在安装hexo-cli，请稍候..."
                    )

            # 捕获错误输出
            error_output = process.stderr.read()
            if error_output:
                print(f"错误输出: {error_output}")
                self.error_signal.emit(f"错误输出: {error_output}")

            # 检查退出码
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, self.command, output=error_output
                )

        except subprocess.CalledProcessError as e:
            error_msg = f"Exit code {e.returncode}\n{e.output}"
            self.error_signal.emit(error_msg)
        except Exception as e:
            self.error_signal.emit(str(e))
        else:
            self.success_signal.emit(self.package_mgr, self.command)



def get_package_manager():
    """获取当前设置的包管理器"""
    try:
        # 正确访问小写的packageMgr配置项，并获取其value值
        current_value = cfg.packageMgr.value
        print(f"[Debug] 原始配置值: {current_value} | 类型: {type(current_value)}")

        # 处理无效值
        if not current_value or not isinstance(current_value, str):
            print("[Debug] 值类型无效，使用默认值 'npm'")
            return 'npm'

        mgr = current_value.lower()
        print(f"[Debug] 处理后值: {mgr}")
        return mgr if mgr in ['npm', 'cnpm', 'pnpm'] else 'npm'

    except AttributeError:
        print("[Debug] packageMgr配置项不存在，使用默认值 'npm'")
        return 'npm'


def on_install_nodejs_clicked():
    QDesktopServices.openUrl(QUrl("https://nodejs.org/zh-cn/download/"))


def on_install_hexo_clicked():
    """根据配置执行Hexo安装"""
    mgr = get_package_manager()
    commands = {
        'npm': 'npm install -g hexo-cli',
        'cnpm': 'cnpm install -g hexo-cli',
        'pnpm': 'pnpm install -g hexo-cli'
    }

    try:
        command = commands[mgr]
    except KeyError:
        InfoBar.error(
            title='不支持的包管理器',
            content=f"无效的包管理器配置: {mgr}",
            position=InfoBarPosition.TOP_RIGHT,
            duration=5000,
            parent=QtWidgets.QApplication.activeWindow()
        )
        return

    # 创建状态提示
    window = QtWidgets.QApplication.activeWindow()
    stateTooltip = StateToolTip('正在准备安装...', '请稍后', window)
    stateTooltip.move(stateTooltip.getSuitablePos())
    stateTooltip.show()

    # 创建并启动线程
    thread = InstallHexoThread(mgr, command)

    # 信号连接
    def on_success(m, c):
        stateTooltip.setTitle('安装完成')
        stateTooltip.setContent('安装成功 🎉')
        stateTooltip.setState(True)
        # 2秒后自动关闭
        QtCore.QTimer.singleShot(10000, stateTooltip.hide)

    def on_error(e):
        stateTooltip.setTitle('安装失败')
        stateTooltip.setContent(f"错误: {e}")
        stateTooltip.setState(False)
        # 错误状态保持更长时间
        QtCore.QTimer.singleShot(5000, stateTooltip.hide)

    def on_progress(title, content):
        stateTooltip.setTitle(title)
        stateTooltip.setContent(content)

    thread.success_signal.connect(on_success)
    thread.error_signal.connect(on_error)
    thread.progress_signal.connect(on_progress)

    # 保持线程引用
    if not hasattr(window, "_install_threads"):
        window._install_threads = []
    window._install_threads.append(thread)

    thread.finished.connect(lambda: (
        window._install_threads.remove(thread)
    ))

    thread.start()