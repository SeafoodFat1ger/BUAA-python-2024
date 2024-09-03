import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QSlider, QPushButton, QSplitter, QScrollArea)
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, Qt
import cv2

from document_ui import Ui_document


class VideoPlayer(Ui_document, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('【用户手册】')

    def initUI(self):
        self.setWindowTitle('Video Player')
        self.setGeometry(100, 100, 1000, 700)

        # 创建主布局
        self.main_layout = QHBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        # 创建文档说明标签并设置内容
        self.doc_label = QLabel(self)
        self.doc_label.setText(
            "<h1 style='font-size: 56px; position: relative; top: -20px;'>用户使用文档</h1><br>"
            "<h2>使用环境说明</h2>"
            "<p> 为实现图像长期储存，需要您<span style='color: red; font-size: 48px; font-weight: bold;'>科学上网</span>。</p>"
            "<h2>任务创建</h2>"
            "<p>1. 该界面有<span style='color: red'>创建、修改、删除、筛选</span>任务功能，并可以对任务进行<span style='color: red'>打勾</span>。</p>"
            "<p>2. 任务栏显示每个任务的大致信息，<span style='color: red'>标红代表紧急任务</span>，通常为今天需要完成且优先级较高的任务。</p>"
            "<p>3. 新增任务键在界面底部，可以在弹出的窗口中输入任务标题、描述、任务类型、优先级（数字越大优先级越高）、任务用时、是否为日常任务。"
            "<span style='color: red'>日常任务是从起始日期到结束日期每天都要做的任务，普通任务是只在截止日期这天需要做的任务</span>。</p>"
            "<p>4. <span style='color: red'>批量导入</span>键也在界面底部，您可以通过上传txt文件来批量导入任务，"
            "<span style='color: red'>文件内容为多行形如\"Task1\",\"Description1\",\"1\",\"工作\""
            ",\"2024/07/20\",\"2\",\"未启动\"的语句</span>，其中第一个数字代表任务优先级，第二个数字代表任务用时。"
            "<span style='color: red'>注意：日期必须输入为\"yyyy/mm/dd\"的形式，年、月、日分别占4、2、2位，不足位用0补齐</span>。"
            "<p>5. 编辑任务键在每个任务栏右侧，<span style='color: red'>不能对已过期和已完成的任务进行编辑</span>。可以修改任务标题、描述、任务类型、优先级、用时，"
            "<span style='color: red'>日常任务不可以修改日期，也不可修改为普通任务；普通任务可以修改日期，但修改后的日期不可以早于今天，普通任务不可以修改为日常任务</span>。</p>"
            "<p>6. 删除任务键在每个任务栏右侧，可以删除任何任务。</p>"
            "<p>7. 筛选任务在界面上端，可以筛选指定时间段、优先级、类型、状态的任务。选定起始时间不得晚于终止时间。"
            "点确定键进行筛选，点重置键进行重置，显示所有任务。</p>"
            "<p>8. 点击每个任务栏左侧的方框，可给任务打勾，表示已经完成此任务，该任务会变绿后恢复黑色。"
            "<span style='color: red'>只能对正在进行和未启动的任务打勾。打勾后任务状态变为已完成，且不可撤销</span>。</p>"
            "<h2>任务计划</h2>"
            "<p>1. 该界面可以查看某天的所有任务，并能以一定的任务调度方式自动安排该天的任务计划，同时可以<span style='color: red'>把调度表和任务表导出</span>。</p>"
            "<p>2. 先在日历上选中某日，点击查看任务按钮，可在右侧视图中<span style='color: red'>查看该天的所有任务</span>。点击任意任务能查看任务详情界面，"
            "包含任务标题、描述、重要性、是否为普通任务、类型、截止日期、用时、状态。</p>"
            "<p>3. 先在日历上选中某日，点击调度任务按钮，并选择短作业优先调度、优先级优先调度、自定义比例等不同任务调度方式后，"
            "点击确定会在右侧视图看到<span style='color: red'>系统以指定调度方式为您安排的该天任务计划</span>。若无法安排下所有任务，<span style='color: red'>会提示您该天任务过多</span>，需要舍弃或修改部分任务。点击任务仍能进入任务详情页。</p>"
            "<p>4. 点击右侧下端的导出键，可以把某天的调度任务表或全部任务表导出到指定文件。</p>"
            "<p>5. 点击上端可选择不同月、年，点击今天按钮可快速回到当月。</p>" 
            "<h2>数据分析</h2>"
            "<p>1. 该界面可对<span style='color: red'>过往任务数据</span>进行统计，并以柱状图、饼状图可视化呈现。</p>"
            "<p>2. 点击日、周、月可选择当天、当周、当月，点击前后键可翻看不同日、周、月。也可在自定义中选择某一连续的时间段，但选定的起始时间不可晚于终止时间。</p>"
            "<p>3. 确定日期后，点击类型或状态，就可根据类型或状态查看该时间段的任务情况。</p>"
            "<h2>个人信息</h2>"
            "<p>1. 该界面显示您的个人信息，包括头像、账号、昵称、邮箱、工作时间等，<span style='color: red'>工作时间可以由您指定</span>，我们会在每天的这段工作时间内为您安排任务计划。</p>"
            "<p>2. 您可以通过点击切换头像、编辑资料来切换头像或修改个人信息，上传头像照片后长期储存该照片，但需要您科学上网。</p>"
        )
        self.doc_label.setWordWrap(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.doc_label)
        self.scroll_area.setWidgetResizable(True)

        # 将滚动区域添加到 splitter 的左侧
        splitter.addWidget(self.scroll_area)

        # 创建视频布局
        self.video_layout = QVBoxLayout()

        self.video_layout.addStretch()

        # 视频显示组件
        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setFixedSize(800, 700)
        self.video_layout.addWidget(self.video_label)

        self.video_layout.addStretch()

        # 创建播放控制按钮
        self.play_button = QPushButton('播放/暂停', self)
        self.play_button.clicked.connect(self.toggle_play)
        self.video_layout.addWidget(self.play_button)

        # 创建进度滑动条
        self.position_slider = QSlider(Qt.Horizontal, self)
        self.position_slider.sliderPressed.connect(self.pause_video)
        self.position_slider.sliderReleased.connect(self.resume_video)
        self.position_slider.sliderMoved.connect(self.update_slider_position)
        self.video_layout.addWidget(self.position_slider)

        video_container = QWidget()
        video_container.setLayout(self.video_layout)

        splitter.addWidget(video_container)

        # 设置 splitter 初始比例
        splitter.setSizes([500, 500])

        self.main_layout.addWidget(splitter)

        self.setLayout(self.main_layout)

        # 初始化视频捕捉
        self.cap = cv2.VideoCapture('test.mp4')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # 获取视频总帧数，显示视频第一帧
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.position_slider.setRange(0, self.total_frames - 1)
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(image))

        # 视频初始状态为暂停
        self.playing = False

    def toggle_play(self):
        if self.playing:
            self.timer.stop()
        else:
            self.timer.start(30)
        self.playing = not self.playing

    def pause_video(self):
        self.timer.stop()

    def resume_video(self):
        self.set_position(self.position_slider.value())
        if self.playing:
            self.timer.start(30)

    def update_slider_position(self, position):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(image))

    def set_position(self, position):
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
        self.update_frame()

    def update_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(image))
                current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.position_slider.setValue(current_frame)
            else:
                self.timer.stop()
                self.cap.release()

    def resetForm(self):
        print("切换到文档页面")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
