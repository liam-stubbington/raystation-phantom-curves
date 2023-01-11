#   02 Dec 2022
#   Liam Stubbington, RT Physicist 

#   RayStation version: 13.1.0.144

'''
    Create BeamVerif Plan on current WaterTank phantom. 
'''

from connect import get_current 

case = get_current("Case")
exam = get_current("Examination")

my_plan = case.AddNewPlan(
    PlanName="BeamModelVerif", 
    PlannedBy="", 
    Comment="", 
    ExaminationName=exam.Name,
    IsMedicalOncologyPlan=False, 
    AllowDuplicateNames=False
    )

my_beamset = my_plan.AddNewBeamSet(
    Name=my_plan.Name, 
    ExaminationName=exam.Name, 
    MachineName="TrueBeamSTx", 
    Modality="Photons", 
    TreatmentTechnique="Conformal", 
    PatientPosition="HeadFirstSupine", 
    NumberOfFractions=1, 
    CreateSetupBeams=False, 
    UseLocalizationPointAsSetupIsocenter=False, 
    UseUserSelectedIsocenterSetupIsocenter=False, 
    Comment="", 
    RbeModelName=None, 
    EnableDynamicTrackingForVero=False, 
    NewDoseSpecificationPointNames=[], 
    NewDoseSpecificationPoints=[], 
    MotionSynchronizationTechniqueSettings={ 
            'DisplayName': None, 
            'MotionSynchronizationSettings': None, 
            'RespiratoryIntervalTime': None, 
            'RespiratoryPhaseGatingDutyCycleTimePercentage': None, 
            'MotionSynchronizationTechniqueType': "Undefined" 
            }, 
    Custom=None, 
    ToleranceTableLabel=None
    )
