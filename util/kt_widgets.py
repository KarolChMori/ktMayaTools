from PySide2 import QtCore
from PySide2 import QtWidgets

class ktRangeSlider(QtWidgets.QWidget):
    def __init__(self, textWidth=60, sliderWidth=150, minValue=0, maxValue=10, showValueField=True, showMinMaxField=True, stepSize=1):
        super().__init__()

        self.textWidth = textWidth
        self.sliderWidth = sliderWidth
        self.minValue = minValue
        self.maxValue = maxValue
        self.showValueField = showValueField
        self.showMinMaxField = showMinMaxField
        self.stepSize = stepSize
        

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        # Scaling factor to allow fractional precision
        self.scaleFactor = 100 
        
        # Scale values to integers
        self.minValueScaled = int(self.minValue * self.scaleFactor)
        self.maxValueScaled = int(self.maxValue * self.scaleFactor)
        self.stepSizeScaled = int(self.stepSize * self.scaleFactor)

        
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setFixedWidth(self.sliderWidth)
        self.slider.setMinimum(self.minValueScaled)
        self.slider.setMaximum(self.maxValueScaled)
        self.slider.setTickInterval(self.stepSizeScaled)
        self.slider.setSingleStep(self.stepSizeScaled)

        # Create QDoubleSpinBox for min and max
        self.minInputTXT = QtWidgets.QDoubleSpinBox()
        self.minInputTXT.setFixedWidth(self.textWidth)
        self.minInputTXT.setValue(self.minValue)
        self.minInputTXT.setSingleStep(self.stepSize)

        self.maxInputTXT = QtWidgets.QDoubleSpinBox()
        self.maxInputTXT.setFixedWidth(self.textWidth)
        self.maxInputTXT.setValue(self.maxValue)
        self.maxInputTXT.setSingleStep(self.stepSize)

        # Create QDoubleSpinBox for the slider's value
        self.valueField = QtWidgets.QDoubleSpinBox()
        self.valueField.setRange(self.minValue, self.maxValue)
        self.valueField.setFixedWidth(self.textWidth)
        self.valueField.setSingleStep(self.stepSize)
        self.valueField.setValue(self.slider.value())
        

    def createLayouts(self):
        mainLayout = QtWidgets.QHBoxLayout(self)

        if self.showValueField:
            mainLayout.addWidget(self.valueField)
        
        mainLayout.addWidget(self.slider)

        if self.showMinMaxField:
            mainLayout.addWidget(self.minInputTXT)
            mainLayout.addWidget(self.maxInputTXT)

    def createConnections(self):
        # Connect input fields to update slider range
        self.minInputTXT.valueChanged.connect(self.updateMin)
        self.maxInputTXT.valueChanged.connect(self.updateMax)

        # Connect the slider's value change to update the updateValueField
        self.slider.valueChanged.connect(self.updateValueField)

        # Connect the valueField to update the slider
        self.valueField.valueChanged.connect(self.updateSliderValue)

    def updateMin(self):
        """Update the slider's minimum value based on the input."""
        minValue = self.minInputTXT.value()
        # Only update if the minValue is less than the maxValue
        if minValue < self.maxInputTXT.value():
            self.slider.setMinimum(minValue)
        else:
            self.minInputTXT.setValue(self.slider.minimum())  # Revert to valid value

    def updateMax(self):
        """Update the slider's maximum value based on the input."""
        maxValue = self.maxInputTXT.value()
        # Only update if the maxValue is greater than the minValue
        if maxValue > self.minInputTXT.value():
            self.slider.setMaximum(maxValue)
        else:
            self.maxInputTXT.setValue(self.slider.maximum())  # Revert to valid value
    
    def updateValueField(self):
        """Update the value of the spinbox when the slider moves."""
        self.valueField.setValue(self.slider.value())

    def updateSliderValue(self):
        """Update the slider's value when the spinbox value changes."""
        self.slider.setValue(self.valueField.value() )
    
    def getValue(self):
        return self.slider.value()