# Script recorded 01 Dec 2022, 13:46:08

#   RayStation version: 13.1.0.144
#   Selected patient: ...

from connect import *

case = get_current("Case")


with CompositeAction('Add Treatment plan'):

  retval_0 = case.AddNewPlan(PlanName="10x10", PlannedBy="BEAM MODEL", Comment="add beam to water tank script", ExaminationName="CT 1", IsMedicalOncologyPlan=False, AllowDuplicateNames=False)

  retval_1 = retval_0.AddNewBeamSet(Name="10x10", ExaminationName="CT 1", MachineName="TrueBeamSTx", Modality="Photons", TreatmentTechnique="Conformal", PatientPosition="HeadFirstSupine", NumberOfFractions=1, CreateSetupBeams=False, UseLocalizationPointAsSetupIsocenter=False, UseUserSelectedIsocenterSetupIsocenter=False, Comment="", RbeModelName=None, EnableDynamicTrackingForVero=False, NewDoseSpecificationPointNames=[], NewDoseSpecificationPoints=[], MotionSynchronizationTechniqueSettings={ 'DisplayName': None, 'MotionSynchronizationSettings': None, 'RespiratoryIntervalTime': None, 'RespiratoryPhaseGatingDutyCycleTimePercentage': None, 'MotionSynchronizationTechniqueType': "Undefined" }, Custom=None, ToleranceTableLabel=None)

  # CompositeAction ends 



