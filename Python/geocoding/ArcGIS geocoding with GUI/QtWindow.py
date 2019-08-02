from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtCore             # import for logging TextEdit form
import sys                                  # import for logging
import mydesign                             # import generated ui file
from main_geo_module import main_geo_func   # import geocoding module
import images_rc                            # import file with resouces
import webbrowser


class Stream(QtCore.QObject):
    newText = QtCore.pyqtSignal(str)
    def write(self, text):
        self.newText.emit(str(text))

# #### Add after
#     def __init__(self, io_stream):
#         super().__init__()
#         self.io_stream = io_stream

#     def write(self, text):
#         self.io_stream.write(text)
#         self.newText.emit(str(text))

#     def flush(self):
#         self.io_stream.flush()

# sys.stdout = Stream(sys.stdout)
# sys.stderr = Stream(sys.stderr)
# #### Add after    

class mywindow(mydesign.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)  # initialize design from import file
        self.file_picker.clicked.connect(self.select_file)
        self.Run_Button.clicked.connect(self.fill_form)
        self.helpButton.clicked.connect(self.open_webbrowser)

        # Install the custom output stream
        sys.stdout = Stream(newText=self.onUpdateText)


# ### Add after 
#         sys.stdout.newText.connect(self.append_log)
#         sys.stderr.newText.connect(self.append_log)

#     def append_log(self, text):
#         text = repr(text)
#         self.log_textEdit.append(text)
# ### Add after 


    def onUpdateText(self, text):
        """Append text to the QTextEdit."""
        cursor = self.log_textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.log_textEdit.setTextCursor(cursor)
        self.log_textEdit.ensureCursorVisible()

    def __del__(self):
        ''' Restore sys.stdout '''
        sys.stdout = sys.__stdout__

    def fill_form(self):
        file = self.import_file_path.text()
        filename = file.split("/")[-1].split(".")[-2] # get name of imported file to put it in output file
        if not file:
            QtWidgets.QMessageBox.about(self, "Ошибка", "Выберите файл для импорта")
            return
        start_index_row = self.start_index_row_box.text()
        save_file_rate = self.save_data_rate_box.text()
        if save_file_rate == "0":
            QtWidgets.QMessageBox.about(self, "Ошибка", "Определите как часто сохранять файл с координатами")
            return
        attempts_quantity = self.attempts_box.text()
        if attempts_quantity == "0":
            QtWidgets.QMessageBox.about(self, "Ошибка", "Определите количество попыток определить координаты. Максимальное количество попыток - 10")
            return
        params = [file, start_index_row, save_file_rate, attempts_quantity, filename] 
        main_geo_func(params)

    def select_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл",
            filter=('Excel files (*.xls, *.xlsx)'))
        # open the file selection dialog and set the variable value to the path to the selected file
        if file_path: # do not execute if the user has not selected a file
            self.import_file_path.setText(file_path)
        return file_path

    def open_webbrowser(self):
        webbrowser.open('https://github.com/fugrusha/blackhole/tree/master/Python/geocoding')




def main():
    app = QtWidgets.QApplication(sys.argv)  # New example of QApplication
    application = mywindow()                # Create object of class mywindow
    application.show()                      # Show windows
    sys.exit(app.exec())                    # run app

if __name__ == "__main__":
    main()