from PySide2 import QtCore
from PySide2 import QtWidgets

class ktRangeSlider(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.createWidgets()
        self.createLayouts()
        self.createConnections()

    def createWidgets(self):
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)  # Default minimum value
        self.slider.setMaximum(100)  # Default maximum value
        self.minInputTXT = QtWidgets.QLineEdit()
        self.maxInputTXT = QtWidgets.QLineEdit()

    def createLayouts(self):
        mainLayout = QtWidgets.QHBoxLayout(self)
        mainLayout.addWidget(self.slider)
        mainLayout.addWidget(self.minInputTXT)
        mainLayout.addWidget(self.maxInputTXT)

    def createConnections(self):
        # Connect input fields to update slider range
        self.minInputTXT.editingFinished.connect(self.updateMin)
        self.maxInputTXT.editingFinished.connect(self.updateMax)

    def updateMin(self):
        """Update the slider's minimum value based on the input."""
        try:
            minValue = int(self.minInputTXT.text())
            if minValue < self.slider.maximum():
                self.slider.setMinimum(minValue)
            else:
                self.minInputTXT.setText(str(self.slider.minimum()))  # Revert to valid value
        except ValueError:
            self.minInputTXT.setText(str(self.slider.minimum()))  # Revert to valid value

    def updateMax(self):
        """Update the slider's maximum value based on the input."""
        try:
            maxValue = int(self.maxInputTXT.text())
            if maxValue > self.slider.minimum():
                self.slider.setMaximum(maxValue)
            else:
                self.maxInputTXT.setText(str(self.slider.maximum()))  # Revert to valid value
        except ValueError:
            self.maxInputTXT.setText(str(self.slider.maximum()))  # Revert to valid value
    
    def getValue(self):
        return self.slider.value()