from PyQt5 import QtCore


class Ui_profile(object):
    def setupUi(self, calendar):
        calendar.setObjectName("profile")
        self.retranslateUi(calendar)
        QtCore.QMetaObject.connectSlotsByName(calendar)

    def retranslateUi(self, calendar):
        _translate = QtCore.QCoreApplication.translate
        calendar.setWindowTitle(_translate("profile", "Form"))
