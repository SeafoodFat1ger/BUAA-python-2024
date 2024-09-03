import sys

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QMessageBox, QDialog, QPushButton
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pyecharts.charts import Pie, Bar
from pyecharts import options as opts

from database import get_task_list_database
from history_ui import Ui_history
from qfluentwidgets import ZhDatePicker, PushButton, LargeTitleLabel

from task import *

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时的负号'-'显示为方块的问题


class history_main(Ui_history, QWidget):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 例子任务数据
        tasks = []
        self.tasks = tasks
        self.id = id
        self.selectBegin = QDate.currentDate().toString('yyyy/MM/dd')
        self.selectEnd = QDate.currentDate().toString('yyyy/MM/dd')
        self.chart_type = 'type'
        self.initUI()

    def initUI(self):
        self.setWindowTitle('数据统计')

        self.current_period = 'day'
        self.current_date = QDate.currentDate()

        main_layout = QVBoxLayout()

        # 标题和导航按钮
        self.title_layout = QHBoxLayout()

        self.prev_button = PushButton('<')
        self.next_button = PushButton('>')
        self.date_label = LargeTitleLabel(
            f'历史数据统计 {self.current_date.toString("yyyy/MM/dd")} - {self.current_date.toString("yyyy/MM/dd")}')
        self.date_label.setAlignment(Qt.AlignLeft)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.date_label.setFont(font)
        self.date_label.setAlignment(Qt.AlignLeft)  # 修改为左对齐

        self.title_layout.addWidget(self.date_label, 1)
        self.title_layout.addStretch(1)
        self.title_layout.addWidget(self.prev_button)
        self.title_layout.addWidget(self.next_button)

        main_layout.addLayout(self.title_layout)

        # 日、周、月、自定义按钮
        period_layout = QHBoxLayout()
        period_layout.setSpacing(10)

        self.day_button = PushButton('日')
        self.week_button = PushButton('周')
        self.month_button = PushButton('月')
        self.custom_button = PushButton('自定义')

        buttons = [self.day_button, self.week_button, self.month_button, self.custom_button]
        for button in buttons:
            button.setCheckable(True)
            button.setFixedSize(80, 40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.day_button.setChecked(True)  # 默认选中“日”

        self.updateButtonStyles()

        period_layout.addStretch(1)
        period_layout.addWidget(self.day_button)
        period_layout.addWidget(self.week_button)
        period_layout.addWidget(self.month_button)
        period_layout.addWidget(self.custom_button)
        period_layout.addStretch(1)

        main_layout.addLayout(period_layout)

        # 图表区域
        chart_layout = QHBoxLayout()

        self.figure_pie = plt.figure()
        self.canvas_pie = FigureCanvas(self.figure_pie)
        self.canvas_pie.setStyleSheet("border: 1px solid black;")

        self.figure_bar = plt.figure()
        self.canvas_bar = FigureCanvas(self.figure_bar)
        self.canvas_bar.setStyleSheet("border: 1px solid black;")

        chart_layout.addWidget(self.canvas_pie)
        chart_layout.addWidget(self.canvas_bar)

        main_layout.addLayout(chart_layout)

        # 底部按钮
        bottom_layout = QHBoxLayout()

        self.type_button = QPushButton('按照类型数据分析')
        self.type_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CAfAf;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                font-size: 15px;
                                                padding: 10px 20px;
                                            }
                                        """)
        self.new_window_button1 = PushButton('点击查看详情')
        self.new_window_button1.setStyleSheet("background-color: rgba(255, 255, 255, 0);color:#4CAfAf")

        self.left_group_layout = QHBoxLayout()
        self.left_group_layout.addStretch(1)
        self.left_group_layout.addWidget(self.type_button)
        self.left_group_layout.addWidget(self.new_window_button1)
        self.status_button = QPushButton('按照状态数据分析')
        self.status_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CAfAf;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                font-size: 15px;
                                                padding: 10px 20px;
                                            }
                                        """)
        self.new_window_button2 = PushButton('点击查看详情')
        self.new_window_button2.setStyleSheet("background-color: rgba(255, 255, 255, 0);color:#4CAfAf")

        self.right_group_layout = QHBoxLayout()
        self.right_group_layout.addStretch(1)
        self.right_group_layout.addWidget(self.status_button)
        self.right_group_layout.addWidget(self.new_window_button2)


        bottom_layout.addLayout(self.left_group_layout)
        bottom_layout.addLayout(self.right_group_layout)


        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        self.setupConnections()

    def setupConnections(self):
        self.prev_button.clicked.connect(self.prevPeriod)
        self.next_button.clicked.connect(self.nextPeriod)
        self.day_button.clicked.connect(lambda: self.selectPeriod('day'))
        self.week_button.clicked.connect(lambda: self.selectPeriod('week'))
        self.month_button.clicked.connect(lambda: self.selectPeriod('month'))
        self.custom_button.clicked.connect(lambda: self.selectPeriod('custom'))
        self.type_button.clicked.connect(lambda: self.showChart('type'))
        self.status_button.clicked.connect(lambda: self.showChart('status'))
        self.new_window_button1.clicked.connect(self.openNewWindow1)
        self.new_window_button2.clicked.connect(self.openNewWindow2)

    def openNewWindow1(self):
        tasks = get_task_list_database(self.id)

        # 筛选符合条件的任务
        filtered_tasks = []
        for task in tasks:
            task_date_str = task.ddl
            if self.selectBegin <= task_date_str <= self.selectEnd and task.state != TASK_NOTSTART:
                filtered_tasks.append(task)

        self.tasks = filtered_tasks

        if not self.tasks:
            QMessageBox.warning(self, '操作无效', '当前时间段无历史记录')
            return

        self.new_window1 = QDialog(flags=Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
        self.new_window1.setWindowIcon(QIcon('logo.png'))
        self.new_window1.setWindowTitle("html")
        self.new_window1.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()
        self.web_view = QWebEngineView()

        if self.chart_type == 'type':
            self.chart_html1 = self.plotTypePie()
        else:
            self.chart_html1 = self.plotStatusPie()

        self.web_view.setHtml(self.chart_html1)

        self.layout.addWidget(self.web_view)
        self.new_window1.setLayout(self.layout)
        self.new_window1.show()

    def plotTypePie(self):
        type_count = {}
        for task in self.tasks:
            if task.type in type_count:
                type_count[task.type] += 1
            else:
                type_count[task.type] = 1

        pie = (
            Pie()
            .add("", [list(z) for z in zip(type_count.keys(), type_count.values())])
            .set_global_opts(title_opts=opts.TitleOpts(title="任务类型饼状图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return pie.render_embed()

    def plotStatusPie(self):
        status_count = {}
        for task in self.tasks:
            if task.state in status_count:
                status_count[task.state] += 1
            else:
                status_count[task.state] = 1

        pie = (
            Pie()
            .add("", [list(z) for z in zip(status_count.keys(), status_count.values())])
            .set_global_opts(title_opts=opts.TitleOpts(title="任务状态饼状图"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        return pie.render_embed()

    def plotTypeBar(self):
        type_count = {}
        for task in self.tasks:
            if task.type in type_count:
                type_count[task.type] += 1
            else:
                type_count[task.type] = 1
        bar = (
            Bar()
            .add_xaxis(list(type_count.keys()))
            .add_yaxis("数量", list(type_count.values()))
            .set_global_opts(title_opts=opts.TitleOpts(title="任务类型柱状图"))
        )
        return bar.render_embed()
    def plotStatusBar(self):
        status_count = {}
        for task in self.tasks:
            if task.state in status_count:
                status_count[task.state] += 1
            else:
                status_count[task.state] = 1
        bar = (
            Bar()
            .add_xaxis(list(status_count.keys()))
            .add_yaxis("数量", list(status_count.values()))
            .set_global_opts(title_opts=opts.TitleOpts(title="任务状态柱状图"))
        )
        return bar.render_embed()

    def openNewWindow2(self):
        tasks = get_task_list_database(self.id)

        # 筛选符合条件的任务
        filtered_tasks = []
        for task in tasks:
            task_date_str = task.ddl
            if self.selectBegin <= task_date_str <= self.selectEnd and task.state != TASK_NOTSTART:
                filtered_tasks.append(task)

        self.tasks = filtered_tasks

        if not self.tasks:
            QMessageBox.warning(self, '操作无效', '当前时间段无历史记录')
            return

        self.new_window2 = QDialog(flags=Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
        self.new_window1.setWindowIcon(QIcon('logo.png'))
        self.new_window2.setWindowTitle("html")
        self.new_window2.setGeometry(100, 100, 800, 600)
        self.layout2 = QVBoxLayout()
        self.web_view2 = QWebEngineView()

        if self.chart_type == 'type':
            self.chart_html2 = self.plotTypeBar()
        else:
            self.chart_html2 = self.plotStatusBar()

        self.web_view2.setHtml(self.chart_html2)

        self.layout2.addWidget(self.web_view2)
        self.new_window2.setLayout(self.layout2)
        self.new_window2.show()

    def showChart(self, chart_type):
        tasks = get_task_list_database(self.id)

        # 筛选符合条件的任务
        filtered_tasks = []
        for task in tasks:
            task_date_str = task.ddl
            if self.selectBegin <= task_date_str <= self.selectEnd and task.state != TASK_NOTSTART:
                filtered_tasks.append(task)

        self.tasks = filtered_tasks

        if not self.tasks:
            QMessageBox.warning(self, '操作无效', '当前时间段无历史记录')
            return
        if chart_type == 'type':
            self.chart_type = 'type'
            self.showTypePieChart()
            self.showTypeBarChart()
        elif chart_type == 'status':
            self.chart_type = 'status'
            self.showStatusPieChart()
            self.showStatusBarChart()

    def showTypePieChart(self):
        type_count = {}
        for task in self.tasks:
            if task.type in type_count:
                type_count[task.type] += 1
            else:
                type_count[task.type] = 1

        self.figure_pie.clear()
        ax = self.figure_pie.add_subplot(111)
        types = list(type_count.keys())
        colors = [plt.colormaps['Blues'](i / float(len(types))) for i in range(len(types))]
        wedges, texts, autotexts = ax.pie(type_count.values(), autopct='%1.1f%%', colors=colors,
                                          textprops={'fontsize': 12})
        ax.set_title('任务类型饼状图')
        ax.legend(wedges, type_count.keys(), loc="upper center", bbox_to_anchor=(0.5, 0.1), ncol=len(type_count),
                  frameon=False)

        self.canvas_pie.draw()

    def showStatusPieChart(self):
        status_count = {}
        for task in self.tasks:
            if task.state in status_count:
                status_count[task.state] += 1
            else:
                status_count[task.state] = 1

        self.figure_pie.clear()
        ax = self.figure_pie.add_subplot(111)
        types = list(status_count.keys())
        colors = [plt.colormaps['Blues'](i / float(len(types))) for i in range(len(types))]
        wedges, texts, autotexts = ax.pie(status_count.values(), autopct='%1.1f%%', colors=colors,
                                          textprops={'fontsize': 12})
        ax.legend(wedges, status_count.keys(), loc="upper center", bbox_to_anchor=(0.5, 0.1), ncol=len(status_count),
                  frameon=False)
        ax.set_title('任务状态饼状图')
        self.canvas_pie.draw()

    def showTypeBarChart(self):
        type_count = {}
        for task in self.tasks:
            if task.type in type_count:
                type_count[task.type] += 1
            else:
                type_count[task.type] = 1

        self.figure_bar.clear()
        ax = self.figure_bar.add_subplot(111)

        types = list(type_count.keys())
        counts = list(type_count.values())
        colors = [plt.colormaps['Blues'](i / float(len(types))) for i in range(len(types))]

        bars = ax.bar(types, counts, color=colors)
        ax.set_title('任务类型柱状图')
        ax.set_xlabel('类型')
        ax.set_ylabel('数量')

        # 在每个栏顶部增加标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

        self.canvas_bar.draw()

    def showStatusBarChart(self):
        status_count = {}
        for task in self.tasks:
            if task.state in status_count:
                status_count[task.state] += 1
            else:
                status_count[task.state] = 1

        self.figure_bar.clear()
        ax = self.figure_bar.add_subplot(111)

        states = list(status_count.keys())
        counts = list(status_count.values())
        colors = [plt.colormaps['Blues'](i / float(len(states))) for i in range(len(states))]

        bars = ax.bar(states, counts, color=colors)
        ax.set_title('任务状态柱状图')
        ax.set_xlabel('状态')
        ax.set_ylabel('数量')

        # 在每个栏顶部增加标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height, '%d' % int(height), ha='center', va='bottom')

        self.canvas_bar.draw()

    def prevPeriod(self):
        if self.current_period == 'day':
            self.current_date = self.current_date.addDays(-1)
        elif self.current_period == 'week':
            self.current_date = self.current_date.addDays(-7)
        elif self.current_period == 'month':
            self.current_date = self.current_date.addMonths(-1)
        self.updateDateLabel()

    def nextPeriod(self):
        if self.current_period == 'day':
            self.current_date = self.current_date.addDays(1)
        elif self.current_period == 'week':
            self.current_date = self.current_date.addDays(7)
        elif self.current_period == 'month':
            self.current_date = self.current_date.addMonths(1)
        self.updateDateLabel()

    def selectPeriod(self, period):
        self.current_date = QDate.currentDate()
        self.current_period = period
        self.day_button.setChecked(period == 'day')
        self.week_button.setChecked(period == 'week')
        self.month_button.setChecked(period == 'month')
        self.custom_button.setChecked(period == 'custom')
        self.updateButtonStyles()
        if period == 'custom':
            self.showCustomDateSelectors()
        else:
            self.hideCustomDateSelectors()
        self.updateDateLabel2()

    def updateDateLabel(self):
        now = QDate.currentDate()
        if self.current_period == 'day':
            self.selectBegin = self.current_date.toString("yyyy/MM/dd")
            self.selectEnd = self.current_date.toString("yyyy/MM/dd")
            self.date_label.setText(f'历史数据统计 {self.current_date.toString("yyyy/MM/dd")}')
        elif self.current_period == 'week':
            start_date = self.current_date.addDays(-self.current_date.dayOfWeek() + 1)
            end_date = start_date.addDays(6)
            self.selectBegin = start_date.toString("yyyy/MM/dd")
            self.selectEnd = end_date.toString("yyyy/MM/dd")
            self.date_label.setText(
                f'历史数据统计 {start_date.toString("yyyy/MM/dd")} - {end_date.toString("yyyy/MM/dd")}')
        elif self.current_period == 'month':
            start_date = QDate(self.current_date.year(), self.current_date.month(), 1)
            end_date = start_date.addMonths(1).addDays(-1)
            self.selectBegin = start_date.toString("yyyy/MM/dd")
            self.selectEnd = end_date.toString("yyyy/MM/dd")
            self.date_label.setText(
                f'历史数据统计 {start_date.toString("yyyy/MM/dd")} - {end_date.toString("yyyy/MM/dd")}')
        elif self.current_period == 'custom':
            self.date_label.setText('历史数据统计')

    def updateDateLabel2(self):
        now = QDate.currentDate()
        if self.current_period == 'day':
            self.selectBegin = now.toString("yyyy/MM/dd")
            self.selectEnd = now.toString("yyyy/MM/dd")
            self.date_label.setText(f'历史数据统计 {now.toString("yyyy/MM/dd")}')
        elif self.current_period == 'week':
            start_date = now.addDays(-now.dayOfWeek() + 1)
            end_date = start_date.addDays(6)
            self.selectBegin = start_date.toString("yyyy/MM/dd")
            self.selectEnd = end_date.toString("yyyy/MM/dd")
            self.date_label.setText(
                f'历史数据统计 {start_date.toString("yyyy/MM/dd")} - {end_date.toString("yyyy/MM/dd")}')
        elif self.current_period == 'month':
            start_date = QDate(now.year(), now.month(), 1)
            end_date = start_date.addMonths(1).addDays(-1)
            self.selectBegin = start_date.toString("yyyy/MM/dd")
            self.selectEnd = end_date.toString("yyyy/MM/dd")
            self.date_label.setText(
                f'历史数据统计 {start_date.toString("yyyy/MM/dd")} - {end_date.toString("yyyy/MM/dd")}')
        elif self.current_period == 'custom':
            self.date_label.setText('历史数据统计')

    def showCustomDateSelectors(self):
        if hasattr(self, 'start_date_edit') and self.start_date_edit is not None:
            return  # 如果自定义日期选择器已经存在，则不创建新的

        self.prev_button.hide()
        self.next_button.hide()

        self.start_date_edit = ZhDatePicker(self)
        self.start_date_edit.setDate(QDate.currentDate())
        self.end_date_edit = ZhDatePicker(self)
        self.end_date_edit.setDate(QDate.currentDate())
        self.confirmButton = PushButton('确定')
        self.confirmButton.setStyleSheet("""
                                            PushButton {
                                                background-color: #4CAfAf;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                padding: 5px 20px;
                                            }
                                        """)

        self.confirmButton.clicked.connect(self.zidingyi)
        self.title_layout.insertWidget(1, self.start_date_edit)
        self.to_label = LargeTitleLabel('-')  # 新增到标签的成员变量
        self.title_layout.insertWidget(2, self.to_label)
        self.title_layout.insertWidget(3, self.end_date_edit)
        self.title_layout.insertWidget(4, self.confirmButton)

    def zidingyi(self):
        start_date_str = self.start_date_edit.getDate().toString('yyyy/MM/dd')
        end_date_str = self.end_date_edit.getDate().toString('yyyy/MM/dd')

        if start_date_str > end_date_str:
            QMessageBox.warning(self, '操作无效', '起始日期不能大于终止日期。')
            return
        self.selectBegin = start_date_str
        self.selectEnd = end_date_str

    def hideCustomDateSelectors(self):
        self.prev_button.show()
        self.next_button.show()
        if hasattr(self, 'start_date_edit') and self.start_date_edit is not None:
            self.title_layout.removeWidget(self.start_date_edit)
            self.start_date_edit.deleteLater()
            self.start_date_edit = None
        if hasattr(self, 'end_date_edit') and self.end_date_edit is not None:
            self.title_layout.removeWidget(self.end_date_edit)
            self.end_date_edit.deleteLater()
            self.end_date_edit = None
        if hasattr(self, 'to_label') and self.to_label is not None:
            self.title_layout.removeWidget(self.to_label)
            self.to_label.deleteLater()
            self.to_label = None
        if hasattr(self, 'confirmButton') and self.confirmButton is not None:
            self.title_layout.removeWidget(self.confirmButton)
            self.confirmButton.deleteLater()
            self.confirmButton = None

    def updateButtonStyles(self):
        buttons = [self.day_button, self.week_button, self.month_button, self.custom_button]
        for button in buttons:
            if button.isChecked():
                button.setStyleSheet("""
                    PushButton {
                        background-color: #4CAfAf;
                        color: white;
                        border: none;
                        border-radius: 15px;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: black;
                        border: none;
                        border-radius: 15px;
                    }
                """)

    def resetForm(self):
        print("切换到历史页面")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = history_main(0)
    window.show()
    sys.exit(app.exec_())
