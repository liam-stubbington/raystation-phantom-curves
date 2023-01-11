#   02 Dec 2022
#   Liam Stubbington, RT Physicist 

#   RayStation version: 13.1.0.144

'''
    Extract the dose values from all beams in the current beamset, for a long list of points (x,y,z). 
    Output file is named according to beamset name. 
    Need to check coordinates of dose values are correct. 
'''


import numpy as np 
from connect import get_current 
from csv import DictReader as DR
from os import path

f_in = path.normpath('//cuh_nas120/Medical Physics & Clinical Engineering/Userdata/Radiotherapy/Liam Stubbington/beam-model/rs_macros/code-validation/coordinates_of_profile.csv')
f_root = path.normpath('//cuh_nas120/Medical Physics & Clinical Engineering/Userdata/Radiotherapy/Liam Stubbington/beam-model/rs_macros/data/')

beam_set = get_current("BeamSet")

with open(f_in, 'r', encoding = 'utf-8') as f: 
    a_ton_of_points = [row for row in DR(f)]

for beam_dose in beam_set.FractionDose.BeamDoses:
    f_out = path.join(f_root, beam_dose.ForBeam.Name + '.csv')
    a_dose_point_array_in_cGy = beam_dose.InterpolateDoseInPoints(
        Points=a_ton_of_points,
        PointsFrameOfReference=beam_set.FrameOfReference
    )
    np.savetxt(
        f_out, 
        a_dose_point_array_in_cGy, 
        delimiter=",", 
        fmt='%f'
        )


