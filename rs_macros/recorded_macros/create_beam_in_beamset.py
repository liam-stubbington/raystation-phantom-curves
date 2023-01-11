# Script recorded 02 Dec 2022, 11:53:45

#   RayStation version: 13.1.0.144
#   Selected patient: ...

from connect import *

beam_set = get_current("BeamSet")


with CompositeAction('Add beam (10x15, beam set: 10x10)'):

  retval_0 = beam_set.CreatePhotonBeam(BeamQualityId="6", CyberKnifeCollimationType="Undefined", CyberKnifeNodeSetName=None, CyberKnifeRampVersion=None, CyberKnifeAllowIncreasedPitchCorrection=None, IsocenterData={ 'Position': { 'x': 0, 'y': -25, 'z': 25 }, 'NameOfIsocenterToRef': "10x10 1", 'Name': "10x10 1", 'Color': "98, 184, 234" }, Name="10x15", Description="10x15 100SSD", GantryAngle=0, CouchRotationAngle=0, CouchPitchAngle=0, CouchRollAngle=0, CollimatorAngle=0)

  retval_0.SetBolus(BolusName="")

  beam_set.Beams['10x15'].BeamMU = 0

  # CompositeAction ends 


retval_0.CreateRectangularField(Width=10, Height=15, CenterCoordinate={ 'x': 0, 'y': 0 }, MoveMLC=True, MoveAllMLCLeaves=False, MoveJaw=True, JawMargins={ 'x': 0, 'y': 0 }, DeleteWedge=False, PreventExtraLeafPairFromOpening=False)
