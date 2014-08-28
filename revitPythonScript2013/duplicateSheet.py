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
#method
def insert(original, new, pos):
	return original[:pos] + new + original[pos:]
def numberExists(i):
	sheetInstancesFilter = ElementClassFilter(clr.GetClrType(ViewSheet))
	collector = FilteredElementCollector(doc)
	sheetsId = collector.WherePasses(sheetInstancesFilter).ToElementIds()
	for id in sheetsId:
		s = doc.get_Element(id)
		if i == clearDot(s.SheetNumber):
			return True
	
	return False
		
	
def clearDot(s):
	s = s.translate(None, '.!@#$')
	i = int(s)
	return i
def getNextNumber(s):
	oldNumber = clearDot(s)
	newNumber = oldNumber + 1
	while numberExists(newNumber):
		newNumber += 1
	#add dot 
	newString=insert(str(newNumber),'.',2)
	return newString
def getFirstFamilySym(fSymSet):
	for f in fSymSet:
		return f
def getParaByName(paraSet,s):
	for p in paraSet:
		if p.Definition.Name == s:
			return p
	return None
#main program

#define a transaction variable and describe the transaction

t = Transaction(doc,'Duplicate Current Sheet')

#start a transaction in the Revit database
t.Start()
#************ ADD YOUR OWN CODES HERE.******************
x = int(raw_input("How many copies: "))
originSheet = doc.ActiveView
tbS = doc.TitleBlocks
tb = getFirstFamilySym(tbS)

for _ in range(0,x):
	newSheet=ViewSheet.Create(doc,tb.Id)
	#tranport origin sheet parameters to new one
	parS = originSheet.Parameters
	for oldP in parS:
		paraName = oldP.Definition.Name
		#print paraName
		if paraName == "Sheet Number": #unique sheet number
			newSheetNumber = getNextNumber(getParaByName(originSheet.Parameters,paraName).AsString())
			getParaByName(newSheet.Parameters,paraName).Set(newSheetNumber)
		else:
			if oldP.AsString() != None and getParaByName(newSheet.Parameters,paraName).IsReadOnly == False:
				getParaByName(newSheet.Parameters,paraName).Set(oldP.AsString())
	
#************** END OF YOUR MAJOR CODES HERE.*********************
#commit the transaction to the Revit database
t.Commit()

#close the script window
#__window__.Close()
