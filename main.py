import sys, time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QProgressBar, QDialog
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import Qt, QTimer

value = 0

class GuessTheNumber(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mind Reader")
        self.setWindowIcon(QIcon("icons/brain.png"))
        self.setMinimumSize(250,100)
        self.setMaximumSize(250,100)
         
        layout = QVBoxLayout()
        
        name = QLabel("Think of a number between 0 and 1000")
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.number = QLineEdit()
        self.number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.button = QPushButton("Read My Mind")
        self.button.clicked.connect(self.NumberValidate)
        
        layout.addWidget(name)
        layout.addWidget(self.number)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
    def NumberValidate(self):
        try:
            number = int(self.number.text())
            if 0 > number or 1000 < number:
                dialog = Error()
                dialog.exec()
            else:
                self.number.clear()
                progress = Progression()
                progress.exec()
                dialog = NumberDisplay(number)
                dialog.exec()
                
        except ValueError:
            dialog = Error()
            dialog.exec()


class Error(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invalid Input!")
        self.setWindowIcon(QIcon("icons/error.png"))
        content = """
        <p>Please enter a valid number between 0 and 1000.</p>
        """
        self.setText(content)
    
    
class NumberDisplay(QMessageBox):
    def __init__(self,number):
        super().__init__()
        self.setWindowTitle("Mind Result")
        self.setWindowIcon(QIcon("icons/answer"))
        content = f"""
        <p><b>The number you thought of is {number}<b></p>
        """
        self.setText(content)    
    
    
class Progression(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reading Your Mind")
        self.setWindowIcon(QIcon("icons/analysis.png"))
        
        layout = QVBoxLayout()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(35)
        
        self.label = QLabel("Analyzing brainwaves...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.progressBar = QProgressBar()
        layout.addWidget(self.label)
        layout.addWidget(self.progressBar)
        
        self.setLayout(layout)
        
    def updateProgress(self):
        global value
        self.progressBar.setValue(value)
        
        if value > 100:
            self.timer.stop()
            self.close()   
            value = 0
        
        if value == 30:
            self.label.setText("Scanning memories...")
        elif value == 60:
            self.label.setText("Examining neural pathways...")
        elif value == 90:
            self.label.setText("Interpreting results...")
        
        value += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GuessTheNumber()
    window.show()
    sys.exit(app.exec())