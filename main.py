from login_main import *
from PyQt5.Qt import *
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = login_main()
    win.show()
    sys.exit(app.exec_())
