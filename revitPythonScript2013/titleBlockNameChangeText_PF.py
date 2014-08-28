import clr
import math
import time
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI.Selection import *

#variables
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
selection = __revit__.ActiveUIDocument.Selection.Elements
#the name of project paras that hold title block sheet name information
var1 = "SHEET_TITLE LINE 1_WF"
var2 = "SHEET_TITLE LINE 2_WF"
var3 = "SHEET_TITLE LINE 3_WF"
#methods
def getNewString(old,x):
	if x == 2:
		new = old.title()
		print new
		return new
	elif x == 1:
		new = old.upper()
		print new
		return new
	
#main program
#define a transaction variable and describe the transaction

t = Transaction(doc,'Change Title Block Text')

#start a transaction in the Revit database
t.Start()

x = int(raw_input("all Title Block Name 1. upper case 2. title: "))

sheetInstancesFilter = ElementClassFilter(clr.GetClrType(ViewSheet))
collector = FilteredElementCollector(doc)
sheetsId = collector.WherePasses(sheetInstancesFilter).ToElementIds()
for id in sheetsId:
	s = doc.get_Element(id)
	parS = s.Parameters
	for p in parS:
		if p.Definition.Name == var1 or p.Definition.Name == var2 or p.Definition.Name == var3 :
			if p.AsString() != None:
				oldString = str(p.AsString())
				newString = getNewString(oldString,x)
				p.Set(newString)
	
#************** END OF YOUR MAJOR CODES HERE.*********************
#commit the transaction to the Revit database
t.Commit()

#close the script window
__window__.Close()
