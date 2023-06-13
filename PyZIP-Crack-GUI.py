import sys, zipfile, itertools, threading
from PyQt5 import QtCore, QtGui, QtWidgets

# Define a global variable to signal the password cracking loop to stop
stop_event = threading.Event()

# Define a signal handler to catch the SIGINT signal
def signal_handler(sig, frame):
    global stop_event
    print('Exited')
    stop_event.set()
    sys.exit()

def extract_zip(zip_file, start_length, max_length, wordlist, charset, callback):
    
    if wordlist:
        # Detect the encoding of the wordlist file
        with open(wordlist, 'r', errors='ignore') as f:
            passwords = f.read().splitlines()
            
        # Filter the passwords list to only include passwords within the desired length range
        passwords = [password for password in passwords if start_length <= len(password) <= max_length]
    else:
        # Generate all possible password combinations
        passwords = (''.join(password) for length in range(start_length, max_length+1) for password in itertools.product(charset, repeat=length))

    for password in passwords:
        ''' Set comments according to which print method you'd like '''
        if stop_event.is_set():
            return None
            
        try:
            password = password.decode('utf-8')
        except:
            password = password
        
        callback.emit(f"Trying password: {password}") # New line every print

        # Attempt to extract the ZIP file with the current password
        try:
            zip_file.extractall(pwd=password.encode())
            return password
        except:
            pass

    # If no password was found, return None
    return None
       
     
class PasswordCrackingThread(QtCore.QThread):
    log = QtCore.pyqtSignal(str)
    password_found = QtCore.pyqtSignal(str)
    process_stopped = QtCore.pyqtSignal()

    def __init__(self, zip_path, min_length, max_length, wordlist, charset, parent=None):
        super().__init__(parent)
        self.zip_path = zip_path
        self.min_length = min_length
        self.max_length = max_length
        self.wordlist = wordlist
        self.charset = charset

    def run(self):
        global stop_event
        # Open the ZIP file
        try:
            zip_file = zipfile.ZipFile(self.zip_path)
        except:
            self.log.emit("Error: Unable to open the ZIP file")
            self.process_stopped.emit()
            return

        # Extract the ZIP file using a brute-force attack
        password = extract_zip(zip_file, self.min_length, self.max_length, self.wordlist, self.charset, self.log)

        if password is None:
            self.log.emit("Password not found")
            self.process_stopped.emit()
        else:
            self.password_found.emit(f"Password found: {password}")
            

