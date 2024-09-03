import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QIcon

import main_main
from database import *
from login_ui import Ui_login


class login_main(Ui_login, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.id = id
        self.initUI()
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle('登录')
        # 禁止用户更改login界面的大小
        self.setFixedSize(1200, 900)
        self.center()

        connect_database()

    def initUI(self):
        # 设置图片大小
        img1_width = 800
        img1_height = 600
        img2_width = 300
        img2_height = 300

        # 创建标签并设置图片
        self.label1 = QLabel(self)
        pixmap1 = QPixmap('logo_left.png')
        pixmap1 = pixmap1.scaled(img1_width, img1_height)
        self.label1.setScaledContents(True)
        self.label1.setPixmap(pixmap1)

        self.label2 = QLabel(self)
        pixmap2 = QPixmap('LOGO.PNG')
        pixmap2 = pixmap2.scaled(img2_width, img2_height)
        self.label2.setPixmap(pixmap2)

        # 创建登录输入框
        self.account_input_login = QLineEdit(self)
        self.account_input_login.setPlaceholderText('请输入账号')
        self.password_input_login = QLineEdit(self)
        self.password_input_login.setPlaceholderText('请输入密码')
        self.password_input_login.setEchoMode(QLineEdit.Password)

        # 创建注册输入框
        self.account_input_register = QLineEdit(self)
        self.account_input_register.setPlaceholderText('请输入账号')
        self.email_input_register = QLineEdit(self)
        self.email_input_register.setPlaceholderText('请输入邮箱地址')
        self.password_input_register = QLineEdit(self)
        self.password_input_register.setPlaceholderText('请输入密码')
        self.password_input_register.setEchoMode(QLineEdit.Password)
        self.confirm_password_input_register = QLineEdit(self)
        self.confirm_password_input_register.setPlaceholderText('请确认密码')
        self.confirm_password_input_register.setEchoMode(QLineEdit.Password)
        self.auto_login_checkbox = QCheckBox('注册后直接登录')

        # 创建按钮
        self.login_switch = QPushButton('登录', self)
        self.register_switch = QPushButton('注册', self)
        buttons = [self.login_switch, self.register_switch]
        for button in buttons:
            button.setCheckable(True)
            button.setFixedSize(100, 40)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.login_switch.setChecked(True)
        self.updateButtonStyles()

        self.login_button = QPushButton('确 认', self)
        self.login_button.setStyleSheet("""
                                            QPushButton {
                                                background-color: #4CAfAf;
                                                color: white;
                                                border: none;
                                                border-radius: 5px;
                                                font-size: 16px;
                                                padding: 8px 20px;
                                            }
                                        """)


        self.register_button = QPushButton('确 认', self)
        self.register_button.setStyleSheet("""
                                                    QPushButton {
                                                        background-color: #4CAfAf;
                                                        color: white;
                                                        border: none;
                                                        border-radius: 5px;
                                                        font-size: 16px;
                                                        padding: 8px 20px;
                                                    }
                                                """)

        # 创建布局
        self.stacked_layout = QStackedLayout()
        self.login_widget = QWidget()
        self.register_widget = QWidget()

        # 登录布局
        login_layout = QVBoxLayout()
        login_layout.addStretch(1)
        login_layout.addWidget(QLabel('账号:'))
        login_layout.addWidget(self.account_input_login)
        login_layout.addWidget(QLabel('密码:'))
        login_layout.addWidget(self.password_input_login)
        login_layout.addStretch(8)
        login_layout.addWidget(self.login_button)
        self.login_widget.setLayout(login_layout)

        # 注册布局
        register_layout = QVBoxLayout()
        register_layout.addWidget(QLabel('账号:'))
        register_layout.addWidget(self.account_input_register)
        register_layout.addWidget(QLabel('邮箱地址:'))
        register_layout.addWidget(self.email_input_register)
        register_layout.addWidget(QLabel('密码:'))
        register_layout.addWidget(self.password_input_register)
        register_layout.addWidget(QLabel('确认密码:'))
        register_layout.addWidget(self.confirm_password_input_register)
        register_layout.addWidget(self.auto_login_checkbox)
        register_layout.addStretch()
        register_layout.addWidget(self.register_button)
        self.register_widget.setLayout(register_layout)

        self.stacked_layout.addWidget(self.login_widget)
        self.stacked_layout.addWidget(self.register_widget)

        # 创建主布局
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        switch_layout = QHBoxLayout()

        # 左边布局
        left_layout.addWidget(self.label1)

        # 右边布局
        right_layout.addWidget(self.label2)

        # 登陆与注册键
        switch_layout.addWidget(self.login_switch)
        switch_layout.addWidget(self.register_switch)
        right_layout.addLayout(switch_layout)
        right_layout.addLayout(self.stacked_layout)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # 设置窗口主布局
        self.setLayout(main_layout)

        # 连接按钮事件
        self.login_switch.clicked.connect(self.show_login_form)
        self.register_switch.clicked.connect(self.show_register_form)
        self.register_button.clicked.connect(self.handle_register)
        self.login_button.clicked.connect(self.handle_login)

        self.setGeometry(300, 300, 600, 400)
        self.show()


    def center(self):
        # 获取屏幕的中心位置，将窗口移动到该位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_login_form(self):
        self.stacked_layout.setCurrentIndex(0)
        self.login_switch.setChecked(True)
        self.register_switch.setChecked(False)
        self.updateButtonStyles()

    def show_register_form(self):
        self.stacked_layout.setCurrentIndex(1)
        self.register_switch.setChecked(True)
        self.login_switch.setChecked(False)
        self.updateButtonStyles()

    def handle_register(self):
        account = self.account_input_register.text()
        email = self.email_input_register.text()
        password = self.password_input_register.text()
        confirm = self.confirm_password_input_register.text()

        if not account or not email or not password or not confirm:
            QMessageBox.information(self, '错误',
                                    '请输入非空用户名、邮箱地址、密码和确认密码',
                                    QMessageBox.Yes)
        elif password != confirm:
            QMessageBox.information(self, '错误',
                                    '请两次输入相同密码',
                                    QMessageBox.Yes)
        else:
            result, message = sign_up_database(account, email, password)
            if result:
                QMessageBox.information(self, '成功',
                                        '成功注册',
                                        QMessageBox.Yes)
                self.confirm_password_input_register.setPlaceholderText("请确认密码")

                if self.auto_login_checkbox.isChecked():
                    self.account_input_login.setText(account)
                    self.password_input_login.setText(password)
                    self.handle_login()
                else:
                    self.show_login_form()
            else:
                QMessageBox.information(self, '错误',
                                        message,
                                        QMessageBox.Yes)

        self.account_input_register.clear()
        self.email_input_register.clear()
        self.password_input_register.clear()
        self.confirm_password_input_register.clear()
        self.account_input_register.setPlaceholderText("请输入账号")
        self.email_input_register.setPlaceholderText("请输入邮箱地址")
        self.password_input_register.setPlaceholderText("请输入密码")
        self.confirm_password_input_register.setPlaceholderText("请确认密码")

    def handle_login(self):
        account = self.account_input_login.text()
        password = self.password_input_login.text()
        result, id, message = login_in_database(account, password)
        if result:
            self.close()
            MainWindow = main_main.window_main(id=id)
            MainWindow.show()

        else:
            QMessageBox.information(self, '错误',
                                    message,
                                    QMessageBox.Yes | QMessageBox.No)
            self.account_input_login.setText('')
            self.password_input_login.setText('')
            self.account_input_login.setPlaceholderText("请输入账号")
            self.password_input_login.setPlaceholderText("请输入密码")

    def updateButtonStyles(self):
        buttons = [self.login_switch, self.register_switch]
        for button in buttons:
            if button.isChecked():
                button.setStyleSheet("""
                    QPushButton {
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = login_main()
    sys.exit(app.exec_())
