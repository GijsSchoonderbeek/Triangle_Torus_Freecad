"""
Examples for a feature class and its view provider.
(c) 2009 Werner Mayer LGPL
"""

__author__ = "Werner Mayer <wmayer@users.sourceforge.net>"

import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
import DraftVecUtils
import math
faces=[]


 
def torus():
	global faces
	Sides=8        # sides per ring
	Rings=6			# Nof ring on the torus
	Width=250 		# approximately final diameter in mm
	Height=Width/3.5
	App.Console.PrintMessage("\n Draw Torus with " + str(Sides) + " Sides, " + str(Sides*Rings*2) +" Faces \n")
	Total_lenght=0
	ring_loc = []
	v_cross=[]
	v_cross_base = FreeCAD.Vector(Height/2,0,0)

#Make the Y / Z locations (cross section) of the Torus 
	for side in range(Rings):
		r_angle =((side-0.5)*(2*math.pi/Rings))+(math.pi/2)
		ring_loc.append(DraftVecUtils.rotate(v_cross_base,-r_angle,FreeCAD.Vector(0,1,0)))

#Make the vertex points on the Torus
	v=[]
	for ring_cnt in range(Rings):
		vr=[]
		base_vector = FreeCAD.Vector((Width-Height)/2,0,0)+ring_loc[ring_cnt]
		for cnt in range(0,Sides):
			if (ring_cnt % 2)==0:
				r_angle=((cnt+0.5)*(2*math.pi/Sides))
			else:
				r_angle=(cnt*(2*math.pi/Sides))
			vr.append(DraftVecUtils.rotate(base_vector,r_angle))
		v.append(vr)
	
# Make the wires/faces
	f=[]
	for ring in range(Rings):
		for cnt in range(Sides):
			v0=v[ring][cnt]
			v1 = v[ring][(cnt+1)%Sides]  					# % Sides --> Start at 0 when round
			v2 = v[(ring+1)%Rings][(cnt+1-(ring%2))%Sides]	# % 2 --> when odd ring use next vertex on next ring
			f.append(make_face(v0,v1,v2)) 					# Up facing Triangle
			v0 = v[(ring+1)%Rings][cnt]						# % Rings --> start at 0 when round
			v1 = v[(ring+1)%Rings][(cnt+1)%Sides]			# % Sides --> Start at 0 when round
			v2 = v[ring][(cnt+(ring%2))%Sides]				# when even ring use next vertex on previous ring
			f.append(make_face(v0,v1,v2))  					# Down facing Triangle
			if cnt ==0:										# Loop for printing triangle information
				App.Console.PrintMessage("Ring " + str(ring) + "\n")
				for face_cnt in range(2):
					edge_lengths=[]
					for edge_cnt in range(3):				
						edge_lengths.append(round(f[2*ring*Sides+face_cnt%2].Edges[edge_cnt].Length,1))
						App.Console.PrintMessage("Length Edge nr. " + str(edge_cnt) + " : " + str(edge_lengths[-1]) + "mm \n")
					angle = round(360*math.asin((edge_lengths[0]/2)/edge_lengths[1])/math.pi,1)
					App.Console.PrintMessage("Angle: " + str(angle)+ "deg , 2x " + str((180-angle)/2) + "deg --> miter: " + str(round(90-(180-angle)/2,1)) + "deg\n")
#				App.Console.PrintMessage("Total Lenght Ring " + str(16*edge_lengths[0]) + "\n")
				vns1 = f[2*ring*Sides].normalAt(0,0)
				vns2 = f[2*ring*Sides+1].normalAt(0,0)
				Angle_1_2=180-round(math.degrees(vns1.getAngle(vns2)),2)
				App.Console.PrintMessage("Angle faces " + str(Angle_1_2) + " deg --> SAW angle: " + str(Angle_1_2/2) + "deg \n")
		Total_lenght += 16*edge_lengths[0]
	for ring_cnt in range(Rings):
		vns1 = f[(2*Sides*ring_cnt)+1].normalAt(0,0)
		vns2 = f[(2*Sides*((ring_cnt+1)%Rings))].normalAt(0,0)
		Angle_1_2=180-round(math.degrees(vns1.getAngle(vns2)),1)
		App.Console.PrintMessage("Angle faces Ring "+ str(ring_cnt) + "-" +str((ring_cnt+1)%Rings)+ " "+ str(Angle_1_2) + " deg --> SAW angle : " + str(round(Angle_1_2/2,1)) + "deg \n")
	App.Console.PrintMessage("Total Length wood " + str(Total_lenght) + "mm \n")
#	dist = f[0+1].distToShape(f[2*(Rings/2)].normalAt(0,0))

#	App.Console.PrintMessage("Diastance between opposite faces " + str(dist) + "mm \n")
	faces=f

	shell=Part.makeShell(f)
	solid=Part.makeSolid(shell)
	Shape = solid
	return Shape

def make_face(v1,v2,v3):									#Function to make the faces of the triangles
	wire = Part.makePolygon([v1,v2,v3,v1])
	face = Part.Face(wire)
	return face

def makeTorus():											#Function to make the Torus
	FreeCAD.newDocument()
	a = torus()
	Part.show(a)

makeTorus()
