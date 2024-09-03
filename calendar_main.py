from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QSplitter, \
    QButtonGroup, QSizePolicy, QTableWidget, QGridLayout, QHeaderView, QDialog, QTableWidgetItem, QMessageBox, \
    QFileDialog
from qfluentwidgets import RadioButton, Slider
from calendar_ui import Ui_calendar
from database import *
import openpyxl


class calendar_main(Ui_calendar, QWidget):
    def __init__(self, id, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.id = id
        self.selected_date = QDate.currentDate().day()
        self.initUI()

    def initUI(self):
        self.layout = QHBoxLayout(self)

        # 创建左侧布局
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout(self.left_widget)

        # 前后翻动按钮
        self.navigation_layout = QHBoxLayout()
        self.prev_month_button = QPushButton('<')
        self.next_month_button = QPushButton('>')
        self.prev_year_button = QPushButton('<<')
        self.next_year_button = QPushButton('>>')

        self.navigation_layout.addWidget(self.prev_year_button)
        self.navigation_layout.addWidget(self.prev_month_button)
        self.navigation_layout.addWidget(self.next_month_button)
        self.navigation_layout.addWidget(self.next_year_button)
        self.left_layout.addLayout(self.navigation_layout)

        # 日期显示
        self.date_and_button_layout = QHBoxLayout()
        self.year = QDate.currentDate().year()
        self.month = QDate.currentDate().month()
        self.day = QDate.currentDate().day()
        self.selected_date_label = QLabel(f"{self.year}年{self.month}月")
        self.date_and_button_layout.addWidget(self.selected_date_label)

        # 添加快速跳转按钮
        self.jump_to_today_button = QPushButton('今天')
        self.jump_to_today_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CB6C0;
                                        color: white;
                                        border: none;
                                        border-radius: 5px;
                                        font-size: 14px;
                                        padding: 6px 20px;
                                    }
                                """)
        self.jump_to_today_button.clicked.connect(self.jump_to_today)
        self.date_and_button_layout.addStretch(1)
        self.date_and_button_layout.addWidget(self.jump_to_today_button)

        self.left_layout.addLayout(self.date_and_button_layout)

        # 设置字体大小
        font = QFont()
        font.setPointSize(20)
        self.selected_date_label.setFont(font)

        self.calendarGrid = QGridLayout()
        self.left_layout.addLayout(self.calendarGrid)

        self.selectedDateLabel = QLabel(
            f'选中日期: {QDate.currentDate().year()}-{QDate.currentDate().month()}-{QDate.currentDate().day()}')
        self.selectedDateLabel.setStyleSheet("color: grey")
        self.left_layout.addWidget(self.selectedDateLabel)
        self.drawCalendar()

        # 创建控制按钮
        self.button1 = QPushButton('调度任务')
        self.button1.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CB6C0;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                font-size: 15px;
                                                padding: 8px 20px;
                                            }
                                        """)
        self.button2 = QPushButton('查看任务')
        self.button2.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CB6C0;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                font-size: 15px;
                                                padding: 8px 20px;
                                            }
                                        """)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.button1)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addStretch(1)

        self.left_layout.addLayout(self.button_layout)
        self.left_layout.addStretch(1)
        self.left_widget.setLayout(self.left_layout)

        # 创建右侧布局
        self.right_widget = QStackedWidget()

        # 创建视图1的表格
        self.view1_widget = QWidget()
        self.view1_layout = QVBoxLayout(self.view1_widget)
        self.table1 = QTableWidget(10, 2)
        self.table1.setHorizontalHeaderLabels(['时间', '任务'])
        self.table1.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止用户编辑表格
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置水平表头的拉伸模式
        self.derive_button1 = QPushButton("导出")
        self.derive_button1.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CAfAf;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                font-size: 15px;
                                                padding: 5px 20px;
                                            }
                                        """)
        self.view1_layout.addWidget(self.table1)
        self.derive_layout1 = QHBoxLayout()
        self.derive_layout1.addStretch(1)
        self.derive_layout1.addWidget(self.derive_button1)
        self.view1_layout.addLayout(self.derive_layout1)

        # 创建视图2的表格
        self.view2_widget = QWidget()
        self.view2_layout = QVBoxLayout(self.view2_widget)
        self.table2 = QTableWidget(10, 1)
        self.table2.setHorizontalHeaderLabels(['任务'])
        self.table2.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁止用户编辑表格
        self.table2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 设置水平表头的拉伸模式
        self.derive_button2 = QPushButton("导出")
        self.derive_button2.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: #4CAfAf;
                                                        color: white;
                                                        border: none;
                                                        border-radius: 5px;
                                                        font-size: 15px;
                                                        padding: 5px 20px;
                                                    }
                                                """)
        self.view2_layout.addWidget(self.table2)
        self.derive_layout2 = QHBoxLayout()
        self.derive_layout2.addStretch(1)
        self.derive_layout2.addWidget(self.derive_button2)
        self.view2_layout.addLayout(self.derive_layout2)

        self.right_widget.addWidget(self.view1_widget)
        self.right_widget.addWidget(self.view2_widget)

        # 添加分隔器
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.left_widget)
        self.splitter.addWidget(self.right_widget)
        self.splitter.setSizes([1000, 1000])  # 设置左右部分各占1/2的比例

        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)

        # 连接按钮与槽
        self.button1.clicked.connect(self.show_radio_buttons)
        self.button2.clicked.connect(self.switch_to_view2)
        self.prev_month_button.clicked.connect(self.prevMonth)
        self.next_month_button.clicked.connect(self.nextMonth)
        self.prev_year_button.clicked.connect(self.prevYear)
        self.next_year_button.clicked.connect(self.nextYear)
        self.derive_button1.clicked.connect(self.export_table1_to_excel)
        self.derive_button2.clicked.connect(self.export_table2_to_excel)

    def export_table1_to_excel(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存为 Excel 文件", "", "Excel Files (*.xlsx);;All Files (*)",
                                                   options=options)
        if not file_name:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "任务列表"

        # 获取表头
        headers = [self.table1.horizontalHeaderItem(i).text() for i in range(self.table1.columnCount())]
        sheet.append(headers)

        # 遍历表格数据
        for row in range(self.table1.rowCount()):
            row_data = [self.table1.item(row, col).text() if self.table1.item(row, col) else '' for col in
                        range(self.table1.columnCount())]
            sheet.append(row_data)

        workbook.save(file_name)

    def export_table2_to_excel(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "保存为 Excel 文件", "", "Excel Files (*.xlsx);;All Files (*)",
                                                   options=options)
        if not file_name:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "任务列表"

        # 获取表头
        headers = [self.table2.horizontalHeaderItem(i).text() for i in range(self.table2.columnCount())]
        sheet.append(headers)

        # 遍历表格数据
        for row in range(self.table2.rowCount()):
            row_data = [self.table2.cellWidget(row, col).text() if self.table2.cellWidget(row, col) else '' for col in
                        range(self.table2.columnCount())]
            sheet.append(row_data)

        workbook.save(file_name)

    def show_radio_buttons(self):
        # 如果已经存在radio_button_layout则先移除
        if hasattr(self, 'radio_button_layout') and self.radio_button_layout is not None:
            return  # 防止重复添加

        # 创建新的布局和控件
        self.radio_button_layout = QVBoxLayout()
        self.radio_button_group = QButtonGroup(self)

        self.radio1 = RadioButton("短作业优先调度")
        self.radio2 = RadioButton("优先级优先调度")
        self.radio3 = RadioButton("自定义比例")
        self.confirm_button = QPushButton("确 定")
        self.confirm_button.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CB6C0;
                                        color: white;
                                        border: none;
                                        border-radius: 5px;
                                        font-size: 17px;
                                        padding: 8px 20px;
                                    }
                                """)
        # 默认选中选项1
        self.radio1.setChecked(True)

        self.radio_button_group.addButton(self.radio1)
        self.radio_button_group.addButton(self.radio2)
        self.radio_button_group.addButton(self.radio3)

        self.radio_button_layout.addWidget(self.radio1)
        self.radio_button_layout.addWidget(self.radio2)
        self.radio_button_layout.addWidget(self.radio3)

        # 添加滑动条
        self.slider = Slider(Qt.Horizontal)
        self.slider.setFixedWidth(200)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider_label = QLabel("短作业优先权重: 0.50")
        self.slider_label.setStyleSheet("color:grey;")
        self.slider.valueChanged.connect(self.update_slider_label)

        self.slider_layout = QHBoxLayout()
        self.slider_layout.addStretch(1)
        self.slider_layout.addWidget(self.slider)
        self.slider_layout.addWidget(self.slider_label)
        self.slider_layout.addStretch(1)
        self.radio_button_layout.addLayout(self.slider_layout)
        self.radio_button_layout.addWidget(self.confirm_button)

        self.left_layout.addLayout(self.radio_button_layout)
        self.left_layout.addStretch(1)

        # 按键功能
        self.confirm_button.clicked.connect(self.on_confirm)
        self.radio3.toggled.connect(self.toggle_slider_visibility)
        self.toggle_slider_visibility()

    def toggle_slider_visibility(self):
        if self.radio3.isChecked():
            self.slider.show()
            self.slider_label.show()
        else:
            self.slider.hide()
            self.slider_label.hide()

    def update_slider_label(self):
        value = self.slider.value() / 100.0
        self.slider_label.setText(f"短作业优先权重: {value:.2f}")

    def switch_to_view1(self, tasks):
        user = get_user_database(self.id)
        start_working_time = user.start
        end_working_time = user.end
        # 清空表格
        self.table1.setRowCount(0)
        # 将工作时间转换为小时数
        start_hour = int(start_working_time.split(':')[0])
        end_hour = int(end_working_time.split(':')[0])
        current_hour = start_hour
        flg = 0
        if not tasks:
            # 插入一行显示“今天没有任务哦~”
            row_position = self.table1.rowCount()
            self.table1.insertRow(row_position)
            no_task_label = QLabel('今天没有任务哦~')
            no_task_label.setAlignment(Qt.AlignCenter)
            self.table1.setCellWidget(row_position, 0, no_task_label)
        else:
            for task in tasks:
                duration = task.duration
                end_task_hour = current_hour + duration
                # 检查任务是否在工作时间内结束
                if flg == 2:
                    QMessageBox.warning(self, "工作时间结束", "任务时间超出工作时间范围qwq")
                    break
                if end_task_hour > end_hour:
                    end_task_hour = end_hour
                    flg = 1
                elif end_task_hour == end_hour:
                    flg = 2
                start_time_str = f"{current_hour:02d}:00"
                end_time_str = f"{end_task_hour:02d}:00"
                # 插入新行
                row_position = self.table1.rowCount()
                self.table1.insertRow(row_position)
                self.table1.setItem(row_position, 0, QTableWidgetItem(f"{start_time_str} - {end_time_str}"))
                self.table1.setItem(row_position, 1, QTableWidgetItem(task.title))
                # 创建按钮显示任务标题
                task_button = QPushButton(task.title)
                task_button.clicked.connect(lambda checked, t=task: self.show_task_details(t))
                self.table1.setCellWidget(row_position, 1, task_button)
                current_hour = end_task_hour
                # 如果任务结束时间到达或超过工作结束时间，停止排入任务
                if current_hour >= end_hour:
                    if flg == 1:
                        QMessageBox.warning(self, "工作时间结束", "任务时间超出工作时间范围qwq")
                        break
        self.right_widget.setCurrentIndex(0)
        self.clear_radio_buttons()

    def on_confirm(self):
        if self.radio1.isChecked():
            op = 1
        elif self.radio2.isChecked():
            op = 2
        elif self.radio3.isChecked():
            op = 3
        else:
            return
        formatted_date = f'{self.year:04d}/{self.month:02d}/{int(self.selected_date):02d}'
        tasks = calendar_get_task_database(self.id, formatted_date)
        tasks = [task for task in tasks if task.state == TASK_UNDERWAY or task.state == TASK_NOTSTART]
        sorted_tasks = self.arrange_tasks(tasks, op)
        self.switch_to_view1(sorted_tasks)
        self.clear_radio_buttons()
        self.slider.hide()
        self.slider_label.hide()

    def custom_sort(self, dialog, tasks, slider_value):
        weight = slider_value / 100
        tasks.sort(key=lambda x: weight * x.duration + (1 - weight) * x.importance)
        dialog.accept()
        self.switch_to_view1(tasks)

    def arrange_tasks(self, tasks, op):
        if op == 1:  # 按时长从短到长
            tasks.sort(key=lambda x: x.duration)
        elif op == 2:  # 按优先级从高到低
            tasks.sort(key=lambda x: x.importance, reverse=True)
        elif op == 3:  # 根据用户输入自定义比例
            weight = self.slider.value() / 100.0
            tasks.sort(key=lambda x: weight * x.duration + (1 - weight) * x.importance)
        return tasks

    def show_task_details(self, task):
        # 创建一个新的对话框显示任务详细信息
        dialog = QDialog(self)
        dialog.setWindowTitle("任务详情")
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        layout = QVBoxLayout()

        title_label = QLabel(f"标题: {task.title}")
        description_label = QLabel(f"描述: {task.description}")
        importance_label = QLabel(f"优先级: {task.importance}")
        is_daily_label = QLabel(f"是否为普通任务: {'是' if task.isDaily else '否'}")
        type_label = QLabel(f"类别: {task.type}")
        ddl_label = QLabel(f"截止日期: {task.ddl}")
        duration_label = QLabel(f"用时: {task.duration}")
        state_label = QLabel(f"状态: {task.state}")

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(importance_label)
        layout.addWidget(is_daily_label)
        layout.addWidget(type_label)
        layout.addWidget(ddl_label)
        layout.addWidget(duration_label)
        layout.addWidget(state_label)

        close_button = QPushButton("关闭")
        close_button.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: #4CAfAf;
                                                        color: white;
                                                        border: none;
                                                        border-radius: 5px;
                                                        font-size: 13px;
                                                        padding: 5px 20px;
                                                    }
                                                """)
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def switch_to_view2(self):
        self.clear_radio_buttons()
        if hasattr(self, 'slider') and self.slider is not None:
            self.slider.hide()
        if hasattr(self, 'slider_label') and self.slider_label is not None:
            self.slider_label.hide()
        formatted_date = f'{self.year:04d}/{self.month:02d}/{int(self.selected_date):02d}'
        tasks = calendar_get_task_database(self.id, formatted_date)
        # 清空表格
        self.table2.setRowCount(0)

        if not tasks:
            row_position = self.table2.rowCount()
            self.table2.insertRow(row_position)
            no_task_label = QLabel('今天没有任务哦~')
            no_task_label.setAlignment(Qt.AlignCenter)
            self.table2.setCellWidget(row_position, 0, no_task_label)
        else:
            for task in tasks:
                # 插入新行
                row_position = self.table2.rowCount()
                self.table2.insertRow(row_position)
                # 创建按钮显示任务标题
                task_button = QPushButton(task.title)
                task_button.clicked.connect(lambda checked, t=task: self.show_task_details(t))
                self.table2.setCellWidget(row_position, 0, task_button)

        self.right_widget.setCurrentIndex(1)

    def clear_radio_buttons(self):
        # 移除单选按钮和确定按钮
        if hasattr(self, 'radio_button_layout') and self.radio_button_layout is not None:
            for i in reversed(range(self.radio_button_layout.count())):
                widget = self.radio_button_layout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            self.radio_button_layout = None

    def drawCalendar(self):
        year = self.year
        month = self.month
        self.selected_date_label.setText(f"{year}年{month}月")

        self.clearLayout(self.calendarGrid)
        days = ['日', '一', '二', '三', '四', '五', '六']
        for i, day in enumerate(days):
            self.calendarGrid.addWidget(QLabel(day), 0, i)

        firstDay = QDate(self.year, self.month, 1).dayOfWeek()
        daysInMonth = QDate(self.year, self.month, 1).daysInMonth()
        row = 1
        col = firstDay % 7
        for day in range(1, daysInMonth + 1):
            btn = QPushButton(str(day))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(self.showDate)
            self.calendarGrid.addWidget(btn, row, col)
            col += 1
            if col > 6:
                col = 0
                row += 1

        for i in range(row + 1):
            self.calendarGrid.setRowStretch(i, 1)
        for j in range(7):
            self.calendarGrid.setColumnStretch(j, 1)

    def showDate(self):
        sender = self.sender()
        day = sender.text()
        self.selected_date = day
        self.selectedDateLabel.setText(f'选中日期: {self.year}-{self.month}-{day}')

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def prevMonth(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.drawCalendar()

    def nextMonth(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.drawCalendar()

    def prevYear(self):
        self.year -= 1
        self.drawCalendar()

    def nextYear(self):
        self.year += 1
        self.drawCalendar()

    def jump_to_today(self):
        self.day = QDate.currentDate().day()
        self.year = QDate.currentDate().year()
        self.month = QDate.currentDate().month()
        self.selectedDateLabel.setText(
            f'选中日期: {QDate.currentDate().year()}-{QDate.currentDate().month()}-{QDate.currentDate().day()}')
        self.drawCalendar()

    def resetForm(self):
        print(1)
