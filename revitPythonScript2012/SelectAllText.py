# IronPython Pad. Write code snippets here and F5 to run.
import clr
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
#selection = list(__revit__.ActiveUIDocument.Selection.Elements)
uidoc = __revit__.ActiveUIDocument
selection = __revit__.ActiveUIDocument.Selection.Elements

#define a transaction variable and describe the transaction
t = Transaction(doc,'Select All Text')

#start a transaction in the Revit database
t.Start()

#************ ADD YOUR OWN CODES HERE.******************

#Rmfilter = RoomFilter();
txtInstancesFilter = ElementClassFilter(clr.GetClrType(TextElement))
#print "after elementclassFilter"
collector = FilteredElementCollector(doc)
textsId = collector.WherePasses(txtInstancesFilter).ToElementIds()
x=int(raw_input("1.selection all text, 2.all text case Title, 3.all text UPPER case: "))
if x == 1:
	selection.Clear()
	for id in textsId:
		selection.Add(doc.get_Element(id))
		print str(id)
elif x == 2: #title
	for id in textsId:
		s = doc.get_Element(id).Text
		newName = s.title()
		doc.get_Element(id).Text = newName
		
elif x == 3: #upper case
	for id in textsId:
		s = doc.get_Element(id).Text
		newName = s.upper()
		doc.get_Element(id).Text = newName
#commit the transaction to the Revit database
t.Commit()

#close the script window
__window__.Close()
