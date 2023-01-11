# Script recorded 01 Dec 2022, 13:49:13

#   RayStation version: 13.1.0.144
#   Selected patient: ...

from connect import *

case = get_current("Case")
beam_set = get_current("BeamSet")


with CompositeAction('Add beam (10x10, beam set: 10x10)'):

  retval_0 = beam_set.CreatePhotonBeam(
  BeamQualityId="6", 
  CyberKnifeCollimationType="Undefined", 
  CyberKnifeNodeSetName=None, 
  CyberKnifeRampVersion=None, 
  CyberKnifeAllowIncreasedPitchCorrection=None, 
  IsocenterData={ 'Position': { 'x': 0, 'y': -25.0, 'z': 25 }, 'NameOfIsocenterToRef': "", 'Name': "10x10 1", 'Color': "98, 184, 234" }, 
  Name="10x10", 
  Description="", 
  GantryAngle=0, 
  CouchRotationAngle=0, 
  CouchPitchAngle=0, 
  CouchRollAngle=0, 
  CollimatorAngle=0
  )

  retval_0.SetBolus(BolusName="")

  beam_set.Beams['10x10'].BeamMU = 0

  # CompositeAction ends 

