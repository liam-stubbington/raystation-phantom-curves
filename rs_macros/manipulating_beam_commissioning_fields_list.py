from connect import get_current

patient_db = get_current("PatientDB")
beam_set = get_current("BeamSet")

 
def list_all():
    # List all Beams in Commissioning Fields List
    for beam in patient_db.ListAllBeamCommissioningFieldNames():
        print(beam)


def remove_all():
    # Remove all beams in Commissioning Fields list
    for beam in patient_db.ListAllBeamCommissioningFieldNames():
        patient_db.RemoveBeamCommissioningField(FieldName = beam)

def add_all_to_list(desc: str, suffix: str = None): 
    # Add all beams in current beam_set to Commissioning Fields list
    for beam in beam_set.Beams:
        patient_db.CopyBeamToBeamCommissioningField(
            FieldName = beam.Name+suffix,
            BeamToCopy = beam,
            Description = desc 
        )

def add_all_to_beamset(qi: str = "6", ssd: int = 85, filt: str = None):
    # Add all Commissioning Fields to current BeamSet
    if filt:
        beams_to_add_list = [
            beam_name for beam_name in patient_db.ListAllBeamCommissioningFieldNames() 
            if filt in beam_name
            ]
    else: 
        beams_to_add_list = [
            beam_name for beam_name in  patient_db.ListAllBeamCommissioningFieldNames() ]

    for beam_name in beams_to_add_list:
        print(beam_name)
        beam_set.AddBeamFromBeamCommissioningField(
            Field=patient_db.LoadBeamCommissioningField(FieldName=beam_name),
            BeamQualityId = qi,
            SSD = ssd
        )


if __name__ == "__main__":
    list_all()
    add_all_to_beamset(
        ssd=85,
    )