import maya.cmds as mc
import maya.OpenMayaUI as omui

from PySide2 import QtCore
from PySide2 import QtWidgets

from shiboken2 import wrapInstance


def mayaMainWindow():
    mainWindowPTR = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindowPTR), QtWidgets.QWidget)

class TestDialog(QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(TestDialog, self).__init__(parent)

        self.setWindowTitle("Test")
        self.setMinimumWidth(200)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint) #Remove the ? button

        self.createWidgets()
        self.createLayouts()

    def createWidgets(self):
        self.lineEdit = QtWidgets.QLineEdit()
        self.checkbox1 = QtWidgets.QCheckBox("Chbox 1")
        self.checkbox2 = QtWidgets.QCheckBox("Chbox 2")
        self.okBTN = QtWidgets.QPushButton("OK")
        self.cancelBTN = QtWidgets.QPushButton("Cancel")

    def createLayouts(self):
    
        mainLayout = QtWidgets.QVBoxLayout(self)

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow("Name: ", self.lineEdit)
        formLayout.addRow("Hidden: ", self.checkbox1)
        formLayout.addRow("Locked: ", self.checkbox2)

        buttonsLayout = QtWidgets.QHBoxLayout()
        buttonsLayout.addStretch()
        buttonsLayout.addWidget(self.okBTN)
        buttonsLayout.addWidget(self.cancelBTN)

        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonsLayout)

    def printHelloName(self):
        name = self.lineEdit.text()
        print(f"Hello {name}")

if __name__ == "__main__":
    #TODO: Replace the variable window by the one of the program (window is only for testing)

    try:
        window.close() # type: ignore
        window.deleteLater() # type: ignore
    except:
        pass

    window = TestDialog()
    window.show()
