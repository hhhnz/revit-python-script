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
#get views in a list
def viewSelectInList():
	sel = uidoc.Selection
	sel.Elements.Clear()
	loopSwitch = 1
	while loopSwitch==1:

		pickedOne = sel.PickObject(ObjectType.Element,"Pick view one by one, pick title block to finish")
		if pickedOne!= None :
			e = doc.GetElement(pickedOne.ElementId)
#			TaskDialog.Show("Revit", e.Category.Name)
			if e.Category.Name.Equals("Title Blocks"):
#				TaskDialog.Show("Revit", e.Category.Name)
				loopSwitch = 0
			else:
				selelementsid.append(e.Id)
#				TaskDialog.Show("Revit", e.Category.Name)
		else:
			break
def reNumber (startInt):
	currentNo = startInt
	for eId in selelementsid:
		setViewPortNumber(eId,currentNo)
		currentNo += 1
def getViewByDetailNumber (vs,i):
	for v in vs.Views:
		if v.get_Parameter(BuiltInParameter.VIEWPORT_DETAIL_NUMBER).AsString() != None:
			if i == int(v.get_Parameter(BuiltInParameter.VIEWPORT_DETAIL_NUMBER).AsString()):
				return v
		
def setViewPortNumber (id, number):
	vs = doc.ActiveView
	stringOldNumber=doc.get_Element(id).get_Parameter(BuiltInParameter.VIEWPORT_DETAIL_NUMBER).AsString()
#	print "viewport detail number: ",stringOldNumber
	if int(stringOldNumber) != number:
		if getViewByDetailNumber(vs, number) != None:
			#*****************to be finished here *****************
			getViewByDetailNumber(vs, number).get_Parameter(BuiltInParameter.VIEWPORT_DETAIL_NUMBER).Set("999")
			doc.get_Element(id).get_Parameter(BuiltInParameter.VIEWPORT_DETAIL_NUMBER).Set(str(number))
			getViewByDetailNumber(vs, 999).get_Parameter(BuiltInParameter.VIEWPORT_DETAIL_NUMBER).Set(stringOldNumber)
		else:
			doc.get_Element(id).get_Parameter(BuiltInParameter.VIEWPORT_DETAIL_NUMBER).Set(str(number))
#define a transaction variable and describe the transaction
t = Transaction(doc,'Sort Views in Sheet')

#start a transaction in the Revit database
t.Start()

#************ ADD YOUR OWN CODES HERE.******************
x = int(raw_input ("number start from: "))
viewSelectInList()
reNumber ( x )


#print "finished"
	
#************** END OF YOUR MAJOR CODES HERE.*********************
#commit the transaction to the Revit database
t.Commit()

#close the script window
__window__.Close()
