import maya.cmds as mc
import maya.OpenMayaUI as omui
import sys
import os
import importlib

from PySide2 import QtCore
from PySide2 import QtWidgets

from shiboken2 import wrapInstance

script_dir = "E:\KATPC\Programming\ktMayaTools\ktMayaTools"
if script_dir not in sys.path:
    sys.path.append(script_dir)

import util
import kt_randomizer

importlib.reload(util)
importlib.reload(kt_randomizer)


def mayaMainWindow():
    mainWindowPTR = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mainWindowPTR), QtWidgets.QWidget)

if __name__ == "__main__":
    # Create 
    try:
        window.close()  # type: ignore
        window.deleteLater()  # type: ignore
    except:
        pass

    window = kt_randomizer.TestDialog(parent=mayaMainWindow())  
    window.show()