from PyQt5 import QtCore


class Ui_login(object):
    def setupUi(self, calendar):
        calendar.setObjectName("login")
        self.retranslateUi(calendar)
        QtCore.QMetaObject.connectSlotsByName(calendar)

    def retranslateUi(self, calendar):
        _translate = QtCore.QCoreApplication.translate
        calendar.setWindowTitle(_translate("login", "Form"))
