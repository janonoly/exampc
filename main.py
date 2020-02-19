import sys
from controllers.importexcel import mywindow
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = mywindow()


    ui.show()
    sys.exit(app.exec_())