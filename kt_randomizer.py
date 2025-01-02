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
        self.selBTN = QtWidgets.QPushButton("New Sel")
        self.selNumLBL = QtWidgets.QLabel('TEST')
        self.selSLD = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.resultBTN = QtWidgets.QPushButton("New Result")
        self.retouchBTN = QtWidgets.QPushButton("Retouch")
        self.clearBTN = QtWidgets.QPushButton("Clear")

        # --------------------------------------------



    def createLayouts(self):
        
        mainLayout = QtWidgets.QVBoxLayout(self)
        
        mainGridLYT = QtWidgets.QGridLayout(self)
        mainGridLYT.addWidget(self.selBTN, 0,0)
        mainGridLYT.addWidget(self.selNumLBL, 0,1)
        mainGridLYT.addWidget(self.selSLD, 0,2)
        mainGridLYT.addWidget(self.resultBTN, 0,3)
        mainGridLYT.addWidget(self.retouchBTN, 0,4)
        mainGridLYT.addWidget(self.clearBTN, 0,5)

        coordGridLYT = QtWidgets.QGridLayout(self)
        coordGridLYT.addWidget(QtWidgets.QLabel('X'), 1,1)
        coordGridLYT.addWidget(QtWidgets.QLabel('Y'), 1,2)
        coordGridLYT.addWidget(QtWidgets.QLabel('Z'), 1,3)
        coordGridLYT.addWidget(QtWidgets.QLabel('Multiply'), 1,4)
        coordGridLYT.addWidget(QtWidgets.QLabel('Range'), 1,5)
        coordGridLYT.addWidget(QtWidgets.QLabel('Min'), 1,6)
        coordGridLYT.addWidget(QtWidgets.QLabel('Max'), 1,7)


        mainLayout.addLayout(mainGridLYT)
        mainLayout.addLayout(coordGridLYT)


    def printHelloName(self):
        pass

if __name__ == "__main__":
    #TODO: Replace the variable window by the one of the program (window is only for testing)

    try:
        window.close() # type: ignore
        window.deleteLater() # type: ignore
    except:
        pass

    window = TestDialog()
    window.show()