class PasswordCrackerGUI(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(603, 505)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.zip_file_text = QtWidgets.QLineEdit(self.centralwidget)
        self.zip_file_text.setGeometry(QtCore.QRect(173, 10, 321, 25))
        self.zip_file_text.setObjectName("zip_file_text")
        self.zip_file_browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.zip_file_browse_button.setGeometry(QtCore.QRect(503, 10, 87, 25))
        self.zip_file_browse_button.setObjectName("zip_file_browse_button")
        self.zip_label = QtWidgets.QLabel(self.centralwidget)
        self.zip_label.setGeometry(QtCore.QRect(88, 13, 81, 16))
        self.zip_label.setObjectName("zip_label")
        self.wordlist_browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.wordlist_browse_button.setGeometry(QtCore.QRect(503, 40, 87, 25))
        self.wordlist_browse_button.setObjectName("wordlist_browse_button")
        self.wordlist_text = QtWidgets.QLineEdit(self.centralwidget)
        self.wordlist_text.setGeometry(QtCore.QRect(173, 40, 321, 25))
        self.wordlist_text.setObjectName("wordlist_text")
        self.wordlist_label = QtWidgets.QLabel(self.centralwidget)
        self.wordlist_label.setGeometry(QtCore.QRect(4, 43, 161, 20))
        self.wordlist_label.setObjectName("wordlist_label")
        self.start_length_label = QtWidgets.QLabel(self.centralwidget)
        self.start_length_label.setGeometry(QtCore.QRect(57, 103, 111, 20))
        self.start_length_label.setObjectName("start_length_label")
        self.end_length_label = QtWidgets.QLabel(self.centralwidget)
        self.end_length_label.setGeometry(QtCore.QRect(219, 103, 91, 20))
        self.end_length_label.setObjectName("end_length_label")
        self.log_text = QtWidgets.QTextEdit(self.centralwidget)
        self.log_text.setGeometry(QtCore.QRect(10, 183, 581, 281))
        self.log_text.setReadOnly(True)
        self.log_text.setObjectName("log_text")
        self.log_label = QtWidgets.QLabel(self.centralwidget)
        self.log_label.setGeometry(QtCore.QRect(260, 157, 81, 17))
        self.log_label.setObjectName("log_label")
        self.start_crack_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_crack_button.setGeometry(QtCore.QRect(356, 100, 121, 25))
        self.start_crack_button.setObjectName("start_crack_button")
        self.stop_crack_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_crack_button.setGeometry(QtCore.QRect(480, 100, 111, 25))
        self.stop_crack_button.setObjectName("stop_crack_button")
        self.clear_log_button = QtWidgets.QPushButton(self.centralwidget)
        self.clear_log_button.setGeometry(QtCore.QRect(10, 470, 581, 25))
        self.clear_log_button.setObjectName("clear_log_button")
        self.seperator = QtWidgets.QFrame(self.centralwidget)
        self.seperator.setGeometry(QtCore.QRect(0, 140, 601, 16))
        self.seperator.setFrameShape(QtWidgets.QFrame.HLine)
        self.seperator.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.seperator.setObjectName("seperator")
        self.charset_label = QtWidgets.QLabel(self.centralwidget)
        self.charset_label.setGeometry(QtCore.QRect(50, 75, 111, 17))
        self.charset_label.setObjectName("charset_label")
        self.charset_text = QtWidgets.QLineEdit(self.centralwidget)
        self.charset_text.setGeometry(QtCore.QRect(173, 70, 418, 25))
        self.charset_text.setProperty("text", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+{}[]|\\;:'\"/?,.<>")
        self.charset_text.setObjectName("charset_text")
        self.start_length_text = QtWidgets.QSpinBox(self.centralwidget)
        self.start_length_text.setGeometry(QtCore.QRect(173, 100, 41, 26))
        self.start_length_text.setMinimum(1)
        self.start_length_text.setProperty("value", 1)
        self.start_length_text.setObjectName("start_length_text")
        self.end_length_text = QtWidgets.QSpinBox(self.centralwidget)
        self.end_length_text.setGeometry(QtCore.QRect(309, 100, 41, 26))
        self.end_length_text.setMinimum(1)
        self.end_length_text.setProperty("value", 8)
        self.end_length_text.setObjectName("end_length_text")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.zip_file_browse_button.setText(_translate("MainWindow", "Browse"))
        self.zip_label.setText(_translate("MainWindow", "ZIP File:"))
        self.wordlist_browse_button.setText(_translate("MainWindow", "Browse"))
        self.wordlist_label.setText(_translate("MainWindow", "Wordlist (Optional):"))
        self.start_length_label.setText(_translate("MainWindow", "Start Length:"))
        self.end_length_label.setText(_translate("MainWindow", "End Length:"))
        self.log_label.setText(_translate("MainWindow", "Log Output"))
        self.start_crack_button.setText(_translate("MainWindow", "Start Cracking"))
        self.stop_crack_button.setText(_translate("MainWindow", "Stop Cracking"))
        self.clear_log_button.setText(_translate("MainWindow", "Clear Log"))
        self.charset_label.setText(_translate("MainWindow", "Character Set:"))


class PasswordCrackerMain(QtWidgets.QMainWindow, PasswordCrackerGUI):
    def __init__(self):
        super(PasswordCrackerMain, self).__init__()
        self.setupUi(self)
        
        self.zip_file_browse_button.clicked.connect(self.browse_zip)
        self.wordlist_browse_button.clicked.connect(self.browse_wordlist)
        self.start_crack_button.clicked.connect(self.start_password_cracking)
        self.stop_crack_button.clicked.connect(self.stop_password_cracking)
        self.clear_log_button.clicked.connect(self.log_text.clear)
        
    def browse_zip(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open ZIP file', '', 'ZIP files (*.zip)')
        if file_path:
            self.zip_file_text.setText(file_path)
            
    def browse_wordlist(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open wordlist file')
        if file_path:
            self.wordlist_text.setText(file_path)
            
    def start_password_cracking(self):
        self.start_crack_button.setEnabled(False)
        self.stop_crack_button.setEnabled(True)
        self.log_text.clear()

        # Start the password cracking thread
        self.password_cracking_thread = PasswordCrackingThread(
            self.zip_file_text.text(),
            self.start_length_text.value(),
            self.end_length_text.value(),
            self.wordlist_text.text(),
            self.charset_text.text(),
            self
        )
        self.password_cracking_thread.process_stopped.connect(self.process_stopped)
        self.password_cracking_thread.log.connect(self.log_text.setPlainText)
        self.password_cracking_thread.password_found.connect(self.password_found)
        self.password_cracking_thread.start()
        
    def stop_password_cracking(self):
        global stop_event
        self.start_crack_button.setEnabled(True)
        self.stop_crack_button.setEnabled(False)

        # Set the stop event and wait for the password cracking thread to finish
        stop_event.set()
        if self.password_cracking_thread is not None:
            self.password_cracking_thread.wait()
        stop_event.clear()
        
    def password_found(self, password):
        self.start_crack_button.setEnabled(True)
        self.stop_crack_button.setEnabled(False)
        self.log_text.append(password)
        
    def process_stopped(self):
        self.start_crack_button.setEnabled(True)
        self.stop_crack_button.setEnabled(False)
        
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    cracker = PasswordCrackerMain()
    cracker.show()
    sys.exit(app.exec_())
