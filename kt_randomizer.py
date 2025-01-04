import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import importlib
import random

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
        self.optionsCMB.addItem('translation')
        self.optionsCMB.addItem('rotation')
        self.optionsCMB.addItem('scale')
        self.xAxisCB = QtWidgets.QCheckBox()
        self.xAxisCB.setChecked(True)
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
        #print(self.objData)

    
    def generateResult(self, value):

        def randomValues(range, xBool, yBool, zBool):
            newValues = [0.0, 0.0, 0.0]

            if xBool:
                newValues[0] = random.uniform(range[0], range[1])
            if yBool:
                newValues[1] = random.uniform(range[0], range[1])
            if zBool:
                newValues[2] = random.uniform(range[0], range[1])

            return newValues
        """
        - Get transformation
        - Gather Checkboxes to see which axis to apply
        - Get value of the slider
        - Apply transformation
        """
        transform = self.optionsCMB.currentText()
        boolValues = [self.xAxisCB.isChecked(), self.yAxisCB.isChecked(), self.zAxisCB.isChecked()]
        minVal = self.transformSLD.getMinValue()
        maxVal = float(value)

        if self.objData:
            selectedObjects = mc.ls(selection=True)
            if selectedObjects:
                for obj in selectedObjects:
                    if obj in self.objData:
                        initialPosition = self.objData[obj][transform]
                        newPosition = randomValues([minVal, maxVal], *boolValues)
                        resultingPosition = [initialPosition[0] + newPosition[0], 
                                             initialPosition[1] + newPosition[1], 
                                             initialPosition[2] + newPosition[2]]
                        mc.xform(obj, **{transform: resultingPosition})
                    else:
                        om.MGlobal.displayWarning(f"The {obj} wasn't found in the selection. Skipping")

    def generateNewResult(self):
        self.generateResult(self.transformSLD.getValue())

    def randomSelection(self, value):
        originalSelection = list(self.objData.keys())
        numSelect = int(float(value) * len(originalSelection))

        # Randomly select a subset
        selectedSubset = random.sample(originalSelection, numSelect)
        
        mc.select(selectedSubset)

    
    def retouchResult(self):
         #Check if two objects Bounding Box intercept
        def checkIntersectionBBox(mesh1, mesh2):

            bbox1 = mc.exactWorldBoundingBox(mesh1)
            bbox2 = mc.exactWorldBoundingBox(mesh2)

            xmin1, ymin1, zmin1, xmax1, ymax1, zmax1 = bbox1
            xmin2, ymin2, zmin2, xmax2, ymax2, zmax2 = bbox2
            
            # Check for intersection
            if (xmin1 <= xmax2 and xmax1 >= xmin2 and
                ymin1 <= ymax2 and ymax1 >= ymin2 and
                zmin1 <= zmax2 and zmax1 >= zmin2):
                return True
            else:
                return False

        def checkTouchingObjList(selectedObjects):
            touched = set()  # Keeps track of objects that have already been checked
            finalObjects = []

            for i in range(len(selectedObjects)):
                obj1 = selectedObjects[i]
                for j in range(i + 1, len(selectedObjects)):
                    obj2 = selectedObjects[j]
                    if obj2 in touched:
                        break
                    if checkIntersectionBBox(obj1, obj2):
                        finalObjects.append((obj2))
                        touched.add(obj2)
                        break  # Move to the next object after finding a touching pair
            return finalObjects
        

        selectedObjects = list(self.objData.keys())
        touchingObjects = []
        
        max_iterations = 100
        iteration_count = 0

        #Will break when all objects are in the same position
        while iteration_count < max_iterations:
            touchingObjects = checkTouchingObjList(selectedObjects)
            if touchingObjects:
                mc.select(touchingObjects)
                self.generateNewResult()
                iteration_count += 1
            else:
                break

        if iteration_count >= max_iterations:
            mc.warning("Max iterations reached. Objects may still be touching.")
        
        mc.select(selectedObjects)
    
    def clearSelection(self):
        print("TODO: Clear selection")

        """
        - Clear selection
        - Reset selection Slider
        - Reset transform range
        - Clear checkboxes?
        """


