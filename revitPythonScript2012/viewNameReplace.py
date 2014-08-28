# IronPython Pad. Write code snippets here and F5 to run.
import clr
import math
import time
import System

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')
clr.AddReference('System.Data')
#clr.AddReference('System.Text')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import View as rView
from Autodesk.Revit.DB.Architecture import *
from Autodesk.Revit.DB.Analysis import *
from Autodesk.Revit.UI.Selection import *
from Autodesk.Revit.UI import TaskDialog
from System.Drawing import *
from System.Windows.Forms import *
from System.Text import StringBuilder

#variables
outPuts = []
uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
sel = uidoc.Selection
ele = sel.Elements
totalView=0
#selection = list(__revit__.ActiveUIDocument.Selection.Elements)
uidoc = __revit__.ActiveUIDocument
selection = __revit__.ActiveUIDocument.Selection.Elements
#methods
def getAsStrParaByName(id,s):
	for p in doc.get_Element(id).Parameters:
		if p.Definition.Name == s:
			return p.AsString()
	return None
def setParaByName(id,name,s):
	for p in doc.get_Element(id).Parameters:
		if p.Definition.Name == name:
			p.Set(s)
			
#CLASSES
class CheckBoxExampleForm(Form):
	#class variables
	#allViewsId = FilteredElementCollector(doc)
	def __init__(self):
		self.Text = "View Name Update"
		self.Width = 460
		self.Height = 600
		#self.dgrid=DataGridView()
		self.setupPanel()
		self.setupDataGridView()
		self.populateDataGridView()
	
	def setupPanel(self):
		self._panel1 = Panel()
		self._btnSelectAll = Button()
		self._btnSelectNone = Button()
		self._btnReplace = Button()
		self._btnTitle = Button()
		self._btnUpperCase = Button()
		self._btnCancel = Button()
		self._btnWriteExcel = Button()
		self._btnReadExcel = Button()
		self._tbxFind = TextBox()
		self._tbxReplace = TextBox()
		self._ckbTrueName = CheckBox()
		self._ckbNameOnSheet = CheckBox()
		
		
		
		self._panel1.Controls.Add(self._btnSelectAll)
		self._panel1.Controls.Add(self._btnSelectNone)
		self._panel1.Controls.Add(self._btnReplace)
		self._panel1.Controls.Add(self._btnTitle)
		self._panel1.Controls.Add(self._btnUpperCase)
		self._panel1.Controls.Add(self._btnCancel)
		self._panel1.Controls.Add(self._btnWriteExcel)
		self._panel1.Controls.Add(self._btnReadExcel)
		self._panel1.Controls.Add(self._tbxFind)
		self._panel1.Controls.Add(self._tbxReplace)
		self._panel1.Controls.Add(self._ckbTrueName)
		self._panel1.Controls.Add(self._ckbNameOnSheet)
		self._panel1.Dock = DockStyle.Top
		self._panel1.Location = Point(0, 0)
		
		self._btnSelectAll.Location = Point(20,5)
		self._btnSelectAll.Text = 'Select All'
		self._btnSelectAll.Click += self.selectAllClicked
		
		self._btnSelectNone.Location = Point(110,5)
		self._btnSelectNone.Text = 'Select None'
		self._btnSelectNone.Click += self.selectNoneClicked
		
		self._btnReplace.Location = Point(20,63)
		self._btnReplace.Text = 'Replace Text'
		self._btnReplace.Click += self.btnReplaceClicked
		self._btnReplace.Size = Size(100, 24)
		
		self._btnTitle.Location = Point(20,34)
		self._btnTitle.Text = 'Text Case to Title'
		self._btnTitle.Click += self.btnTitleClicked
		self._btnTitle.Size = Size(120, 24)
		
		self._btnUpperCase.Location = Point(150,34)
		self._btnUpperCase.Text = 'Text Case to UpperCase'
		self._btnUpperCase.Click += self.btnUpperClicked
		self._btnUpperCase.Size = Size(150, 24)
		
		self._btnCancel.Location = Point(250,121)
		self._btnCancel.Text = 'Cancel'
		self._btnCancel.Click += self.btnCancelClicked
		
		self._btnWriteExcel.Location = Point(350,2)
		self._btnWriteExcel.Text = 'Write Excel'
		self._btnWriteExcel.Click += self.btnWriteExcelClicked
		
		self._btnReadExcel.Location = Point(350,31)
		self._btnReadExcel.Text = 'Read Excel'
		self._btnReadExcel.Click += self.btnReadExcelClicked
		
		self._tbxFind.Location = Point(130,63)
		self._tbxFind.Text = 'Find'
		self._tbxFind.Size = Size(200, 24)
		
		self._tbxReplace.Location = Point(130,92)
		self._tbxReplace.Text = 'Replace'
		self._tbxReplace.Size = Size(200, 24)
		
		self._ckbTrueName.Text = "View Name"
		self._ckbTrueName.Location = Point(20,121)
		self._ckbTrueName.Checked = True
		self._ckbTrueName.Width=90
		
		self._ckbNameOnSheet.Text = "Name on Sheet"
		self._ckbNameOnSheet.Location = Point (130,121)
		self._ckbNameOnSheet.Size = Size(300,24)
		
		self._panel1.Size = Size(600,160)
		self.Controls.Add(self._panel1)
		
	def setupDataGridView(self):
		self._dataGridView1 = DataGridView()
		self._dataGridView1.AllowUserToOrderColumns = True
		self._dataGridView1.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
		self._dataGridView1.Dock = DockStyle.Bottom
		self._dataGridView1.Location = Point(0, 130)
		self._dataGridView1.Size = Size(600, 400)
		self._dataGridView1.TabIndex = 3
		self._dataGridView1.Name="view list"
		self._dataGridView1.RowHeadersVisible = True
		
		self._dataGridView1.SelectionMode = DataGridViewSelectionMode.FullRowSelect
		self._dataGridView1.MultiSelect = True
        
		#column setup
		self._dataGridView1.ColumnCount=4
		self._dataGridView1.Columns[0].Name="View Type"
		self._dataGridView1.Columns[1].Name="View Name"
		self._dataGridView1.Columns[2].Name="View ID"
		self._dataGridView1.Columns[3].Name="Title on Sheet"
		
		
		
		self.Controls.Add(self._dataGridView1)
	def updateSheetName(self,type):
		if self._ckbNameOnSheet.Checked:
			if type == 1: #replace
				print "sheet name replace"
				for row in self._dataGridView1.SelectedRows:
					id=ElementId(int(row.Cells[2].Value))
					v = doc.get_Element(id)			
					s = getAsStrParaByName(id,"Title on Sheet")
					newName = s.Replace(self._tbxFind.Text,self._tbxReplace.Text)
					setParaByName(id,"Title on Sheet",newName)
					outPuts.append (s+" -> changed to: "+newName+'\n')
			elif type == 2: #title
				print "sheet name title"
				for row in self._dataGridView1.SelectedRows:
					id=ElementId(int(row.Cells[2].Value))
					v = doc.get_Element(id)			
					s = getAsStrParaByName(id,"Title on Sheet")
					newName = s.title()
					setParaByName(id,"Title on Sheet",newName)
					outPuts.append (s+" -> changed to: "+newName+'\n')
				
			elif type == 3: #upper case
				print "sheet name upper"
				for row in self._dataGridView1.SelectedRows:
					id=ElementId(int(row.Cells[2].Value))
					v = doc.get_Element(id)			
					s = getAsStrParaByName(id,"Title on Sheet")
					newName = s.upper()
					setParaByName(id,"Title on Sheet",newName)
					outPuts.append (s+" -> changed to: "+newName+'\n')
	def viewTypeRight(self,id):
		#print "inside view type check: ",doc.get_Element(id).ViewType
		vType=doc.get_Element(id).ViewType
		if vType == ViewType.AreaPlan:
			return True
		elif vType == ViewType.CeilingPlan:
			return True
		elif vType == ViewType.Detail:
			return True
		elif vType == ViewType.DraftingView:
			return True
		elif vType == ViewType.DrawingSheet:
			return True
		elif vType == ViewType.Elevation:
			return True
		elif vType == ViewType.FloorPlan:
			return True
		elif vType == ViewType.Rendering:
			return True
		elif vType == ViewType.Schedule:
			return True
		elif vType == ViewType.ThreeD:
			return True
		elif vType == ViewType.Section:
			return True
		elif vType == ViewType.Legend:
			return True
		#print "return False"
		return False
	def showOutPut(self):
		if outPuts.Count !=0:
			sb=StringBuilder()
			for s in outPuts:
				sb.Append(s)
			TaskDialog.Show("Name Updated",sb.ToString())
		else:
			TaskDialog.Show("Name Updated","nothing updated")
	def populateDataGridView(self):
		self._dataGridView1.Rows.Clear()
		allViewsId=self.getAllViews()
		for id in allViewsId:
			if self.viewTypeRight(id):
				 row = []
				 row.append(doc.get_Element(id).ViewType)
				 row.append(doc.get_Element(id).Name)
				 #print "row 0: ",row[0]
				 row.append(id.ToString())
				 row.append(getAsStrParaByName(id,"Title on Sheet"))
				 #row.append("test")
				 #print "row 1:",row[1]
				 self._dataGridView1.Rows.Add(row[0],row[1],row[2],row[3])
				 
	
	def getAllViews(self):
		global totalView
		viewInstancesFilter = ElementClassFilter(clr.GetClrType(rView))
		collector = FilteredElementCollector(doc)
		textsId = collector.WherePasses(viewInstancesFilter).ToElementIds()
		totalView=textsId.Count
		print totalView, " views picked"
		return textsId
	def selectAllClicked(self, sender, event):
		self._dataGridView1.SelectAll()
		intLastRow = self._dataGridView1.RowCount-1
		print intLastRow
		self._dataGridView1.Rows[intLastRow].Selected = False
		
	def selectNoneClicked(self, sender, event):
		self._dataGridView1.ClearSelection()
	def btnReplaceClicked(self, sender, event):
		#print "btnReplaceClicked."
		if self._ckbTrueName.Checked:
			for row in self._dataGridView1.SelectedRows:
				v = doc.get_Element(ElementId(int(row.Cells[2].Value)))
				s = v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
				newName = s.Replace(self._tbxFind.Text,self._tbxReplace.Text)
				v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newName)
				outPuts.append (s+"-> changed to: "+newName+'\n')
		self.updateSheetName(1)
		self.showOutPut()
		self.Close()
	def btnTitleClicked(self, sender, event):
		if self._ckbTrueName.Checked:
			for row in self._dataGridView1.SelectedRows:
				v = doc.get_Element(ElementId(int(row.Cells[2].Value)))			
				s = v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
				newName = s.title()
				v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newName)
				outPuts.append (s+"-> changed to: "+newName+'\n')
		self.updateSheetName(2)
		self.showOutPut()
		self.Close()
	def btnUpperClicked(self, sender, event):
		if self._ckbTrueName.Checked:
			for row in self._dataGridView1.SelectedRows:
				v = doc.get_Element(ElementId(int(row.Cells[2].Value)))
				s = v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
				newName = s.upper()
				v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newName)
				outPuts.append (s+"-> changed to: "+newName+'\n')
		self.updateSheetName(3)
		self.showOutPut()
		self.Close()
	def btnCancelClicked(self, sender, event):
		self.Close()
	def btnWriteExcelClicked(self, sender, event):
		global totalView
		print "btnWriteExcel activated."
		print "total view: ",totalView
		#Accessing the Excel applications.
		xlApp = System.Runtime.InteropServices.Marshal.GetActiveObject('Excel.Application')
		
		#Worksheet, Row, and Column parameters
		worksheet = 1
		rowStart = 1
		columnStart = 1
		#clear worksheet
		xlApp.Worksheets(worksheet).UsedRange.Clear()
		
		print "befor for loop", totalView
		n=0
		while n < totalView-1 :
			#print "n= ",n
			row = self._dataGridView1.Rows[n]
			name = row.Cells[1].Value
			id = row.Cells[2].Value
			#insert view name
			data1 = xlApp.Worksheets(worksheet).Cells(n+1, 1)
			data1.Value = name
			data2 = xlApp.Worksheets(worksheet).Cells(n+1, 2)
			data2.Value = id
			n += 1
		
	def isodd(self,num):
		return num & 1 and True or False
	def	btnReadExcelClicked(self, sender, event):
		worksheet=1
		#Accessing the Excel applications.
		xlApp = System.Runtime.InteropServices.Marshal.GetActiveObject('Excel.Application')
		#print "btnReadExcel activated."
		range = xlApp.Worksheets(worksheet).UsedRange
		columnIndex=1
		dict={}
		newName=str()
		id = 0
		for c in range.Cells:
			if self.isodd(columnIndex):
				newName = c.Value2
				#print "new name: ",newName
			elif not(self.isodd(columnIndex)):
				id = int(c.Value2)
				#print "id: ",id," = ",newName
				self.renameView(id,newName)
			columnIndex += 1
		#rename view if there is any change
		self.showOutPut()
		self.Close()
		
	def renameView(self,id,newName):
		eid=ElementId(id)
		v=doc.get_Element(eid)
		s = v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
		if not(s == newName):
			v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newName)
			outPuts.append(s+"-> changed to: "+newName+'\n')
		#else:
			#print"same name no change"
			
			
	def checkTextboxEmpty(self):
		#if self._tbxFind.isEmpty():
		print "inside check text box empty."
		
		
		
		
