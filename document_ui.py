from PyQt5 import QtCore


class Ui_document(object):
    def setupUi(self, calendar):
        calendar.setObjectName("document")
        self.retranslateUi(calendar)
        QtCore.QMetaObject.connectSlotsByName(calendar)

    def retranslateUi(self, calendar):
        _translate = QtCore.QCoreApplication.translate
        calendar.setWindowTitle(_translate("document", "Form"))
