from PySide2 import QtCore
from PySide2 import QtWidgets

class ktRangeSlider(QtWidgets.QWidget):
    # Define a custom signal to notify when the value changes
    valueChangedEvent = QtCore.Signal(float)

    def __init__(self, textWidth=60, sliderWidth=150, devValue=0, minValue=0, maxValue=10, showValueField=True, showMinMaxField=True, stepSize=1):
        super().__init__()

        """
        Variables definition
        """
        self.textWidth = textWidth
        self.sliderWidth = sliderWidth
        self.devValue = devValue
        self.minValue = minValue
        self.maxValue = maxValue
        self.showValueField = showValueField
        self.showMinMaxField = showMinMaxField
        self.stepSize = stepSize
        
        """
        UI Creation
        """
        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        # Scaling factor to allow fractional precision (unmodified pre=2)
        self.scaleFactor = 100 
        
        # Scale values to integers
        self.minValueScaled = int(self.minValue * self.scaleFactor)
        self.maxValueScaled = int(self.maxValue * self.scaleFactor)
        self.stepSizeScaled = int(self.stepSize * self.scaleFactor)
        self.devValueScaled = int(self.devValue * self.scaleFactor)

        
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(self.minValueScaled, self.maxValueScaled)
        self.slider.setValue(self.devValueScaled)
        self.slider.setFixedWidth(self.sliderWidth)
        self.slider.setTickInterval(self.stepSizeScaled)
        self.slider.setSingleStep(self.stepSizeScaled)

        # Create QDoubleSpinBox for min and max
        self.minField = QtWidgets.QDoubleSpinBox()
        self.minField.setFixedWidth(self.textWidth)
        self.minField.setValue(self.minValue)
        self.minField.setSingleStep(self.stepSize)

        self.maxField = QtWidgets.QDoubleSpinBox()
        self.maxField.setFixedWidth(self.textWidth)
        self.maxField.setValue(self.maxValue)
        self.maxField.setSingleStep(self.stepSize)

        # Create QDoubleSpinBox for the slider's value
        self.valueField = QtWidgets.QDoubleSpinBox()
        self.valueField.setRange(self.minValue, self.maxValue)
        self.valueField.setFixedWidth(self.textWidth)
        self.valueField.setSingleStep(self.stepSize)
        self.valueField.setValue(self.slider.value() / self.scaleFactor)
        

    def createLayouts(self):
        mainLayout = QtWidgets.QHBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)

        if self.showValueField:
            mainLayout.addWidget(self.valueField)
        
        mainLayout.addWidget(self.slider)

        if self.showMinMaxField:
            mainLayout.addWidget(self.minField)
            mainLayout.addWidget(self.maxField)

    def createConnections(self):
        """When values change update the widgets with the functions innit"""
        self.slider.valueChanged.connect(self.onSliderValueChanged)
        self.minField.valueChanged.connect(self.setMinSlider)
        self.maxField.valueChanged.connect(self.setMaxSlider)
        self.valueField.valueChanged.connect(self.setSliderValue)
    
    def onSliderValueChanged(self):
        """This function will be called whenever the slider value changes, and will 
            emit a custom signal when the slider value changes"""
        self.valueField.setValue(self.slider.value() / self.scaleFactor)
        self.valueChangedEvent.emit(self.valueField.value())
        #print(f"Slider value changed: {value}")

    def setMinSlider(self):
        """Update the slider's minimum value based on the input."""
        self.minValueScaled = int(self.minField.value() * self.scaleFactor)

        """If the min value is smaller than max then update it, otherwise revert it"""
        if self.minValueScaled < self.maxValueScaled:
            self.slider.setMinimum(self.minValueScaled)
            self.valueField.setMinimum(self.minValueScaled)
        else:
            self.minField.setValue(self.slider.minimum() / self.scaleFactor)

    def setMaxSlider(self):
        """Update the slider's maximum value based on the input."""
        self.maxValueScaled = int(self.maxField.value() * self.scaleFactor)

        """If the max value is bigger than min then update it, otherwise revert it"""
        if self.maxValueScaled > self.minValueScaled:
            self.slider.setMaximum(self.maxValueScaled)
            self.valueField.setMaximum(self.maxValueScaled)
        else:
            self.maxField.setValue(self.slider.maximum() / self.scaleFactor)

    def setSliderValue(self):
        """Update the slider's value when the spinbox value changes."""
        self.slider.setValue(int(self.valueField.value() * self.scaleFactor))
    
    def getValue(self):
        return self.slider.value() / self.scaleFactor