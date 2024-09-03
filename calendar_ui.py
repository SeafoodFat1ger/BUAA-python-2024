from PyQt5 import QtCore


class Ui_calendar(object):
    def setupUi(self, calendar):
        calendar.setObjectName("calendar")
        self.retranslateUi(calendar)
        QtCore.QMetaObject.connectSlotsByName(calendar)

    def retranslateUi(self, calendar):
        _translate = QtCore.QCoreApplication.translate
        calendar.setWindowTitle(_translate("calendar", "Form"))
