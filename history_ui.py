from PyQt5 import QtCore


class Ui_history(object):
    def setupUi(self, calendar):
        calendar.setObjectName("history")
        self.retranslateUi(calendar)
        QtCore.QMetaObject.connectSlotsByName(calendar)

    def retranslateUi(self, calendar):
        _translate = QtCore.QCoreApplication.translate
        calendar.setWindowTitle(_translate("history", "Form"))
