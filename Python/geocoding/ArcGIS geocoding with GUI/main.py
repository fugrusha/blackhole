from PyQt5 import QtWidgets
from QtWindow import mywindow, Stream
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)  # New example of QApplication
    application = mywindow()                # Create object of class mywindow
    application.show()                      # Show windows
    sys.exit(app.exec())                    # run app

if __name__ == "__main__":
    main()