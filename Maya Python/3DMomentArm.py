###
### This is a test script for calculating the perpendicular distance between a point and a line (measure tool) in 3D
###
import maya.cmds as cmds #loads in native Maya MEL command library
import maya.api.OpenMaya as om #loads in OpenMaya API (Maya C++ via Python wrapper)

## Function: Makes a new locator and stores its coordinates in testLocator_xyz
def makeTestLocator(x0,y0,z0,name):
    testLocator=cmds.spaceLocator(name=name,position=[0,0,0])
    cmds.move(x0,y0,z0,testLocator)
    testLocator_xyz=om.MVector(cmds.xform(testLocator, query=True, translation=True))
    print "test locator's coordinates are: "+name+":"+str(testLocator_xyz)
    return testLocator_xyz
    
## Function: Makes a new measure tool and stores its locators in newLocators
def makeMeasureTool(name0,x1,y1,z1,name1,x2,y2,z2,name2):
    scene_before = cmds.ls(l=True, transforms=True)
    cmds.distanceDimension(sp=[x1,y1,z1],ep=[x2,y2,z2])
    scene_after = cmds.ls(l=True, transforms=True)    #gets 'after' list of scene objects 
    newMeasureObjects = list(set(scene_after).difference(scene_before))    #gets new objects in scene (measure tool and locators)
    print "New Measure Tool objects are: "+str(newMeasureObjects)
    newLocators = [newMeasureObjects[2],newMeasureObjects[1]]    #grabs locators from list
    #print newLocators
    newLocators[0]=cmds.rename(newMeasureObjects[2],name1)
    newLocators[1]=cmds.rename(newMeasureObjects[1],name2)
    return newLocators

## Function: Returns the xyz coordinates of the measure tool's locators
def measureToolQuery():
    measureToolCoordinates = []    #create empty list
    for i in newLocators:
        print newLocators
        testLocator_xyz=cmds.xform(i, query=True, translation=True)
        #print "measure tool "+str(i[1:])+"'s coordinates are: "+str(testLocator_xyz)
        measureToolCoordinates.append(testLocator_xyz)    #add new coordinates to empty list created earlier
    measureLocator1_xyz=om.MVector(measureToolCoordinates[0])    #converts coordinates from list of floats to position vector using MVector class in OpenMaya API
    measureLocator2_xyz=om.MVector(measureToolCoordinates[1])    #converts coordinates from list of floats to position vector using MVector class in OpenMaya API
    print "measure tool locator B's coordinates are: "+str(measureLocator1_xyz)
    print "measure tool locator C's coordinates are: "+str(measureLocator2_xyz)
    return measureLocator1_xyz,measureLocator2_xyz    #multiple values are returned from this function, and may be accessed by calling the function on the same number of variables (in this case, 2)
    
##Function: Calculates the perpendicular distance from a point A to a line between points B and C
def perpendicularDistance(A,B,C,name):
    vectBA=A-B    #vector math is supported by the OpenMaya MVector class
    vectBC=C-B
    unitBC=vectBC/om.MVector.length(vectBC)    #get unit vector for BC by dividing BC vector by its scalar magnitude
    distT=vectBA*unitBC    #get distance T from point B to projection P of point A on vector BC
    projectionP=B+distT*unitBC    #get projection P of point A on vector BC as sum of postion B and distance T
    vectAP=projectionP-A
    distanceResult=om.MVector.length(vectAP)
    #projectionPpos=list(projectionP)
    makeMeasureTool("momentArm"+name, A[0],A[1],A[2],"jointCenter"+name,projectionP[0],projectionP[1],projectionP[2],"projection"+name)
    print "the perpendicular distance is: "+str(distanceResult)
    return distanceResult

##test case 1: coplanar, perpendicular to grid
#A_xyz=makeTestLocator(0,10,0,"A")
#newLocators=makeMeasureTool(-10,0,0,"B",10,0,0,"C")
#B_xyz,C_xyz=measureToolQuery()
#distanceResult=perpendicularDistance(A_xyz,B_xyz,C_xyz)

##test case 2: collinear on arbitrary line
#A_xyz=makeTestLocator(7,8.5,15.5,"A")
#newLocators=makeMeasureTool(1,2,11,"B",13,15,20,"C")
#B_xyz,C_xyz=measureToolQuery()
#distanceResult=perpendicularDistance(A_xyz,B_xyz,C_xyz)

##test case 3: non-collinear on arbitrary plane
A_xyz=makeTestLocator(8,9,12,"A")
newLocators=makeMeasureTool("MuscleName",1,12,11,"B",13,15,20,"C")
B_xyz,C_xyz=measureToolQuery()
distanceResult=perpendicularDistance(A_xyz,B_xyz,C_xyz,"MuscleNameMomentArm")

##stuff to make this a moment arm thing. TEST_glenohumeralcenter is at joint center
#cmds.xform("TEST_glenohumeralcenter", query=True, translation=True, worldSpace=True)    #worldSpace flag uses world's frame of reference, not parent's frame
