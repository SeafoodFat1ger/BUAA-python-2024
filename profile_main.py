from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea,
                             QFormLayout, QFrame,
                             QSpacerItem, QSizePolicy, QFileDialog, QDialog, QLineEdit, QDialogButtonBox, QDateEdit,
                             QMessageBox, QTimeEdit, QPushButton)
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtCore import Qt, QDate, QUrl, QRectF
from qfluentwidgets import PushButton
import main_main

import login_main
from database import get_user_database, modify_user_database, add_hope_database, get_hope_list_database, \
    modify_hope_database, delete_hope_database, delete_user_database
from hope import Hope
from img import upload_image_to_imgur
from profile_ui import Ui_profile
from user import User
from login_main import *


class RoundedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, event):
        path = QPainterPath()
        path.addEllipse(QRectF(0, 0, self.width(), self.height()))
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setClipPath(path)
        super().paintEvent(event)

    def setPixmap(self, pixmap):
        if not pixmap.isNull():
            cropped_pixmap = QPixmap(pixmap.size())
            cropped_pixmap.fill(Qt.transparent)

            painter = QPainter(cropped_pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(QRectF(0, 0, pixmap.width(), pixmap.height()))
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()

            super().setPixmap(cropped_pixmap)


class Profile(Ui_profile, QWidget):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.user = get_user_database(self.id)
        main_layout = QVBoxLayout()

        header = self.create_header()
        main_layout.addLayout(header)

        # 任务滚动显示
        self.scroll_area = QScrollArea()
        self.task_widget = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_layout.setSpacing(5)
        self.task_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.task_widget.setLayout(self.task_layout)
        self.scroll_area.setWidget(self.task_widget)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        add_countdown_button = PushButton("+")
        add_countdown_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CB6C0;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                font-size: 16px;
                                                padding: 5px 20px;
                                            }
                                        """)
        add_countdown_button.clicked.connect(self.open_add_task_dialog)
        main_layout.addWidget(add_countdown_button)

        self.setLayout(main_layout)
        self.initHope()

    def initHope(self):
        ls = get_hope_list_database(self.id)
        for hope in ls:
            self.add_task(hope.id, hope.title, hope.ddl)

    def create_header(self):
        header_layout = QVBoxLayout()

        profile_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        self.headLabel = RoundedLabel(self)
        self.headLabel.setFixedSize(100, 100)
        self.headLabel.setAlignment(Qt.AlignCenter)
        self.updateHeadImage(self.user.head_image)


        switch_image_btn = PushButton("切换头像")
        switch_image_btn.setStyleSheet("""
                                                            QPushButton {
                                                                background-color: #4CAfAf;
                                                                color: white;
                                                                border: none;
                                                                border-radius: 5px;
                                                                font-size: 12px;
                                                                padding: 5px 15px;
                                                            }
                                                        """)
        switch_image_btn.clicked.connect(self.uploadImage)

        left_layout.addWidget(self.headLabel)
        left_layout.addWidget(switch_image_btn)

        profile_layout.addLayout(left_layout)

        details_layout = QFormLayout()

        self.account_label = QLabel(self.user.account)
        self.name_label = QLabel(self.user.name)
        self.email_label = QLabel(self.user.email)
        self.timeLayout = QHBoxLayout()
        self.startTime = QLabel(self.user.start)
        self.endTime = QLabel(self.user.end)
        self.timeLayout.addWidget(self.startTime)
        self.timeLayout.addWidget(QLabel('-'))
        self.timeLayout.addWidget(self.endTime)
        self.timeLayout.addStretch(1)

        details_layout.addRow(QLabel(""))
        details_layout.addRow(QLabel("昵称:"), self.name_label)
        details_layout.addRow(QLabel("帐号:"), self.account_label)
        details_layout.addRow(QLabel("邮箱:"), self.email_label)
        details_layout.addRow(QLabel("工作时间:"), self.timeLayout)

        profile_layout.addLayout(details_layout)

        header_buttons_layout = QVBoxLayout()

        edit_info_btn = PushButton("编辑资料")
        edit_info_btn.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: #4CAfAf;
                                                        color: white;
                                                        border: none;
                                                        border-radius: 5px;
                                                        font-size: 12px;
                                                        padding: 5px 15px;
                                                    }
                                                """)
        edit_info_btn.clicked.connect(self.edit_info)

        logout_button = PushButton("退出账号")
        logout_button.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: #4CAfAf;
                                                        color: white;
                                                        border: none;
                                                        border-radius: 5px;
                                                        font-size: 12px;
                                                        padding: 5px 15px;
                                                    }
                                                """)
        logout_button.clicked.connect(self.logout)

        header_buttons_layout.addWidget(edit_info_btn)
        header_buttons_layout.addWidget(logout_button)
        profile_layout.addLayout(header_buttons_layout)

        header_layout.addLayout(profile_layout)

        return header_layout

    def cancel(self):
        reply = QMessageBox.question(self, '确认注销', '你确定要注销账号吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            success, message = self.remove_user_from_database(self.id)
            if success:
                QMessageBox.information(self, '注销成功', '用户已成功注销。')

                # 关闭当前窗口
                self.close()

                # 关闭主窗口
                for widget in QApplication.topLevelWidgets():
                    if isinstance(widget, main_main.window_main):
                        widget.close()

                # 显示登录窗口
                self.login_window = login_main.login_main()
                self.login_window.show()
            else:
                QMessageBox.warning(self, '注销失败', message)


    def remove_user_from_database(self, user_id):
        # 实现从数据库中删除用户的逻辑
        try:
            success = delete_user_database(user_id)
            if success:
                return True, ""
            else:
                return False, "无法删除用户数据"
        except Exception as e:
            return False, str(e)

    def logout(self):
        reply = QMessageBox.question(self, '确认退出', '你确定要退出账号吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # 清除用户会话信息

            # 关闭当前窗口
            self.close()

            # 关闭主窗口
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, main_main.window_main):
                    widget.close()

            # 显示登录窗口
            self.login_window = login_main.login_main()
            self.login_window.show()

    def updateHeadImage(self, imagePath):
        manager = QNetworkAccessManager(self)
        manager.finished.connect(self.onImageLoaded)
        request = QNetworkRequest(QUrl(imagePath))
        manager.get(request)

    def onImageLoaded(self, reply):
        if reply.error() == 0:  # 没有error
            data = reply.readAll()
            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.headLabel.setPixmap(pixmap.scaled(self.headLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            print(f"Error: {reply.errorString()}")

    def uploadImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(self, "选择头像", "", "Images (*.png *.xpm *.jpg);;All Files (*)",
                                                  options=options)
        if filePath:
            url = upload_image_to_imgur(filePath)
            self.user.head_image = url
            modify_user_database(self.user)
            self.updateHeadImage(url)

    def delet_task(self, task_frame, taskLabel):
        currentText = taskLabel.text()
        colon_index = currentText.find(':')
        number_part = currentText[:colon_index]
        task_id = int(number_part)
        success, message = delete_hope_database(self.id, task_id)
        if success:
            self.task_layout.removeWidget(task_frame)
            task_frame.deleteLater()
            QMessageBox.information(self, '删除成功', '倒计时已成功删除。')
        else:
            QMessageBox.warning(self, '删除失败', message)

    def edit_task(self, taskLabel, old_title, old_date, taskFrame):
        currentText = taskLabel.text()
        colon_index = currentText.find(':')
        number_part = currentText[:colon_index]
        task_id = int(number_part)

        dialog = QDialog(self)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        dialog.setWindowTitle("编辑任务")

        form_layout = QFormLayout()
        old_title = currentText.split(':')[1].strip()
        task_name_edit = QLineEdit(old_title)
        deadline_edit = QDateEdit(calendarPopup=True)
        deadline_edit.setDate(QDate.fromString(old_date, "yyyy/MM/dd"))
        deadline_edit.setDisplayFormat("yyyy/MM/dd")
        form_layout.addRow("任务名称:", task_name_edit)
        form_layout.addRow("截止时间:", deadline_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.save_edited_task(task_id, dialog, taskFrame, task_name_edit.text(),
                                                                  deadline_edit.date().toString("yyyy/MM/dd")))
        button_box.rejected.connect(dialog.reject)

        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def save_edited_task(self, task_id, dialog, task_frame, new_title, new_deadline):
        if new_title:
            task_layout = task_frame.layout()
            task_label = task_layout.itemAt(0).widget()
            countdown_label = task_layout.itemAt(1).widget()
            date_label = task_layout.itemAt(2).widget()

            current_date = QDate.currentDate()
            days_remaining = current_date.daysTo(QDate.fromString(new_deadline, "yyyy/MM/dd"))
            task_label.setText(f"{task_id}:   {new_title}")
            days_remaining = int(days_remaining)
            if days_remaining < 0:
                countdown_label.setText(f"已经过去 {-days_remaining}天")
            else:
                countdown_label.setText(f"还剩 {days_remaining}天")
            date_label.setText(new_deadline)
            # 更新数据库中的任务信息
            new_hope = Hope(
                title=new_title,
                ddl=new_deadline
            )
            new_hope.id = task_id
            modify_hope_database(self.id, new_hope)

            dialog.accept()
        else:
            QMessageBox.warning(self, '操作无效', '标题不能为空')
            return

    def create_task(self, id, title, countdown, date):
        task_frame = QFrame()
        task_frame.setFrameShape(QFrame.StyledPanel)
        task_frame.setFrameShadow(QFrame.Raised)

        task_layout = QHBoxLayout()
        task_label = QLabel(f"{id}:   {title}")
        task_label.setStyleSheet("border: none;font-size: 16px;font-weight: bold")
        countdown_label = QLabel()
        countdown = int(countdown)
        if countdown < 0:
            countdown_label.setText(f"已经过去 {-countdown}天")
        else:
            countdown_label.setText(f"还剩 {countdown}天")

        countdown_label.setStyleSheet("border: none;font-size: 16px;font-weight: bold")
        date_label = QLabel(date)
        date_label.setStyleSheet("border: none; color:grey")

        edit_button = QPushButton("  ✎")
        edit_button.setStyleSheet("border: none; font-size:16px")
        edit_button.clicked.connect(lambda: self.edit_task(task_label, title, date, task_frame))

        delete_button = QPushButton("  ✖")
        delete_button.setStyleSheet("border: none; font-size:16px")
        delete_button.clicked.connect(lambda: self.delet_task(task_frame, task_label))

        task_layout.addWidget(task_label)
        task_layout.addStretch(1)
        task_layout.addWidget(countdown_label)
        task_layout.addStretch(2)
        task_layout.addWidget(date_label)
        task_layout.addStretch(4)
        task_layout.addWidget(edit_button)
        task_layout.addWidget(delete_button)

        task_frame.setLayout(task_layout)

        # 设置背景色
        task_frame.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            border: 1px solid #dcdcdc;
        """)

        return task_frame

    def add_task(self, id, title, deadline):
        current_date = QDate.currentDate()
        days_remaining = current_date.daysTo(QDate.fromString(deadline, 'yyyy/MM/dd'))
        new_task = self.create_task(id, title, f"{days_remaining}", deadline)
        self.task_layout.insertWidget(self.task_layout.count() - 1, new_task)

    def open_add_task_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        dialog.setWindowTitle("增添倒计时")

        form_layout = QFormLayout()
        task_name_edit = QLineEdit()
        deadline_edit = QDateEdit(calendarPopup=True)
        deadline_edit.setDate(QDate.currentDate())
        deadline_edit.setDisplayFormat("yyyy/MM/dd")
        form_layout.addRow("任务名称:", task_name_edit)
        form_layout.addRow("截止时间:", deadline_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.save_task(dialog, task_name_edit.text(), deadline_edit.text()))
        button_box.rejected.connect(dialog.reject)

        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def save_task(self, dialog, title, deadline):
        if title:
            hope = Hope(
                title=title,
                ddl=deadline
            )
            add_hope_database(self.id, hope)
            self.add_task(hope.id, title, deadline)
            dialog.accept()
        else:
            QMessageBox.warning(self, '操作无效', '标题不能为空')
            return

    def edit_info(self):
        dialog = QDialog(self)
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        dialog.setWindowTitle("编辑资料")

        form_layout = QVBoxLayout()
        nickname_edit = QLineEdit(self.user.name)
        email_edit = QLineEdit(self.user.email)
        startTimeEdit = QTimeEdit(self)
        endTimeEdit = QTimeEdit(self)
        startTimeEdit.setDisplayFormat("HH:mm")
        endTimeEdit.setDisplayFormat("HH:mm")


        form_layout.addWidget(QLabel('昵称:'))
        form_layout.addWidget(nickname_edit)
        form_layout.addWidget(QLabel('邮箱:'))
        form_layout.addWidget(email_edit)
        form_layout.addWidget(QLabel('工作时间:'))
        timeLayout = QHBoxLayout()
        timeLayout.addWidget(startTimeEdit)
        timeLayout.addWidget(QLabel('到'))
        timeLayout.addWidget(endTimeEdit)
        form_layout.addLayout(timeLayout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.save_info(dialog, nickname_edit.text(), email_edit.text(),
                                                           startTimeEdit.time().toString("HH:mm"),
                                                           endTimeEdit.time().toString("HH:mm")))
        button_box.rejected.connect(dialog.reject)

        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(button_box)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def save_info(self, dialog, name, email, start, end):
        newUser = User(
            id=self.user.id,
            account=self.user.account,
            password=self.user.password,
            name=name,
            email=email,
            start=start,
            end=end,
            head_image=self.user.head_image
        )
        modify_user_database(newUser)
        self.user = newUser
        self.account_label.setText(self.user.account)
        self.name_label.setText(self.user.name)
        self.email_label.setText(self.user.email)
        self.startTime.setText(self.user.start)
        self.endTime.setText(self.user.end)
        dialog.accept()

    def resetForm(self):
        print("切换到个人系统页面")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Profile(0)
    ex.show()
    sys.exit(app.exec_())
