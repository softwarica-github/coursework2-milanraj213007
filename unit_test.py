import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import sys
import time
 
# Import the module containing the GUI and password cracking logic
from Gui import PasswordCrackerMain, stop_event
 
class TestPasswordCracker(unittest.TestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = PasswordCrackerMain()
 
    def tearDown(self):
        self.window.close()
 
    def test_password_cracking(self):
        # Set up the UI
        self.window.zip_file_text.setText("path/to/test.zip")
        self.window.wordlist_text.setText("path/to/wordlist.txt")
        self.window.charset_text.setText("abcdefghijklmnopqrstuvwxyz")
        self.window.start_length_text.setValue(1)
        self.window.end_length_text.setValue(3)
 
 
        # Click browse buttons
        QTest.mouseClick(self.window.zip_file_browse_button, Qt.LeftButton)
        QTest.mouseClick(self.window.wordlist_browse_button, Qt.LeftButton)
 
        # Start password cracking
        self.window.start_password_cracking()
 
        # Ensure stop button is enabled and start button is disabled
        self.assertTrue(self.window.stop_crack_button.isEnabled())
        self.assertFalse(self.window.start_crack_button.isEnabled())
 
        # Simulate password found
        self.window.password_found("Password found: test123")
 
        # Ensure stop button is disabled, start button is enabled, and log contains the password
        self.assertFalse(self.window.stop_crack_button.isEnabled())
        self.assertTrue(self.window.start_crack_button.isEnabled())
        self.assertIn("Password found: test123", self.window.log_text.toPlainText())
 
        # Stop password cracking
        self.window.stop_password_cracking()
 
        # Ensure stop button is disabled and start button is enabled
        self.assertFalse(self.window.stop_crack_button.isEnabled())
        self.assertTrue(self.window.start_crack_button.isEnabled())
 
        # Ensure the global stop event is cleared
        self.assertFalse(stop_event.is_set())
 
if __name__ == '__main__':
    unittest.main()
 