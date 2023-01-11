#   02 Dec 2022
#   Liam Stubbington, RT Physicist 

#   RayStation version: 13.1.0.144

'''
    Extract the dose at a POI. 
    Coordinates of POI may not match dose point? 
'''

from connect import get_current 
case = get_current("Case")
exam = get_current("Examination")
beam_set = get_current("BeamSet")

# pois = [poi.Point for poi in case.PatientModel.StructureSets[exam.Name].PoiGeometries if "cm" in poi.OfPoi.Name]
a_for = exam.EquipmentInfo.FrameOfReference
a_for2 = beam_set.FrameOfReference 
print(a_for)
print(a_for2)
# these are the same... 

a_point = { 'x': -0.05, 'y': -20.05, 'z':25 }
'''
    Points are specified in the DICOM Patient coordinates from the specified frame of reference 
    d_10cm has coordinates {x: -0.05, y: 25, z: 20.05}
    In DICOM this is {x: -0.05, y:-20.05, z: 25}
    So the x coordinate is invariant, the y becomes minus RS z and the z becomes the RS y. 
'''

for beam_dose in beam_set.FractionDose.BeamDoses:
    a_dose_point_value_in_cGy = beam_dose.InterpolateDoseInPoint(
    Point=a_point,
    PointFrameOfReference=a_for
    ) 

    print(f"{beam_dose.ForBeam.Name}: {a_dose_point_value_in_cGy}")
  


'''
a_point = case.PatientModel.StructureSets["exam"].PoiGeometries["POI"].Point
a_for = case.Examinations["exam"].EquipmentInfo.FrameOfReference

a_dose_point_value_in_cGy = beam_set.FractionDose.InterpolateDoseInPoint(
    Point=a_point,
    PointFrameOfReference=a_for
    )

print(f"Dose at point is: {a_dose_point_value_in_cGy} [cGy]")

a_for = case.Examinations[examination].EquipmentInfo.FrameOfReference
another_point = { 'x': 0.5, 'y': -15, 'z': 25 }

a_dose_point_value_in_cGy = beam_set.FractionDose.InterpolateDoseInPoint(
    Point=another_point,
    PointFrameOfReference=a_for
    )

'''