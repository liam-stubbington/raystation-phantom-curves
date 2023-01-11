#   02 Dec 2022
#   Liam Stubbington, RT Physicist 

#   RayStation version: 13.1.0.144

'''
    Add Beams to Current BeamSet.
    Beam data read from csv. 
'''

from connect import get_current 
from csv import DictReader as DR
from os.path import normpath

my_plan = get_current("Plan")
my_beamset = get_current("BeamSet")

isoc = { 
    'Position': { 'x': 0, 'y': -25, 'z': 25 }, 
    'NameOfIsocenterToRef': "BeamModelVerif 1", 
    'Name': "BeamModelVerif 1", 
    'Color': "Lime", 
    }

def create_beam(beam):

    my_beam = my_beamset.CreatePhotonBeam(
        BeamQualityId="6", 
        CyberKnifeCollimationType="Undefined", 
        CyberKnifeNodeSetName=None, 
        CyberKnifeRampVersion=None, 
        CyberKnifeAllowIncreasedPitchCorrection=None, 
        IsocenterData= isoc,
        Name = beam['name'], 
        Description = beam['description'], 
        GantryAngle=0, 
        CouchRotationAngle=0, 
        CouchPitchAngle=0, 
        CouchRollAngle=0, 
        CollimatorAngle=0
    )

    my_beam.SetBolus(BolusName="")

    my_beam.CreateRectangularField(
        Width= beam['width'], 
        Height= beam['height'], 
        CenterCoordinate={ 'x': 0, 'y': 0 }, 
        MoveMLC=True, 
        MoveAllMLCLeaves=False, 
        MoveJaw=True, 
        JawMargins={ 'x': 0, 'y': 0 }, 
        DeleteWedge=False, 
        PreventExtraLeafPairFromOpening=False
        )

    my_beam.ConformMlc()
    my_beam.BeamMU = 100


f_path = normpath('//cuh_nas120/Medical Physics & Clinical Engineering/Userdata/Radiotherapy/Liam Stubbington/beam-model/rs_macros/data/verif_beams.csv')

with open(f_path, 'r', encoding='utf-8') as f:
    list_of_beams = [row for row in DR(f)] 

for beam in list_of_beams:
    create_beam(beam)    
