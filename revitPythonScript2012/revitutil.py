# IronPython Pad. Write code snippets here and F5 to run.
'''
revitutil.py

a collection of utillity functions / stuff for working with
revit in the RevitPythonShell.

Last updated: 2011-01-26
'''

# add references to needed assemblies
import clr
clr.AddReference('System')
clr.AddReference('mscorlib')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

# import some stuff from those assemblies
import Autodesk.Revit
import System
from System.Collections.Specialized import *
from System.Collections.Generic import *

from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import TaskDialog

def alert(msg):
    TaskDialog.Show('RevitPythonShell', msg)

def meters(feet):
    return float(feet) * 0.3048

def removeParameters(parameterFilePath, document):
    '''removes all parameters in parameterFile from the document (unbinds them)'''
    document.Application.Options.SharedParametersFilename = parameterFile
    df = document.Application.OpenSharedParameterFile()
    for dg in df.Groups:
        for d in dg.Definitions:
            print "removing parameter", d.Name
            document.ParameterBindings.Remove(d)

def listWindows(document):
    '''
    Returns a list of windows (FamilyInstance) in the document.
    '''    
    collector = FilteredElementCollector(document)
    collector = collector.OfCategory(BuiltInCategory.OST_Windows)
    collector = collector.OfClass(FamilyInstance)
    return list(collector)

def findWindowFace(window):
    '''
    Find the most likely candiate for being the face of a window as
    seen from outside the building.

    NOTE: This function returns a tuple (PlanarFace, GeometryElement),
    with the GeometryElement being the instance geometry for the
    FamilyInstance 'window'. The instance geometry should not be allowed
    to go out of scope, as that would render the PlanarFace invalid.
    '''
    geometry = window.get_Geometry(Options())
    gi = geometry.Objects.get_Item(0)
    g = gi.GetInstanceGeometry()
    solids = [o for o in g.Objects if isinstance(o, Solid)]
    faces = []
    for solid in solids:
        faces.extend([f for f in solid.Faces if isinstance(f, PlanarFace)])
    # NOTE: the following will fail if the host isn't a wall
    faces = [f for f in faces if isCollinear(f.Normal, window.Host.Orientation)]
    faces = sorted(faces, key=lambda f: f.Area, reverse=True)
    return faces[0], g

def isCollinear(vec1, vec2):
    '''
    returns true, if vec1 and vec2 are collinear. Both arguments must have
    X, Y and Z attributes, like points and vectors in Revit.
    '''
    # scalarProduct is either -1 or 1 for collinear vectors
    scalarProduct = vec1.X * vec2.X + vec1.Y * vec2.Y + vec1.Z * vec2.Z
    return 1 - abs(scalarProduct) < 0.001 # close enough to 1 or -1

def getParameter(element, parameterName):
    '''
    retrieves a (string) parameter from the document.
    '''
    parameter = element.get_Parameter(parameterName)
    if parameter:
        return parameter.AsString()
    else:
        raise KeyError('Element %d does not have requested parameter %s' % (element.Id.IntegerValue, parameterName))

def setParameter(element, parameterName, value):
    '''
    sets a (string) parameter for an element.
    '''
    parameter = element.get_Parameter(parameterName)
    if parameter:
        parameter.Set(value)
    else:
        raise KeyError('Element %d does not have requested parameter %s' % (element.Id.IntegerValue, parameterName))

def getElementsByType(doc, type):
    '''
    Returns all elements of a given type in the document.
    '''
    collector = FilteredElementCollector(doc)
    return collector.OfClass(type).ToElements()

def getAnalysisDisplayStyle(doc, name):
    '''
    Returns the AnalysisDisplayStyle with the same name.
    '''
    import Autodesk.Revit.DB.Analysis
    styles = [ads for ads in getElementsByType(doc, Autodesk.Revit.DB.Analysis.AnalysisDisplayStyle) if ads.Name == name]
    if len(styles) > 0:
        return styles[0]
    else:
        return None
