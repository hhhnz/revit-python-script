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
selection = __revit__.ActiveUIDocument.Selection.Elements
#methods

def printFilledRegionType():
	frtInstancesFilter = ElementClassFilter(clr.GetClrType(FilledRegionType))
	collector = FilteredElementCollector(doc)
	frtS = collector.WherePasses(frtInstancesFilter)
	for frt in frtS:
		print frt," ",frt.Id
def getComments(fr):
	for p in fr.Parameters:
		if p.Definition.Name == "Comments":
			return p.AsString()
	return None
def getAreaFR(fr):
	for p in fr.Parameters:
		if p.Definition.Name == "Area":
			words=p.AsValueString().split()
			return float(words[0])
	return double("0")
		
#define a transaction variable and describe the transaction
#t = Transaction(doc,'Select All Text')

#start a transaction in the Revit database
#t.Start()

#************ ADD YOUR OWN CODES HERE.******************
#get all filled regions
frInstancesFilter = ElementClassFilter(clr.GetClrType(FilledRegion))
collector = FilteredElementCollector(doc)
frS = collector.WherePasses(frInstancesFilter)
y=int(raw_input("group filled region area: 1.by comments 2.by Id 3. check TYPE Id: "))
if y==1:
	dic={}
	print "group filled region area by comments..."
	for fr in frS:
		paraS = fr.Parameters
		if int(fr.GetTypeId().ToString()) != -1:
			strId=getComments(fr)
			if strId in dic:
				dic[strId] += getAreaFR(fr)
				
			else:
				dic[strId] = getAreaFR(fr)
	print dic
	print "unit = square meters"
	
elif y==2:
	dic={}
	print "group filled region area by Id..."
	for fr in frS:
		paraS = fr.Parameters
		if int(fr.GetTypeId().ToString()) != -1:
			strId=fr.GetTypeId().ToString()
			if strId in dic:
				dic[strId] += getAreaFR(fr)
				
			else:
				dic[strId] = getAreaFR(fr)
	print dic
	print "unit = square meters"
				
			
elif y==3:
	sel = uidoc.Selection
	sel.Elements.Clear()
	pickedOne = sel.PickObject(ObjectType.Element,"pick an element to check TYPE Id")
	if pickedOne!= None :
		e = doc.GetElement(pickedOne.ElementId)
		l = []
		l.append("element typeId is: ")
		l.append(str(e.GetTypeId()))
		prompt = ''.join(l)
		TaskDialog.Show("typeId", prompt)
		



#print "end"
	

#commit the transaction to the Revit database
#t.Commit()

#close the script window
raw_input("Enter to Quit.....")
__window__.Close()
