import sys

from PyQt5.QtGui import QPalette, QBrush, QPixmap

from controllers.importexcel import mywindow
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = mywindow()

    ui.show()
    sys.exit(app.exec_())