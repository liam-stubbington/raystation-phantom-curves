# Author: Liam Stubbington, RT Physicist 
# Cambridge University Hospitals NHS Foundation Trust 

# -- IMPORTS -- 
import sys, os
from connect import get_current 

# -- ADD FOLDER TO SYSTEM PATH -- 
rs_macros = os.path.normpath("//cuh_nas120/Medical Physics & Clinical Engineering/Userdata/Radiotherapy/Liam Stubbington/beam-model/rs_macros/")
mcc = os.path.normpath("//cuh_nas120/Medical Physics & Clinical Engineering/Userdata/Radiotherapy/Liam Stubbington/beam-model/mcc/")
sys.path.append(rs_macros)
sys.path.append(mcc)

# IMPORT MY MODULES --
from raystation_curves import RayCurves
from ptw_mcc import PTW_mcc 

# -- CONSTANTS -- 
beam_set = get_current("BeamSet")
PROJECT_ROOT = os.getcwd() 

# -- MAIN -- #
if __name__ == "__main__":           


    for beam_dose in beam_set.FractionDose.BeamDoses:
        rc = RayCurves(
            beam_dose
        )

        pdd_mcc = PTW_mcc(
            rc,
            curve_type = "pdd",
            depth = None,
            energy = 6.3,
            positions = rc.pdd_positions,
            dose = rc.pdd,
            f_root = PROJECT_ROOT
        )

        pdd_mcc.write_mcc()

        for y, d in zip(rc.crossplane_profiles, rc.cax_depths):
            crossplane_profile_mcc = PTW_mcc(
                rc,
                curve_type = "x profile",
                depth = d,
                energy = rc.energy,
                positions =rc.crossplane_positions,
                dose = y,
                f_root = PROJECT_ROOT
            )
            crossplane_profile_mcc.write_mcc() 

        for y, d in zip(rc.inplane_profiles, rc.cax_depths):
            inplane_profile_mcc = PTW_mcc(
                rc,
                curve_type = "y profile",
                depth = d,
                energy = 6.3,
                positions = rc.inplane_positions,
                dose = y,
                 f_root = PROJECT_ROOT
            )
            inplane_profile_mcc.write_mcc() 
