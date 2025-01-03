import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import importlib

from PySide2 import QtCore
from PySide2 import QtWidgets

import util.kt_widgets as ktW
importlib.reload(ktW)


"""
DISCLAIMER:
This file needs to be executed importing it on a parent and with the library kt_widgets included.
This version will be updated so be able to execute it from the main window.

"""




class kt_randomizer(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(kt_randomizer, self).__init__(parent)

        self.setWindowTitle("Randomizer")
        self.setFixedSize(510, 100)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint) #Remove the ? button

        '''
        VARIABLES
        '''
        self.objData = {}

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        self.selBTN = QtWidgets.QPushButton("New Sel")
        self.selBTN.setFixedWidth(70)
        self.selSLD = ktW.ktRangeSlider(devValue=1, minValue=0, maxValue=1, showMinMaxField=False, 
                                        stepSize=0.1, sliderWidth=100)
        self.resultBTN = QtWidgets.QPushButton("New Result")
        self.retouchBTN = QtWidgets.QPushButton("Retouch")
        self.clearBTN = QtWidgets.QPushButton("Clear")
        self.clearBTN.setFixedWidth(50)

        # --------------------------------------------
        self.optionsCMB = QtWidgets.QComboBox()
        self.optionsCMB.addItem('Translate')
        self.optionsCMB.addItem('Rotate')
        self.optionsCMB.addItem('Scale')
        self.xAxisCB = QtWidgets.QCheckBox()
        self.yAxisCB = QtWidgets.QCheckBox()
        self.zAxisCB = QtWidgets.QCheckBox()
        self.transformSLD = ktW.ktRangeSlider(textWidth=55)


    def createLayouts(self):
        
        mainLayout = QtWidgets.QVBoxLayout(self)
        
        """ Main section Grid """
        mainGridLYT = QtWidgets.QGridLayout(self)
        mainGridLYT.addWidget(self.selBTN, 0,0)
        mainGridLYT.addWidget(self.selSLD, 0,1)
        mainGridLYT.addWidget(self.resultBTN, 0,2)
        mainGridLYT.addWidget(self.retouchBTN, 0,3)
        mainGridLYT.addWidget(self.clearBTN, 0,4)

        """ Transformation Grid """
        coordGridLYT = QtWidgets.QGridLayout(self)
        coordGridLYT.setAlignment(QtCore.Qt.AlignCenter)
        coordGridLYT.addWidget(QtWidgets.QLabel('X'), 0,1, alignment=QtCore.Qt.AlignCenter)
        coordGridLYT.addWidget(QtWidgets.QLabel('Y'), 0,2, alignment=QtCore.Qt.AlignCenter)
        coordGridLYT.addWidget(QtWidgets.QLabel('Z'), 0,3, alignment=QtCore.Qt.AlignCenter)
        coordGridLYT.addWidget(QtWidgets.QLabel('Range'), 0,4)
        coordGridLYT.addWidget(QtWidgets.QLabel('Min'), 0,8)
        coordGridLYT.addWidget(QtWidgets.QLabel('Max'), 0,9)

        coordGridLYT.addWidget(self.optionsCMB, 1,0)
        coordGridLYT.addWidget(self.xAxisCB, 1,1)
        coordGridLYT.addWidget(self.yAxisCB, 1,2)
        coordGridLYT.addWidget(self.zAxisCB, 1,3)
        coordGridLYT.addWidget(self.transformSLD, 1,4,1,6)


        mainLayout.addLayout(mainGridLYT)
        mainLayout.addLayout(coordGridLYT)

        self.setLayout(mainLayout)

    def createConnections(self):
        self.selBTN.clicked.connect(self.createSelection)
        self.resultBTN.clicked.connect(self.generateNewResult)
        self.retouchBTN.clicked.connect(self.retouchResult)
        self.clearBTN.clicked.connect(self.clearSelection)
        self.selSLD.valueChangedEvent.connect(self.randomSelection)
        self.transformSLD.valueChangedEvent.connect(self.generateResult)

    def createSelection(self):
        '''
        Save all transformation values, "translate","rotate","scale"
        '''
        self.objData.clear()
        selectedObjects = mc.ls(selection=True)

        if selectedObjects:
            for obj in selectedObjects:
                translate = mc.xform(obj, query=True, worldSpace=True, translation=True)
                rotate = mc.xform(obj, query=True, worldSpace=True, rotation=True)
                scale = mc.xform(obj, query=True, worldSpace=True, scale=True)

                self.objData[obj] = {
                    'translation': translate,
                    'rotation': rotate,
                    'scale': scale
                }
        else:
            om.MGlobal.displayError("Please select any object.")

        # Print the dictionary to verify
        print(self.objData)

    
    def generateNewResult(self):
        print("TODO: Generate new result")
        #Does it until there is no more touching
        '''def randomizeAgain(touchingObjects):
            mc.select(touchingObjects)
            newRandomAction()
            mc.select(selectedObjects)

        selectedObjects = mc.ls(selection=True)
        touchingObjects = []
        
        max_iterations = 100
        iteration_count = 0

        #Will break when all objects are in the same position
        while iteration_count < max_iterations:
            touchingObjects = util.intersection.checkTouchingObjList(selectedObjects)
            if touchingObjects:
                randomizeAgain(touchingObjects)
                iteration_count += 1
            else:
                break

        if iteration_count >= max_iterations:
            mc.warning("Max iterations reached. Objects may still be touching.")'''

    def retouchResult(self):
        print("TODO: Retouch")
    
    def clearSelection(self):
        print("TODO: Clear selection")

        """
        - Clear selection
        - Reset selection Slider
        - Reset transform range
        - Clear checkboxes?
        """

    def generateResult(self, value):
        print(f"TODO: Generate result when slider changes {float(value)}")
        """
        - Get transformation
        - Gather Checkboxes to see which axis use to apply
        - Get value of the slider
        - Apply transformation
        """
        transform = self.optionsCMB.currentText()
        boolValues = [self.xAxisCB.isChecked(), self.yAxisCB.isChecked(), self.zAxisCB.isChecked()]
        minVal = self.transformSLD.getMinValue()
        print(minVal)


        """
        # GET VALUES
        multiplyValue = mc.floatField(multiplyValueKey, q=True, v=True)
        boolValues = [mc.checkBox(key, q=True, v=True) for key in boolKeys]
        minVal = mc.floatField(minValKey, q=True, v=True)

        if selObjRandom:
            selectedObjects = mc.ls(selection=True)
            selectedObjects = util.select.filterFlattenSelection(selectedObjects)
            if selectedObjects:
                for obj in selectedObjects:
                    if obj in selObjRandom:
                        initialPosition = selObjRandom[obj][transformationType]
                        if initialPosition:
                            if newValue != minVal:
                                newPosition = util.random.getPosition(multiplyValue, [minVal, newValue], *boolValues)
                                resultingPosition = [initialPosition[0] + newPosition[0], initialPosition[1] + newPosition[1], initialPosition[2] + newPosition[2]]
                                mc.xform(obj, **{transformationType: resultingPosition})
                            else:
                                mc.xform(obj, **{transformationType: initialPosition})
                    else:
                        mc.confirmDialog(title='Error', message=obj + " can't be found in the selection. Please create a New Selection", button=['OK'], defaultButton='OK')
                        break
        else:
            mc.confirmDialog(title='Error', message='Please create a New Selection', button=['OK'], defaultButton='OK')
        """

    def randomSelection(self, value):
        print(f"TODO: Randomize  selection {float(value)}")
        """
        newValue = mc.floatSliderGrp('selSlider', query=True, value=True)
        originalSelection = list(selObjRandom.keys())

        mc.select(originalSelection)
        currentSelection = mc.ls(selection=True)
        currentSelection = util.select.filterFlattenSelection(currentSelection)

        numSelect = int(newValue * len(originalSelection))
        # Randomly select a subset
        selectedSubset = util.random.getSample(originalSelection, numSelect)
        
        mc.select(selectedSubset)
        """