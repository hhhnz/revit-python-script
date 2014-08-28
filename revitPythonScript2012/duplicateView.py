import clr
import math
import time
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
#METHODS
def nameNumberIncrement(oldName):
	words=oldName.split()
	lastIndex = words.__len__()-1
	try:
		oldNumber = int(words[lastIndex])
		newNumber = oldNumber+1
		words[lastIndex]=str(newNumber)
		newName = ' '.join(words)
		return newName
	except ValueError:
		l=[]
		l.append(oldName)
		l.append(str(1))
		newName = ' '.join(l)
		return newName
	
def existViewName(vname):
	vInstancesFilter = ElementClassFilter(clr.GetClrType(View))
	collector = FilteredElementCollector(doc)
	vs = collector.WherePasses(vInstancesFilter)
	for ele in vs:
		if ele.Name == vname:
			return True
	return False
def getNewName(oldName,i):
	words=oldName.split()
	lastIndex = words.__len__()-1
	try:
		oldNumber = int(words[lastIndex])
		newNumber = oldNumber+i
		words[lastIndex]=str(newNumber)
		newName = ' '.join(words)
		while existViewName(newName):
			newName=nameNumberIncrement(newName)
		
		return newName
	except ValueError:
		l=[]
		l.append(oldName)
		l.append(str(i))
		newName = ' '.join(l)
		while existViewName(newName):
			newName=nameNumberIncrement(newName)
		return newName
	
#define a transaction variable and describe the transaction
#**************CHANGE TRANSACTION NAME BY USER*********************
t = Transaction(doc,'Duplicate View')

#start a transaction in the Revit database
t.Start()

#************ ADD YOUR OWN CODES HERE.******************
stry=raw_input("duplication type: 1.Duplicate view 2.as Dependent 3.with Detailing: ")
y=int(stry)
x=raw_input("how many copies: ")
oldName = doc.ActiveView.ViewName
try:
	for i in range(1,int(x)+1):
		if y==1:
			newView=doc.ActiveView.Duplicate(ViewDuplicateOption.Duplicate)
			#TRY RENAME VIEW METHOD
			doc.GetElement(newView).ViewName=getNewName(oldName,i)
		elif y==2:
			newView=doc.ActiveView.Duplicate(ViewDuplicateOption.AsDependent)
			doc.GetElement(newView).ViewName=getNewName(oldName,i)
		elif y==3:   
			newView=doc.ActiveView.Duplicate(ViewDuplicateOption.WithDetailing)
			doc.GetElement(newView).ViewName=getNewName(oldName,i)
		else:
			print ("wrong type, nothing to do")
except Exception as err:
	print err
time.sleep(1)
print("finished")



#*************** FINISH YOUR CODES HERE



#commit the transaction to the Revit database
t.Commit()

#close the script window
#__window__.Close()
