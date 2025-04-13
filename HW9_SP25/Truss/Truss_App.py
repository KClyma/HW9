"""
Homework 9 – Truss Design GUI Application

Problem Statement:
I have written a program with a GUI for reading a file and drawing a truss as illustrated below.

a. While the program is mostly in the MVC pattern, there are still some function calls in the App that are of form
   self.controller.view.function(). Correct these so that all function calls are directly to the controller.

b. Add some extra information to each link in the text file and read it in to a modified link class that includes
   width and thickness of the link and the material of construction (your choice if it is steel or aluminum).
   You see in the figure below, a tool tip for link 3 that appears when the mouse hovers over that link.
   Augment this information to include the weight of the link in appropriate units.

c. There are pin joints for both supports of this truss, but this over constrains the system.
   Replace the pin joint at the right node with a roller. Also, compute the vertical load at the right and
   left nodes due to the weight of the truss and display it in the tooltip for the node.
"""
"Used ChatGPT to help work through steps A, B, and C. It helped fix errors i had as well as problem solve part C"


#region imports
from Truss_GUI import Ui_TrussStructuralDesign
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from Truss_Classes import TrussController
import sys
#endregion


#region class definitions
class MainWindow(Ui_TrussStructuralDesign,qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_Open.clicked.connect(self.OpenFile)
        self.spnd_Zoom.valueChanged.connect(self.setZoom) #$NEW$ double spinner widget for setting zoom level

        self.controller=TrussController()
        self.controller.setDisplayWidgets((self.te_DesignReport, self.le_LinkName, self.le_Node1Name,
                                           self.le_Node2Name, self.le_LinkLength, self.gv_Main))

        self.controller.installEventFilter(self)   #This calls the function from the view directly. Fix so that it only calls the controller directly.
        self.gv_Main.setMouseTracking(True)

        self.show()

    def setZoom(self):
        self.gv_Main.resetTransform()
        self.gv_Main.scale(self.spnd_Zoom.value(), self.spnd_Zoom.value())

    def eventFilter(self, obj, event):
        """
        This overrides the default eventFilter of the widget.  It takes action on events and then passes the event
        along to the parent widget.
        :param obj: The object on which the event happened
        :param event: The event itself
        :return: boolean from the parent widget
        """
        #There are several places where functions in view are called directly. Fix these so that the only
        # function calls are from the controller.
        if obj == self.controller.getScene():
            et = event.type()
            if et == qtc.QEvent.GraphicsSceneMouseMove:
                scenePos = event.scenePos()
                strScene = "Mouse Position:  x = {}, y = {}".format(round(scenePos.x(), 2), round(-scenePos.y(), 2))
                s = self.controller.getItemAt(scenePos, self.gv_Main.transform())  # gets item from graphics scene under the mouse
                if s is not None and s.data(0) is not None:  # when creating nodes and pipes, I used the setData() function to store a name
                    strScene += ' (' + s.data(0) + ')'
                items = self.controller.getItemsAt(scenePos)

                item_names = [item.name if hasattr(item, 'name') else None for item in items]
                for i in item_names:
                    strScene += ', '+(i if i is not None else 'none')
                self.lbl_MousePos.setText(strScene)  # display information in a label
            if event.type() == qtc.QEvent.GraphicsSceneWheel:  # I added this to zoom on mouse wheel scroll
                if event.delta() > 0:
                    self.spnd_Zoom.stepUp()
                else:
                    self.spnd_Zoom.stepDown()
                pass
            if event.type() == qtc.QEvent.ToolTip:
                pass

        # pass the event along to the parent widget if there is one.
        return super(MainWindow, self).eventFilter(obj, event)

    def OpenFile(self):
        filename = qtw.QFileDialog.getOpenFileName()[0]
        if len(filename) == 0:  # no file selected
            return
        self.te_Path.setText(filename)
        file = open(filename, 'r')  # open the file
        data = file.readlines()  # read all the lines of the file into a list of strings
        self.controller.ImportFromFile(data)  # import the pipe network information
#endregion

#region function definitions
def Main():
    app=qtw.QApplication(sys.argv)
    mw=MainWindow()
    sys.exit(app.exec())
#endregion

#region function calls
if __name__=="__main__":
    Main()
#endregion