#main program
#define a transaction variable and describe the transaction
t = Transaction(doc,'View Name Text Replace Case Change')

#start a transaction in the Revit database
t.Start()

#************ ADD YOUR OWN CODES HERE.******************
if uidoc.Selection.Elements.IsEmpty:
	print ("selesct section first")
	form = CheckBoxExampleForm()
	Application.Run(form)
	
else:
	y = int(raw_input("1.change view name, 2 Change title on sheet: "))
	if y == 1:
		x = int(raw_input("1. replace text, 2.Change Case to Title, 3.UPPER CASE: "))
		if x == 1: #change view name
			findTxt = raw_input("text in View Name to replace: ")
			newTxt = raw_input("replace to text: ")
			for v in selection:
				s = v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
				newName = s.Replace(findTxt,newTxt)
				v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newName)
				print s," changed to: ",newName
		elif x==2: #  title case
			for v in selection:
				s = v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
				newName = s.title()
				v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newName)
				print s," changed to: ",newName
		elif x==3: #UPPER CASE
			for v in selection:
				s = v.get_Parameter(BuiltInParameter.VIEW_NAME).AsString()
				newName = s.upper()
				v.get_Parameter(BuiltInParameter.VIEW_NAME).Set(newName)
				print s," changed to: ",newName
	elif y == 2: #change title on sheet
		x = int(raw_input("1. replace text, 2.Change Case to Title, 3.UPPER CASE: "))
		if x == 1: #change view name
			findTxt = raw_input("text in View Name to replace: ")
			newTxt = raw_input("replace to text: ")
			for v in selection:
				id=v.Id
				s = getAsStrParaByName(id,"Title on Sheet")
				newName = s.Replace(findTxt,newTxt)
				setParaByName(id,"Title on Sheet",newName)
				print s," -> changed to: ",newName
		elif x==2: #  title case
			for v in selection:
				id=v.Id
				s = getAsStrParaByName(id,"Title on Sheet")
				newName = s.title()
				setParaByName(id,"Title on Sheet",newName)
				print s," -> changed to: ",newName
		elif x==3: #UPPER CASE
			for v in selection:
				id=v.Id
				s = getAsStrParaByName(id,"Title on Sheet")
				newName = s.upper()
				setParaByName(id,"Title on Sheet",newName)
				print s," -> changed to: ",newName
			
	

	
#************** END OF YOUR MAJOR CODES HERE.*********************
#commit the transaction to the Revit database
t.Commit()
time.sleep(1)

#close the script window
__window__.Close()
	
