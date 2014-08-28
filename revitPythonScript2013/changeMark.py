# IronPython Pad. Write code snippets here and F5 to run.
import clr
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
#selection = list(__revit__.ActiveUIDocument.Selection.Elements)
uidoc = __revit__.ActiveUIDocument
#selection = __revit__.ActiveUIDocument.Selection.Elements
selelementsid=[]
#############################method###################################
def getAsStrParaByName(id,s):
	for p in doc.get_Element(id).Parameters:
		if p.Definition.Name == s:
			return p.AsString()
	return None
def setParaByName(id,name,s):
	doc.get_Element(id).get_Parameter(BuiltInParameter.ALL_MODEL_MARK ).Set( s )
			



#define a transaction variable and describe the transaction
t = Transaction(doc,'Change Element Mark')

#start a transaction in the Revit database
t.Start()

#************ ADD YOUR OWN CODES HERE.******************
sel = uidoc.Selection
sel.Elements.Clear()
pickedOne = sel.PickObject(ObjectType.Element,"Pick one Element")
if pickedOne!= None :
	currentMark = getAsStrParaByName(pickedOne.ElementId,"Mark")
	if currentMark != None :
		print "Current Mark Value: ",currentMark
		__window__.BringToFront()
		x = raw_input ("New Mark Value: ")
		setParaByName(pickedOne.ElementId,"Mark",x)
		newMark = getAsStrParaByName(pickedOne.ElementId,"Mark")
		print "NEW Mark Value: ",newMark
	else:
		print "no Mark for this element!!!"
z = raw_input ("finished... any Enter to quit ")

#************** END OF YOUR MAJOR CODES HERE.*********************
#commit the transaction to the Revit database
t.Commit()

#close the script window
__window__.Close()
