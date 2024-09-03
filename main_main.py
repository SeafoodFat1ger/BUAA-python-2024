from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from PyQt5.QtWidgets import QDesktopWidget
from qfluentwidgets import NavigationItemPosition, Theme, setTheme, FluentWindow

from qfluentwidgets import FluentIcon
from calendar_main import *
from document_main import VideoPlayer
from home_main import *
from profile_main import *
from history_main import *

class TestUpdateWorker(QObject):
    update_signal = pyqtSignal()

    def __init__(self, id):
        super().__init__()
        self.id = id
        self.update_signal.connect(self.run_update)

    def run_update(self):
        update_timer_state_database(self.id)


class window_main(FluentWindow):
    def __init__(self, id):
        super().__init__()
        # 显示缓冲窗口
        buffer_window = BufferWindow()
        buffer_window.exec_()

        self.user = None
        self.manager = None
        self.navigationInterface.setExpandWidth(120)
        self.id = id
        # 设置最初的主题
        self.curTheme = Theme.LIGHT
        self.setWindowTitle("BUAA Task schedule")
        self.setWindowIcon(QIcon("logo.png"))
        # 切换主题颜色
        self.navigationInterface.addItem(
            routeKey='click',
            icon=FluentIcon.CONSTRACT,
            text='Click',
            onClick=self.changeTheme,
            position=NavigationItemPosition.BOTTOM,
        )

        # 添加主界面
        self.homeInterface = VideoPlayer()
        self.addSubInterface(self.homeInterface, FluentIcon.HOME, '使用说明')

        self.tasklist = TodoApp(id=self.id)
        self.addSubInterface(self.tasklist, FluentIcon.LIBRARY, '任务创建')

        self.calender = calendar_main(id=self.id)
        self.addSubInterface(self.calender, FluentIcon.CALENDAR, '任务计划')

        self.history = history_main(id=self.id)
        self.addSubInterface(self.history, FluentIcon.HISTORY, '数据分析')

        self.profile = Profile(id=self.id)
        self.addSubInterface(self.profile, FluentIcon.PEOPLE, '个人信息')

        # 初始化定时器
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.handle_timeout)
        self.timer.start(5000)  # 每5秒触发一次

        # 初始化信号类
        self.worker = TestUpdateWorker(self.id)

        # 设置界面大小
        self.resize(1800, 1200)
        self.center()

    def center(self):
        # 获取屏幕的中心位置，将窗口移动到该位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def handle_timeout(self):
        self.worker.update_signal.emit()

    def switchTo(self, interface: QWidget):
        super().switchTo(interface)
        interface.resetForm()

    def changeTheme(self):
        if self.curTheme == Theme.LIGHT:
            setTheme(Theme.DARK)
            self.curTheme = Theme.DARK
        else:
            setTheme(Theme.LIGHT)
            self.curTheme = Theme.LIGHT

    class BufferWindow(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.initUI()

        def initUI(self):
            # 设置窗口大小和无边框
            self.setFixedSize(1200, 800)
            self.center()  # 窗口居中显示
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
            self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

            # 创建标签并设置图片
            label = QLabel(self)
            pixmap = QPixmap('LOGO.PNG')  # 图片路径
            label.setPixmap(pixmap.scaled(1200, 800, Qt.KeepAspectRatioByExpanding))
            label.setAlignment(Qt.AlignCenter)
            label.setGeometry(0, 0, 1200, 800)

            # 使用QTimer在2秒后关闭窗口
            QTimer.singleShot(2000, self.accept)

        def center(self):
            qr = self.frameGeometry()
            cp = QDesktopWidget().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())


class BufferWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 设置窗口大小和无边框
        self.setFixedSize(600, 400)
        self.center()  # 窗口居中显示
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明

        # 创建标签并设置图片
        label = QLabel(self)
        pixmap = QPixmap('LOGO.PNG')  # 图片路径
        label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatioByExpanding))
        label.setAlignment(Qt.AlignCenter)
        label.setGeometry(0, 0, 600, 400)

        # 使用QTimer在1秒后关闭窗口
        QTimer.singleShot(500, self.accept)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
