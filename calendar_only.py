import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt5.QtCore import QDate
import calendar


class CustomCalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_date = QDate.currentDate()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # 添加年份和月份导航按钮
        self.navigation_layout = QHBoxLayout()
        self.prev_year_button = QPushButton('<<')
        self.prev_month_button = QPushButton('<')
        self.next_month_button = QPushButton('>')
        self.next_year_button = QPushButton('>>')

        self.navigation_layout.addWidget(self.prev_year_button)
        self.navigation_layout.addWidget(self.prev_month_button)
        self.navigation_layout.addWidget(self.next_month_button)
        self.navigation_layout.addWidget(self.next_year_button)

        self.layout.addLayout(self.navigation_layout)

        # 添加显示年份和月份的标签和快速跳转按钮的水平布局
        self.date_and_button_layout = QHBoxLayout()
        self.label_date = QLabel(self)
        font = self.label_date.font()
        font.setPointSize(16)
        self.label_date.setFont(font)
        self.date_and_button_layout.addWidget(self.label_date)

        # 添加快速跳转按钮
        self.jump_to_today_button = QPushButton('今天')
        self.jump_to_today_button.setFixedSize(50, 50)
        self.jump_to_today_button.clicked.connect(self.jump_to_today)
        self.date_and_button_layout.addWidget(self.jump_to_today_button)

        self.layout.addLayout(self.date_and_button_layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        # 添加选中日期显示标签
        self.selected_date_label = QLabel(self)
        self.selected_date_label.setText("未选中任何日期")
        self.layout.addWidget(self.selected_date_label)

        self.setLayout(self.layout)

        # 连接信号和槽
        self.prev_year_button.clicked.connect(self.show_prev_year)
        self.prev_month_button.clicked.connect(self.show_prev_month)
        self.next_month_button.clicked.connect(self.show_next_month)
        self.next_year_button.clicked.connect(self.show_next_year)

        self.update_calendar()
        self.setWindowTitle('日历')
        self.show()

    def update_calendar(self):
        # 更新显示的年份和月份
        year = self.current_date.year()
        month = self.current_date.month()
        self.label_date.setText(f"{year}年{month}月")

        # 清空当前网格布局中的部件
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        days_of_week = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        for col, day in enumerate(days_of_week):
            self.grid_layout.addWidget(QLabel(day), 0, col)

        # 获取当月的日期信息
        cal = calendar.Calendar(firstweekday=0)  # 以周一为一周的第一天
        month_days = cal.monthdayscalendar(year, month)

        # 填充日期
        for row, week in enumerate(month_days, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    btn = QPushButton(str(day))
                    btn.setFixedSize(200, 100)
                    btn.clicked.connect(lambda checked, d=day: self.date_selected(d))
                    self.grid_layout.addWidget(btn, row, col)

    def date_selected(self, day):
        self.selected_date_label.setText(f"成功选中{self.current_date.year()}年{self.current_date.month()}月{day}日")

    def show_prev_year(self):
        self.current_date = self.current_date.addYears(-1)
        self.update_calendar()

    def show_prev_month(self):
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar()

    def show_next_month(self):
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar()

    def show_next_year(self):
        self.current_date = self.current_date.addYears(1)
        self.update_calendar()

    def jump_to_today(self):
        self.current_date = QDate.currentDate()
        self.update_calendar()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CustomCalendarWidget()
    sys.exit(app.exec_())
