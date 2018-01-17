"""

Generate some example cells with spines..

"""

from neuroml import Cell
from neuroml import Morphology
from neuroml import Point3DWithDiam
from neuroml import Segment
from neuroml import SegmentParent
from neuroml import SegmentGroup
from neuroml import Member
from neuroml import Input
from neuroml import InputList
from neuroml import Instance
from neuroml import Location
from neuroml import Network
from neuroml import NeuroMLDocument
from neuroml import PoissonFiringSynapse
from neuroml import Population
from neuroml import Projection
from neuroml import Property
import neuroml.writers as writers
import random
import math



nml_doc = NeuroMLDocument(id="Example2")

nml_doc.notes = "Demo of cell with spines"

net = Network(id=nml_doc.id)

net.notes = nml_doc.notes

nml_doc.networks.append(net)
populations = {}


def add_instance(name, x,y,z):
    
    pop = populations[name]
    inst = Instance(id=len(pop.instances))
    pop.size=pop.size+1
    pop.instances.append(inst)
    inst.location = Location(x=x,y=y,z=z)
    
    
def on_circle(fract,radius):
    return radius*math.sin(fract*2*math.pi),radius*math.cos(fract*2*math.pi)
    

def create_object(name, color,x=0,y=0,z=0):

    obj = Cell()
    obj.name = name
    obj.id = name
    nml_doc.cells.append(obj)
    morphology = Morphology(id='mm')  
    obj.morphology = morphology
    
    pop = Population(id="Pop_%s"%name, component=obj.id, type="populationList",size=0)
    net.populations.append(pop)
    populations[name]=pop
    pop.properties.append(Property(tag="color", value=color))
    add_instance(name,x,y,z)
    
    sg = SegmentGroup(id='all')
    obj.morphology.segment_groups.append(sg)
    
    return obj

def add_segment(obj,p0,p1,name=None):
    

    p = Point3DWithDiam(x=p0[0],
                                y=p0[1],
                                z=p0[2],
                                diameter=p0[3])
    d = Point3DWithDiam(x=p1[0],
                                y=p1[1],
                                z=p1[2],
                                diameter=p1[3])

    segid = len(obj.morphology.segments)
    
    parent = None if segid==0 else SegmentParent(segments=segid-1)
    
    segment = Segment(id=segid,
                              proximal = p, 
                              distal = d, 
                              parent = parent)
    if name:
        segment.name=name
                    
    obj.morphology.segment_groups[0].members.append(Member(segments=segid))
    
    obj.morphology.segments.append(segment)
    
    return segment


cell1 = create_object('OneSeg','0 .4 0',x=0,y=0,z=0)
cell2 = create_object('TwoSeg','1 .4 0',x=0,y=100,z=0)

add_segment(cell1,(0,0,0,10),(20,0,0,10),name='soma') 

add_segment(cell2,(0,0,0,10),(20,0,0,10),name='soma') 
add_segment(cell2,(20,0,0,5),(40,0,0,5),name='soma') 

'''
dend_seg_num = 10
seg_length = 10
seg_diam = 2

for i in range(dend_seg_num):
    add_segment(cell1,(0,seg_length*i,0,seg_diam),(0,seg_length*(i+1),0,seg_diam),name='dend_%s'%i) '''


add_instance(cell1.id, 100,0,0)
'''
add_instance(cell1.id, -10,100,0)
add_instance(cell1.id, 10,0,100)'''

nml_file = '%s.net.nml'%net.id
writers.NeuroMLWriter.write(nml_doc, nml_file)


print("Created:\n"+nml_doc.summary())
print("Written network file to: "+nml_file)



###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)

