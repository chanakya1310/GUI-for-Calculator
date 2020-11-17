import sys
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial

ERROR_MSG =  'ERROR'
def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = ERROR_MSG
    return result
    
class PyCalcUi(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyCalc')
        self.setFixedSize(500, 500) # Used to fix the GUI size

        self.generalLayout = QVBoxLayout()

        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)

        self._centralWidget.setLayout(self.generalLayout)
        #since your GUI class inherits from QMainWindow, you need a central widget. 
        # This object will be the parent for the rest of the GUI component.

        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()

        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignBaseline)
        self.display.setReadOnly(True)

        self.generalLayout.addWidget(self.display)

    def _createButtons(self):

        self.buttons = {}
        buttonsLayout = QGridLayout()
        buttons = {
            '7' : (0, 0),
            '8' : (0, 1),
            '9' : (0, 2),
            '/' : (0, 3),
            'C' : (0, 4),
            '4' : (1, 0),
            '5' : (1, 1),
            '6' : (1, 2),
            '*' : (1, 3),
            '(' : (1, 4),
            '1' : (2, 0),
            '2' : (2, 1),
            '3' : (2, 2),
            '-' : (2, 3),
            ')' : (2, 4),
            '0' : (3, 0),
            '00' : (3, 1),
            '.' : (3, 2),
            '+' : (3, 3),
            '=' : (3, 4)
        }
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(100, 100)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        
        self.generalLayout.addLayout(buttonsLayout)
    
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()
        # setFocus() to set the cursor’s focus on the display.

    def displayText(self):
        """
        displayText() is a getter method that returns the display’s current text. 
        When the user clicks on the equals sign (=), the program will use the return value 
        of .displayText() as the math expression to be evaluated.
        """
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText('')

#Controller Class to connect the GUI and the model

class PyCalcCtrl:

    def __init__(self, model, view):
        self._evaluate = model
        self._view = view

        #Connect Signals and slots
        self._connectSignals()
        # self._view.show()
    
    def _calculateResult(self):

        result = self._evaluate(expression = self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        
        if self._view.displayText() == ERROR_MSG:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)
    
    def _connectSignals(self):

        for btnText, btn in self._view.buttons.items():
            if btnText not in {'=', 'C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self._view.buttons['='].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)
        self._view.buttons['C'].clicked.connect(self._view.clearDisplay)

    

def main():
    pycalc = QApplication(sys.argv)

    view = PyCalcUi()
    view.show()

    model = evaluateExpression
    PyCalcCtrl(model = model, view = view)

    sys.exit(pycalc.exec_())

if __name__ == '__main__':
    main()
