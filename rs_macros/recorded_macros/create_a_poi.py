# Script recorded 01 Dec 2022, 16:56:25

#   RayStation version: 13.1.0.144
#   Selected patient: ...

from connect import *

case = get_current("Case")
examination = get_current("Examination")


retval_0 = case.PatientModel.CreatePoi(Examination=examination, Point={ 'x': 0.5, 'y': -15, 'z': 25 }, Name="10.5cm", Color="Yellow", VisualizationDiameter=1, Type="Undefined")
