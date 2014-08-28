# IronPython Pad. Write code snippets here and F5 to run.
# IronPython Pad. Write code snippets here and F5 to run.
import clr
import math
import time
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI.Selection import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
sel = uidoc.Selection
ele = sel.Elements
#selection = list(__revit__.ActiveUIDocument.Selection.Elements)
uidoc = __revit__.ActiveUIDocument
selection = __revit__.ActiveUIDocument.Selection.Elements

# method
def addArrow(y,id):
	t = Transaction(doc,'Add Arrow to Text')
	#start a transaction in the Revit database
	t.Start()
	if y==1:
		doc.get_Element(id).AddLeader(TextNoteLeaderTypes.TNLT_STRAIGHT_L)
		print "add left"
	elif y==2:
		doc.get_Element(id).AddLeader(TextNoteLeaderTypes.TNLT_STRAIGHT_R)
		print "add right"
	elif y==3:
		doc.get_Element(id).RemoveLeaders()
#commit the transaction to the Revit database
	t.Commit()

#************ ADD YOUR OWN CODES HERE.******************

if uidoc.Selection.Elements.IsEmpty:
	print ("selesct texts first")
else:
	y=int(raw_input("Arrow direction: 1.left 2.right 3.remove arrow: "))
	
	listElementIds=[]
	for e in ele:
		if e.Category is not None:
			if e.Category.Name == "Text Notes":
				listElementIds.append(e.Id)
	
	for id in listElementIds:
		addArrow(y,id)

	

time.sleep(1)

#close the script window
__window__.Close()
