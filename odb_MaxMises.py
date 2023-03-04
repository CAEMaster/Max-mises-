#!/user/bin/python
# -* - coding:UTF-8 -*-

from abaqus import *
from abaqusConstants import *
import visualization
import displayGroupOdbToolset as dgo


vp = session.viewports[session.currentViewportName]
odb = vp.displayedObject
if type(odb) != visualization.OdbType: 
    raise 'show odb file¡£'


maxValue = None
stressOutputExists = FALSE
for step in odb.steps.values():
    print 'finding step:', step.name
    for frame in step.frames:
        try: 
            stress = frame.fieldOutputs['S']
            stressOutputExists = TRUE
        except KeyError: 
            continue
        for stressValue in stress.values:
            if (not maxValue or
                    stressValue.mises > maxValue.mises):
                    maxValue = stressValue
                    maxStep, maxFrame = step, frame  
               


print 'max Mises %E £º' % maxValue.mises
print '  step name:             ', maxStep.name 
print '  frame:                 ', maxFrame.frameId    
print '  part name:           ', maxValue.instance.name
print '  node:           ', maxValue.elementLabel 
print '  sectionPoint:             ', maxValue.sectionPoint
print '  integrationPoint:             ', maxValue.integrationPoint


leaf = dgo.Leaf(ALL_SURFACES)
vp.odbDisplay.displayGroup.remove(leaf)
leaf = dgo.LeafFromElementLabels(partInstanceName=maxValue.instance.name, 
    elementLabels=(maxValue.elementLabel,) )
vp.setColor(leaf=leaf, fillColor='Red')
vp.odbDisplay.commonOptions.setValues(renderStyle=FILLED,
    elementShrink=ON, elementShrinkFactor=0.15)
vp.odbDisplay.display.setValues(plotState=(UNDEFORMED,))