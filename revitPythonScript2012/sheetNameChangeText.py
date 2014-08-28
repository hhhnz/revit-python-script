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
#selection = list(__revit__.ActiveUIDocument.Selection.Elements)
uidoc = __revit__.ActiveUIDocument
selection = __revit__.ActiveUIDocument.Selection.Elements

#main program
#define a transaction variable and describe the transaction
t = Transaction(doc,'Change Sheet Name Text')

#start a transaction in the Revit database
t.Start()

x = int(raw_input("all Sheet Name 1. upper case 2. title: "))

sheetInstancesFilter = ElementClassFilter(clr.GetClrType(ViewSheet))
collector = FilteredElementCollector(doc)
sheetsId = collector.WherePasses(sheetInstancesFilter).ToElementIds()
for id in sheetsId:
	s = doc.get_Element(id)
	oldName = s.Name
	if x == 2:
		newname = oldName.title()
		print newname
		s.ViewName = newname
	elif x == 1:
		newname = oldName.upper()
		print newname
		s.ViewName = newname
	
	
#************** END OF YOUR MAJOR CODES HERE.*********************
#commit the transaction to the Revit database
t.Commit()

#close the script window
__window__.Close()
