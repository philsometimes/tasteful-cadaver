###
###This makes 1) a body plane from tracked body markers, or 2) a muscle measure tool from tracked muscle markers.
###
import maya.cmds as cmds #loads in native Maya command library

##function: make body plane##
def makeBodyPlane():
    if bpMarkers==[]: #checks to see if body markers have been selected
        cmds.confirmDialog(title='No markers selected', message='Please select body markers in ascending order.', button=['Okay'], defaultButton='Okay')
    else:  
        cmds.polyPlane(name='bodyPlane',sx=1,sy=1) #makes polygon plane 'bodyPlane' with 1x1 subdivisions
        cmds.select(cl=True) #clears active selection
        cmds.select('bodyPlane'+'.vtx[0:3]',add=True) #selects all 4 vertices in plane
        bpVertices = cmds.ls(sl=1, fl=1) #makes array of vertices from selection (-fl flag says flatten)
        cmds.delete(bpVertices[-1]) #deletes 4th vertex to make triangular plane
        return bpVertices #allows us to get bpVertices outside scope of makeBodyPlane function
        
##funcion: move body plane vertices to body marker locations##
def orientBodyPlane():
    for i,j in zip(bpMarkers,bpVertices): #iterates simultaneously over both lists (body markers and plane vertices
        bp_xyz=cmds.xform(i, query=True, translation=True) #queries xyz location of body markers
        cmds.move(bp_xyz[0],bp_xyz[1],bp_xyz[2],j) #moves remaining 3 plane vertices to xyz locations of body markers
        
##function: make measure tool from any set of 2 muscle markers
def makeMeasureTool():
    scene_before = cmds.ls(l=True, transforms=True)    #gets 'before' list of scene objects    
    cmds.distanceDimension( startPoint=(0, 0, 0), endPoint=(1, 1, 1) ) #makes measure tool with start and end points at the origin
    scene_after = cmds.ls(l=True, transforms=True)    #gets 'after' list of scene objects 
    newMeasure = list(set(scene_after).difference(scene_before))    #gets new objects in scene (measure tool and locators)
    newLocators = [newMeasure[1],newMeasure[0]]    #grabs locators from list
    
    for i,j in zip(msMarkers,newLocators):
         ms_xyz=cmds.xform(i, query=True, translation=True) #queries xyz location of muscle markers
         cmds.move(ms_xyz[0],ms_xyz[1],ms_xyz[2],j) #moves  to xyz locations of body markers
         cmds.rename(j,i+'_measure')    
         basename=i[0:-2]   #gets muscle name for later use
         
    cmds.rename(newMeasure[2],basename+'distance')

##prompt user to select desired action##
userInput=cmds.confirmDialog( title='Choose option', message='Make sure you already have body/muscle marker locators selected in ascending order', button=['Make body plane','Make muscle measure tool','Cancel'], cancelButton='Cancel')

if userInput=='Make body plane':
    bpMarkers = cmds.ls(sl=1, fl=1) #makes new variable bpMarkers containing a list of selected body markers
    bpVertices=makeBodyPlane() #gets bpVertices variable out of makeBodyPlane function so it can be used by orientBodyPlane function
    orientBodyPlane()
    
elif userInput=='Make muscle measure tool':
    msMarkers = cmds.ls(sl=1, fl=1) #makes new variable msMarkers containing a list of selected muscle markers
    makeMeasureTool()

