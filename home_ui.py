from PyQt5 import QtCore


class Ui_home(object):
    def setupUi(self, calendar):
        calendar.setObjectName("home")
        self.retranslateUi(calendar)
        QtCore.QMetaObject.connectSlotsByName(calendar)

    def retranslateUi(self, calendar):
        _translate = QtCore.QCoreApplication.translate
        calendar.setWindowTitle(_translate("home", "Form"))
