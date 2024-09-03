import sys
from datetime import timedelta

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QListWidget, QListWidgetItem, QCheckBox, QDialog, QTextEdit, QButtonGroup, \
    QMessageBox, QFileDialog, QSizePolicy
from PyQt5.QtCore import QDate, Qt
from qfluentwidgets import ComboBox, ZhDatePicker, RadioButton, BodyLabel
from datetime import datetime

from database import add_task_database, get_task_database, get_task_list_database, modify_task_database, \
    delete_task_database, modify_task_state_database
from home_ui import Ui_home
from task import *


class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent, flags=Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('新增任务')
        self.initUI()
        self.task = task
        if task:
            self.setTaskDetails(task)

    def initUI(self):
        layout = QVBoxLayout()

        titleLayout = QHBoxLayout()
        titleLabel = QLabel('标题:')
        self.titleEdit = QLineEdit()
        self.titleEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        titleLayout.addWidget(titleLabel)
        titleLayout.addWidget(self.titleEdit)
        layout.addLayout(titleLayout)

        descLayout = QHBoxLayout()
        descLabel = QLabel('描述:')
        self.descEdit = QTextEdit()
        self.descEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        descLayout.addWidget(descLabel)
        descLayout.addWidget(self.descEdit)
        layout.addLayout(descLayout)

        typeLayout = QHBoxLayout()
        typeLabel = QLabel('类型:')
        self.typeCombo = ComboBox()
        self.typeCombo.addItems(["工作", "学习", "休闲", "其他"])
        self.typeCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        typeLayout.addWidget(typeLabel)
        typeLayout.addWidget(self.typeCombo)
        layout.addLayout(typeLayout)

        priorityLayout = QHBoxLayout()
        priorityLabel = QLabel('优先级:')
        self.priorityCombo = ComboBox()
        self.priorityCombo.addItems(["1", "2", "3", "4", "5"])
        self.priorityCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        priorityLayout.addWidget(priorityLabel)
        priorityLayout.addWidget(self.priorityCombo)
        layout.addLayout(priorityLayout)

        durationLayout = QHBoxLayout()
        durationLabel = QLabel('用时:')
        self.durationCombo = ComboBox()
        self.durationCombo.addItems([str(i) for i in range(1, 11)])
        self.durationCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        durationLayout.addWidget(durationLabel)
        durationLayout.addWidget(self.durationCombo)
        layout.addLayout(durationLayout)

        self.radioGroup = QButtonGroup()
        taskRadioLayout = QHBoxLayout()
        self.dailyRadio = RadioButton('日常任务')
        self.dailyRadio.toggled.connect(self.toggleDateInputs)
        self.waitingRadio = RadioButton('普通任务')
        self.radioGroup.addButton(self.dailyRadio)
        self.radioGroup.addButton(self.waitingRadio)
        self.dailyRadio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.waitingRadio.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        taskRadioLayout.addWidget(self.dailyRadio)
        taskRadioLayout.addWidget(self.waitingRadio)
        layout.addLayout(taskRadioLayout)

        self.startDateLayout = QHBoxLayout()
        self.startDateLabel = QLabel('起始日期:')
        self.startDateEdit = ZhDatePicker()
        self.startDateEdit.setDate(QDate.currentDate())
        self.startDateEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.startDateLayout.addWidget(self.startDateLabel)
        self.startDateLayout.addWidget(self.startDateEdit)

        self.endDateLayout = QHBoxLayout()
        self.endDateLabel = QLabel('结束日期:')
        self.endDateEdit = ZhDatePicker()
        self.endDateEdit.setDate(QDate.currentDate().addDays(1))
        self.endDateEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.endDateLayout.addWidget(self.endDateLabel)
        self.endDateLayout.addWidget(self.endDateEdit)

        self.deadlineLayout = QHBoxLayout()
        self.deadlineLabel = QLabel('截止日期:')
        self.deadlineEdit = ZhDatePicker()
        self.deadlineEdit.setDate(QDate.currentDate().addDays(1))
        self.deadlineEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.deadlineLayout.addWidget(self.deadlineLabel)
        self.deadlineLayout.addWidget(self.deadlineEdit)

        layout.addLayout(self.startDateLayout)
        layout.addLayout(self.endDateLayout)
        layout.addLayout(self.deadlineLayout)

        # 按钮
        buttonLayout = QHBoxLayout()
        self.saveButton = QPushButton('保存')
        self.saveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.saveButton.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CB6C0;
                                        color: white;
                                        border: none;
                                        border-radius: 5px;
                                        font-size: 14px;
                                        padding: 5px 20px;
                                    }
                                """)
        self.saveButton.clicked.connect(self.accept)
        self.cancelButton = QPushButton('取消')
        self.cancelButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cancelButton.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CB6C0;
                                        color: white;
                                        border: none;
                                        border-radius: 5px;
                                        font-size: 14px;
                                        padding: 5px 20px;
                                    }
                                """)
        self.cancelButton.clicked.connect(self.reject)
        buttonLayout.addWidget(self.saveButton)
        buttonLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)
        self.toggleDateInputs()

    def accept(self):
        if not self.titleEdit.text().strip():
            QMessageBox.warning(self, '无效输入', '标题不能为空。')
            return
        today = QDate.currentDate()
        if isinstance(self.task, bool):  # 新增窗口
            if self.dailyRadio.isChecked():
                start_date = self.startDateEdit.date
                end_date = self.endDateEdit.date

                if start_date > end_date:
                    QMessageBox.warning(self, '无效日期', '起始日期不能晚于结束日期')
                    return
                if start_date < today and end_date < today:
                    QMessageBox.warning(self, '无效日期', '起始日期和结束日期不能早于今天。')
                    return
                if start_date < today:
                    QMessageBox.warning(self, '无效日期', '起始日期不能早于今天。')
                    return
                if end_date < today:
                    QMessageBox.warning(self, '无效日期', '结束日期不能早于今天。')
                    return

            else:
                deadline_date = self.deadlineEdit.date
                if deadline_date < today:
                    QMessageBox.warning(self, '无效日期', '截止日期不能早于今天。')
                    return
        else:  # 编辑窗口
            if self.task.isDaily == 'True':  # 原来是日常任务
                if not self.dailyRadio.isChecked() and (self.startDateEdit.date !=
                                                        QDate.fromString(self.task.ddl, 'yyyy/MM/dd')
                                                        or self.endDateEdit.date !=
                                                        QDate.fromString(self.task.ddl, 'yyyy/MM/dd')):
                    QMessageBox.warning(self, '无效操作', '不能修改日常任务的状态和日期。')
                    return
                if not self.dailyRadio.isChecked():
                    QMessageBox.warning(self, '无效操作', '不能修改日常任务的状态。')
                    return
                if (self.startDateEdit.date != QDate.fromString(self.task.ddl, 'yyyy/MM/dd') or
                        self.endDateEdit.date != QDate.fromString(self.task.ddl, 'yyyy/MM/dd')):
                    QMessageBox.warning(self, '无效操作', '不能修改日常任务的日期。')
                    return
            else:  # 原来是普通任务
                if self.dailyRadio.isChecked():
                    QMessageBox.warning(self, '无效操作', '不能修改普通任务的状态')
                    return

                deadline_date = self.deadlineEdit.date
                if deadline_date < today:
                    QMessageBox.warning(self, '无效日期', '截止日期不能早于今天。')
                    return
        super().accept()

    def toggleDateInputs(self):
        if self.dailyRadio.isChecked():
            self.startDateLayout.setEnabled(True)
            self.endDateLayout.setEnabled(True)
            self.startDateLabel.setVisible(True)
            self.startDateEdit.setVisible(True)
            self.endDateLabel.setVisible(True)
            self.endDateEdit.setVisible(True)
            self.deadlineLayout.setEnabled(False)
            self.deadlineLabel.setVisible(False)
            self.deadlineEdit.setVisible(False)
        else:
            self.startDateLayout.setEnabled(False)
            self.endDateLayout.setEnabled(False)
            self.startDateLabel.setVisible(False)
            self.startDateEdit.setVisible(False)
            self.endDateLabel.setVisible(False)
            self.endDateEdit.setVisible(False)
            self.deadlineLayout.setEnabled(True)
            self.deadlineLabel.setVisible(True)
            self.deadlineEdit.setVisible(True)

    def setTaskDetails(self, task):
        self.titleEdit.setText(task.title)
        self.descEdit.setText(task.description)
        self.typeCombo.setCurrentText(task.type)

        self.priorityCombo.setCurrentText(str(task.importance))
        self.durationCombo.setCurrentText(str(task.duration))
        if task.isDaily:
            self.dailyRadio.setChecked(True)
            self.startDateEdit.setDate(QDate.fromString(task.ddl, 'yyyy/MM/dd'))
            self.endDateEdit.setDate(QDate.fromString(task.ddl, 'yyyy/MM/dd'))
        else:
            self.waitingRadio.setChecked(True)
            self.deadlineEdit.setDate(QDate.fromString(task.ddl, 'yyyy/MM/dd'))


class TodoApp(Ui_home, QWidget):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.setupUi(self)
        self.initUI()
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('TODO')

    def initUI(self):
        self.setWindowTitle('Todo List App')
        self.setMinimumSize(400, 300)  # 设置一个最小尺寸，防止界面太小

        mainLayout = QVBoxLayout()

        # 第一行：起始日期和终止日期的日期选择器
        dateLayout = QHBoxLayout()

        startDateLabel = BodyLabel('起始日期:')
        dateLayout.addWidget(startDateLabel)

        self.startDateEdit = ZhDatePicker()  # Assuming DatePicker replaces QDateEdit
        self.startDateEdit.setDate(QDate.currentDate())
        self.startDateEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dateLayout.addWidget(self.startDateEdit)

        dateLayout.addStretch(1)  # 拉伸因子，确保后面的组件靠右

        endDateLabel = BodyLabel('终止日期:')
        dateLayout.addWidget(endDateLabel)

        self.endDateEdit = ZhDatePicker()
        self.endDateEdit.setDate(QDate.currentDate().addDays(1))
        self.endDateEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dateLayout.addWidget(self.endDateEdit)

        dateLayout.addStretch(1)  # 拉伸因子，确保后面的组件靠右

        mainLayout.addLayout(dateLayout)

        # 第二行：重要性、类别、状态等
        optionLayout = QHBoxLayout()

        # 优先级
        priorityLabel = BodyLabel('优先级:')
        optionLayout.addWidget(priorityLabel)
        self.priorityCombo = ComboBox()
        self.priorityCombo.addItems(["全部", "1", "2", "3", "4", "5"])
        self.priorityCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        optionLayout.addWidget(self.priorityCombo)

        optionLayout.addStretch(1)  # 拉伸因子，确保后面的组件靠右

        # 类型
        categoryLabel = BodyLabel('类型:')
        optionLayout.addWidget(categoryLabel)
        self.categoryCombo = ComboBox()
        self.categoryCombo.addItems(["全部", "工作", "学习", "休闲", "其他"])
        self.categoryCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        optionLayout.addWidget(self.categoryCombo)

        optionLayout.addStretch(1)  # 拉伸因子，确保后面的组件靠右

        # 状态
        statusLabel = BodyLabel('状态:')
        optionLayout.addWidget(statusLabel)
        self.statusCombo = ComboBox()
        self.statusCombo.addItems(["全部", "正在进行", "已完成", "逾期", "未启动"])
        self.statusCombo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        optionLayout.addWidget(self.statusCombo)

        optionLayout.addStretch(1)  # 拉伸因子，确保后面的组件靠右

        # 确定键
        self.confirmButton = QPushButton('确定')
        self.confirmButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.confirmButton.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CAfAf;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                padding: 5px 20px;
                                            }
                                        """)
        self.confirmButton.clicked.connect(self.filterTasks)
        optionLayout.addWidget(self.confirmButton)

        # 重置键
        self.resetButton = QPushButton('重置')
        self.resetButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.resetButton.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CAfAf;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                padding: 5px 20px;
                                            }
                                        """)
        self.resetButton.clicked.connect(self.resetForm)
        optionLayout.addWidget(self.resetButton)

        mainLayout.addLayout(optionLayout)

        # 任务列表
        self.taskList = QListWidget()
        mainLayout.addWidget(self.taskList)

        # 新增任务按钮
        self.addButton = QPushButton('新增任务')
        self.addButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.addButton.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CB6C0;
                                        color: white;
                                        border: none;
                                        border-radius: 5px;
                                        font-size: 14px;
                                        padding: 6px 20px;
                                    }
                                """)
        self.addButton.clicked.connect(self.openTaskDialog)

        # 批量导入按钮
        self.loadButton = QPushButton('批量导入')
        self.loadButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.loadButton.setStyleSheet("""
                                    QPushButton {
                                        background-color: #4CB6C0;
                                        color: white;
                                        border: none;
                                        border-radius: 5px;
                                        font-size: 14px;
                                        padding: 6px 20px;
                                    }
                                """)
        self.loadButton.clicked.connect(self.uploadMany)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.addButton)
        self.bottomLayout.addWidget(self.loadButton)
        mainLayout.addLayout(self.bottomLayout)

        self.setLayout(mainLayout)

        self.initTask()

    def initTask(self):
        ls = get_task_list_database(self.id)
        for task in ls:
            self.addTask_ui(task)

    def openTaskDialog(self, task=None, taskLabel=None, taskInfoLabel=None):
        dialog = TaskDialog(self, task)
        if dialog.exec() == QDialog.Accepted:
            if task:
                self.updateTask(dialog, task, taskLabel, taskInfoLabel)
            else:
                self.addTask(dialog)

    def uploadMany(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "",
                                                   "Text Files (*.txt);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        parts = line.strip().split('","')
                        if len(parts) == 7:
                            # 去掉首尾的引号
                            parts[0] = parts[0][1:]
                            parts[6] = parts[6][:-1]
                            task = Task(
                                title=parts[0],
                                description=parts[1],
                                importance=int(parts[2]),
                                type=parts[3],
                                ddl=parts[4],
                                duration=int(parts[5]),
                                state=parts[6]
                            )
                            add_task_database(self.id, task)

        self.resetForm()

    def filterTasks(self):
        # 获取筛选条件，直接使用日期对象
        start_date = self.startDateEdit.date  # 确保这里返回QDate对象
        end_date = self.endDateEdit.date

        # 检查日期有效性
        if start_date > end_date:
            QMessageBox.warning(self, '操作无效', '起始日期不能大于终止日期。')
            return

        # 获取所有任务
        tasks = get_task_list_database(self.id)

        # 转换日期格式，如果DatePicker返回的是QDate
        start_date_str = start_date.toString('yyyy/MM/dd')
        end_date_str = end_date.toString('yyyy/MM/dd')

        # 筛选符合条件的任务
        filtered_tasks = []
        for task in tasks:
            task_date_str = task.ddl
            if start_date_str <= task_date_str <= end_date_str and \
                    (self.priorityCombo.currentText() == str(
                        task.importance) or self.priorityCombo.currentText() == "" or
                     self.priorityCombo.currentText() == "全部") and \
                    (self.categoryCombo.currentText() == task.type or self.categoryCombo.currentText() == "" or
                     self.categoryCombo.currentText() == "全部") and \
                    (self.statusCombo.currentText() == task.state or self.statusCombo.currentText() == "" or
                     self.statusCombo.currentText() == "全部"):
                filtered_tasks.append(task)

        # 清空当前任务列表
        self.taskList.clear()

        # 显示筛选后的任务
        for task in filtered_tasks:
            self.addTask_ui(task)

    def addTask(self, dialog):
        title = dialog.titleEdit.text()
        description = dialog.descEdit.toPlainText()
        taskType = dialog.typeCombo.currentText()
        duration = int(dialog.durationCombo.currentText())
        importance = int(dialog.priorityCombo.currentText())
        isDaily = True if dialog.dailyRadio.isChecked() else False
        if isDaily:
            start_date_str = dialog.startDateEdit.date.toString('yyyy/MM/dd')
            end_date_str = dialog.endDateEdit.date.toString('yyyy/MM/dd')
            start_date = datetime.strptime(start_date_str, '%Y/%m/%d')
            end_date = datetime.strptime(end_date_str, '%Y/%m/%d')
            # 获取今天的日期并将时间部分设置为零
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y/%m/%d')
                # 比较当前日期和今天的日期
                if current_date > today:
                    state = TASK_NOTSTART
                else:
                    state = TASK_UNDERWAY

                task = Task(title=title,
                            description=description,
                            importance=importance,
                            isDaily=isDaily,
                            type=taskType,
                            ddl=date_str,
                            duration=duration,
                            state=state
                            )
                add_task_database(self.id, task)
                self.addTask_ui(task)
                current_date += timedelta(days=1)

        else:
            taskDate_str = dialog.deadlineEdit.date.toString('yyyy/MM/dd')
            input_date = datetime.strptime(taskDate_str, '%Y/%m/%d')
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if input_date > today:
                state = TASK_NOTSTART
            else:
                state = TASK_UNDERWAY
            # 新建task数据实例
            task = Task(title=title,
                        description=description,
                        importance=importance,
                        isDaily=isDaily,
                        type=taskType,
                        ddl=taskDate_str,
                        duration=duration,
                        state=state
                        )
            add_task_database(self.id, task)
            self.addTask_ui(task)

    def addTask_ui(self, task):
        taskItemWidget = QWidget()
        taskItemLayout = QVBoxLayout()
        taskItemLayout.setSpacing(1)

        # 第一行：id和title，字体加大加粗，左对齐
        taskTitleLayout = QHBoxLayout()
        taskCheckBox = QCheckBox()
        if task.state == TASK_FINISHED:
            taskCheckBox.setChecked(True)
            taskCheckBox.setEnabled(False)
        else:
            taskCheckBox.clicked.connect(lambda: self.markTaskCompleted(taskCheckBox, taskLabel, taskInfoLabel))
        taskTitleLayout.addWidget(taskCheckBox)

        # TODO windows版本
        # taskLabel = QLabel(f"    {task.id}: {task.title}")
        # taskLabel.setStyleSheet("font-weight: bold; font-size: 26px;")

        # macOS版本
        taskLabel = QLabel(f"     {task.id}: {task.title}")
        taskLabel.setStyleSheet("font-weight: bold; font-size: 16px;")

        # 设置任务的颜色
        today_str = datetime.now().strftime('%Y/%m/%d')
        if task.importance >= 3 and task.ddl == today_str:  # 假设重要性大于等于3的今日任务设置为红色
            taskLabel.setStyleSheet(taskLabel.styleSheet() + " color: red;")

        taskTitleLayout.addWidget(taskLabel)
        taskTitleLayout.addStretch()

        # 第二行：截止日期、重要性、类型等信息
        taskInfoLayout = QHBoxLayout()

        taskInfoLabel = QLabel(
            f"        截止日期: {task.ddl:<35} 优先级: {task.importance:<15} 类型: {task.type:<15} 用时: {task.duration:<16} 状态: {task.state:<20}"
        )
        taskInfoLabel.setStyleSheet("color: gray")

        # 编辑和删除按钮
        editButton = QPushButton('✎')
        editButton.clicked.connect(lambda: self.editTask(taskLabel, taskInfoLabel))
        taskTitleLayout.addWidget(editButton)

        deleteButton = QPushButton('✖')
        deleteButton.clicked.connect(lambda: self.deleteTask(taskLabel))
        taskTitleLayout.addWidget(deleteButton)

        taskItemLayout.addLayout(taskTitleLayout)

        taskInfoLayout.addWidget(taskInfoLabel)
        taskItemLayout.addLayout(taskInfoLayout)
        taskItemWidget.setLayout(taskItemLayout)

        taskItem = QListWidgetItem()
        taskItem.setSizeHint(taskItemWidget.sizeHint())
        self.taskList.insertItem(0, taskItem)
        self.taskList.setItemWidget(taskItem, taskItemWidget)

    def markTaskCompleted(self, checkBox, taskLabel, taskInfoLabel):
        taskText = taskLabel.text()
        task_id = int(taskText.split(':')[0])
        task = get_task_database(self.id, task_id)

        if not task:
            QMessageBox.warning(self, '任务不存在', '找不到指定的任务。')
            return

        if task and task.state in [TASK_UNDERWAY, TASK_NOTSTART]:
            if checkBox.isChecked():
                new_state = TASK_FINISHED
                task.state = new_state
                success, message = modify_task_state_database(self.id, task_id, new_state)
                if success:
                    taskLabel.setText(f"     {task.id}: {task.title}")
                    taskLabel.setStyleSheet('color: green;font-weight: bold; font-size: 16px;')
                    taskInfoLabel.setText(
                        f"        截止日期: {task.ddl:<35} 重要性: {task.importance:<15} 类型: {task.type:<15} 用时: {task.duration:<16} 状态: {task.state:<20}"
                    )
                    checkBox.setEnabled(False)
                else:
                    QMessageBox.warning(self, '状态更新失败', message)
                    checkBox.setChecked(False)  # 如果更新失败，取消勾选
            else:
                # 如果试图取消勾选，重置复选框状态
                checkBox.setChecked(True)
                QMessageBox.warning(self, '操作无效', '任务完成后无法撤销。')
        else:
            # 如果任务状态不允许被勾选，重置复选框状态
            checkBox.setChecked(task.state == TASK_FINISHED)
            QMessageBox.warning(self, '操作无效', '只能勾选正在进行或未启动的任务。')

    def deleteTask(self, taskLabel):
        currentText = taskLabel.text()
        colon_index = currentText.find(':')
        number_part = currentText[:colon_index]
        task_id = int(number_part)
        task = get_task_database(self.id, task_id)

        if not task:
            QMessageBox.warning(self, '任务不存在', '找不到指定的任务。')
            return

        # 从数据库中删除任务
        success, message = delete_task_database(self.id, task_id)
        if success:
            # 从任务列表中移除项目
            for i in range(self.taskList.count()):
                item = self.taskList.item(i)
                widget = self.taskList.itemWidget(item)
                if widget.findChild(QLabel).text() == currentText:
                    self.taskList.takeItem(i)
                    break
            QMessageBox.information(self, '删除成功', '任务已成功删除。')
        else:
            QMessageBox.warning(self, '删除失败', message)

    def editTask(self, taskLabel, taskInfoLabel):
        currentText = taskLabel.text()
        colon_index = currentText.find(':')
        number_part = currentText[:colon_index]
        task_id = int(number_part)
        task = get_task_database(self.id, task_id)
        if not task:
            QMessageBox.warning(self, '任务不存在', '找不到指定的任务。')
            return
        if task.state in [TASK_FINISHED, TASK_OVERDUE]:
            QMessageBox.warning(self, '操作无效', '任务完成或过期后无法编辑。')
            return
        self.openTaskDialog(task, taskLabel, taskInfoLabel)

    def updateTask(self, dialog, task, taskLabel, taskInfoLabel):

        title = dialog.titleEdit.text()
        description = dialog.descEdit.toPlainText()
        taskType = dialog.typeCombo.currentText()
        duration = int(dialog.durationCombo.currentText())
        importance = int(dialog.priorityCombo.currentText())
        isDaily = True if dialog.dailyRadio.isChecked() else False

        if isDaily:
            taskDate_str = dialog.startDateEdit.date.toString('yyyy/MM/dd')
        else:
            taskDate_str = dialog.deadlineEdit.date.toString('yyyy/MM/dd')

        input_date = datetime.strptime(taskDate_str, '%Y/%m/%d')
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if input_date > today:
            state = TASK_NOTSTART
        else:
            state = TASK_UNDERWAY

        new_task = Task(title=title,
                        description=description,
                        importance=importance,
                        isDaily=isDaily,
                        type=taskType,
                        ddl=taskDate_str,
                        duration=duration,
                        state=state
                        )
        new_task.id = task.id
        modify_task_database(self.id, new_task)
        taskLabel.setText(f"     {new_task.id}: {new_task.title}")
        taskInfoLabel.setText(
            f"        截止日期: {new_task.ddl:<35} 优先级: {new_task.importance:<15} 类型: {new_task.type:<15} 用时: {new_task.duration:<16} 状态: {task.state:<20}"
        )

    def resetForm(self):
        print("切换到主页面")
        self.startDateEdit.setDate(QDate.currentDate())
        self.endDateEdit.setDate(QDate.currentDate().addDays(1))
        self.priorityCombo.setCurrentIndex(0)
        self.categoryCombo.setCurrentIndex(0)
        self.statusCombo.setCurrentIndex(0)

        # 获取所有任务
        tasks = get_task_list_database(self.id)

        # 清空当前任务列表
        self.taskList.clear()

        for task in tasks:
            self.addTask_ui(task)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TodoApp(id=0)
    ex.show()
    sys.exit(app.exec_())
