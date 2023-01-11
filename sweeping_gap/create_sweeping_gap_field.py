from pydicom import dcmread 
from os import path 
import copy 

f_name = "10X_DLG_HD120.dcm"

class ASyncSweepingGapField():
    '''
        This class is used to manipulate Varian's DLG RT Plan files to produce async. sweeping gap fields. 
        You must give it a starting point path to an existing RT Plan file.
    '''
    def __init__(self, f_name: str, f_root: str = None):
        if f_root is None:
            self.f_root = "//cuh_nas120/Medical Physics & Clinical Engineering/Userdata/Radiotherapy/Liam Stubbington/beam-model/sweeping_gap/varian_dcm"
        else:
            self.f_root = f_root 
        self.f_path = path.join(self.f_root,f_name)
        self.f_name = f_name
        self.ds = dcmread(self.f_path)
        self.beams = [beam for beam in self.ds.BeamSequence]
        self.fractions = self.ds['FractionGroupSequence'][0] # expects only 1 element 
        self.setups = self.ds['PatientSetupSequence']
        
        

    def set_jaw_positions(self, f_out: str = "MOD_JAW_POSITIONS.dcm", jaw_pos: list = [-5.0, 5.0]):
        '''
            Set the jaw positions for each control point.
        '''
        for beam in self.ds.BeamSequence:
            print("Next Beam\n")
            for cp in beam.ControlPointSequence:
                print("Next ControlPoint\n") 
                for coll in cp.BeamLimitingDevicePositionSequence:
                    if coll["RTBeamLimitingDeviceType"].value == "ASYMY":
                        print("Found an ASYM Y value")
                        coll["LeafJawPositions"].value = jaw_pos

        self.ds.save_as(path.join(self.f_root,f_out))
        print("New RT Plan file @: "+path.join(self.f_root,f_out))


    def write_dcm_beams_to_txt(self):
        '''
            Dump certain beam attributes to text file. 
        '''
        f_name = self.f_name.split(".")[0]+".txt"

        with open(path.join(self.f_root,f_name), "w", encoding = "utf-8") as f: 
            
            f.write("RT Plan file "+self.f_name+" contains the following beams: \n")
            f.writelines([beam.BeamName+", " for beam in self.beams])

            f.write(f"There should be {self.fractions.NumberOfBeams} in the RT Plan file - CHECK THIS\n")
            f.write(f"There are {self.fractions.NumberOfFractionsPlanned} fractions planned - CHECK THIS\n")

            f.write("\n")

            for ref_beam in self.fractions.ReferencedBeamSequence:
                for elem in ref_beam:
                    f.write(f"{elem.keyword}: {elem.value}\n")

            f.write("\n")

            for beam in self.beams:
                
                f.write("Beam Name: "+beam.BeamName+"\n")
                f.write(f"Beam Number: {beam.BeamNumber}\n")
                for cp in beam.ControlPointSequence:
                    f.write("StartControlPoint\n") 
                    f.write(f"Cumulative MU: {cp.CumulativeMetersetWeight}\n")
                    for thing in cp:
                        f.write("Element of control point is called: "+thing.name+"\n")
                        
                        if thing.name == "Beam Limiting Device Position Sequence":
                            for t in thing: 
                                f.write("Collimation: " + t.RTBeamLimitingDeviceType+"\n")
                                list_of_positions = [str(l)+"\n" for l in t.LeafJawPositions]
                                f.write(f"MLC Positions {len(list_of_positions)}\n")
                                f.writelines(list_of_positions)
                                f.write("\n")
                                
                        f.write("\n")

    def print_mlc_positions_in_control_points(self, beam):

        for cp in beam.ControlPointSequence: 
            for thing in cp: 
                if thing.name == "Beam Limiting Device Position Sequence":
                    for t in thing: 
                        if t.RTBeamLimitingDeviceType == "MLCX":
                            print(t.LeafJawPositions)
                            print("\n")


    def create_beam_30mm(self):
        '''
            Adds the 30mm gap beam to the RT plan file. 
        '''
        # CREATE A COPY OF THE 20mm BEAMS 
        gap_30mm = [-80 for item in range(60)] + [-50 for item in range(60)]
        increment = [10 for item in range(120)]
        beam_20mm = [beam for beam in self.beams if beam.BeamName == "20mm"][0]
        beam_30mm = copy.deepcopy(beam_20mm) 
        beam_30mm.BeamName = "30mm"
        beam_30mm.BeamNumber += 1

        # CREATE A COPY OF LAST ELEMENT OF PATIENT SETUP SEQUENCE 
        ps = copy.deepcopy(self.setups[-1])
        ps.PatientSetupNumber += 1 
        self.setups.value.append(ps)
        
        # MODIFY REF DATA
        self.fractions.NumberOfBeams += 1
        self.fractions.NumberOfFractionsPlanned += 1
        ref_beam = copy.deepcopy(self.fractions.ReferencedBeamSequence[-1])
        ref_beam.ReferencedBeamNumber += 1 
        self.fractions.ReferencedBeamSequence.append(ref_beam)

        # MODIFY MLC POSITIONS
        i = 0
        for cp in beam_30mm.ControlPointSequence: 
            for thing in cp: 
                if thing.name == "Beam Limiting Device Position Sequence":
                    for t in thing: 
                        if t.RTBeamLimitingDeviceType == "MLCX":
                            t.LeafJawPositions = [sum(tup) for tup  in zip(gap_30mm, [item * i for item in increment])]
                            i+=1
        

        # APPEND A NEW CONTROL POINT 
        add_cp = copy.deepcopy(beam_30mm.ControlPointSequence[-1])
        add_cp.ControlPointIndex += 1
        for thing in add_cp: 
            if thing.name == "Beam Limiting Device Position Sequence":
                for t in thing: 
                    if t.RTBeamLimitingDeviceType == "MLCX":
                        t.LeafJawPositions = [sum(tup) for tup  in zip(gap_30mm, [item * i for item in increment])]
        beam_30mm.ControlPointSequence.append(add_cp)
        beam_30mm.NumberOfControlPoints += 1
        no_cps = len([1 for cp in beam_30mm.ControlPointSequence])
        cu_mu = [x/(no_cps-1) for x in range(0,no_cps)]
        for i, cp in enumerate(beam_30mm.ControlPointSequence):
            scientific_notation = "{:.3e}".format(cu_mu[i])
            cp.CumulativeMetersetWeight = scientific_notation

        # APPEND TO DATASET
        self.ds.BeamSequence.append(beam_30mm)
        
        
    def create_async_fields(self, beam_to_copy_beam_name: str):
        ''' 
            Shift MLCs by alternating amounts in all control points in sliding gap beams. 
        '''
        deltas = [1, 2, 3, 5, 7, 10, 20, 30]

        for i, delta in enumerate(deltas):
           
            # COPY REF BEAM 
            copy_this_beam = [beam for beam in self.beams if beam.BeamName == beam_to_copy_beam_name][0]
            new_beam = copy.deepcopy(copy_this_beam) 
            new_beam.BeamName = "aSG_"+str(delta)+"mm"
            new_beam.BeamNumber += (i+2)

            # MODIFY REF DATA
            self.fractions.NumberOfBeams += 1
            self.fractions.NumberOfFractionsPlanned += 1
            ref_beam = copy.deepcopy(self.fractions.ReferencedBeamSequence[-1])
            ref_beam.ReferencedBeamNumber += 1 
            self.fractions.ReferencedBeamSequence.append(ref_beam)

            # ADJUST MLC POSITIONS IN CONTROL POINTS 
            for cp in new_beam.ControlPointSequence: 
                for thing in cp: 
                    if thing.name == "Beam Limiting Device Position Sequence":
                        for t in thing: 
                            if t.RTBeamLimitingDeviceType == "MLCX":
                                delta_array = [x for t in zip([delta for item in range(60)], [-1*delta for item in range(60)]) for x in t]
                                current_leaf_positions = [item for item in t.LeafJawPositions]
                                t.LeafJawPositions = [sum(tup) for tup  in zip(delta_array, current_leaf_positions)]

            # APPEND TO DATASET 
            self.ds.BeamSequence.append(new_beam)

            # CREATE A COPY OF LAST ELEMENT OF PATIENT SETUP SEQUENCE 
            ps = copy.deepcopy(self.setups[-1])
            ps.PatientSetupNumber += 1 
            self.setups.value.append(ps)

    def write_new_dataset(self, f_out: str = "MODIFIED_BEAMS.dcm"):
        self.ds.save_as(path.join(self.f_root,f_out), write_like_original=False)

    def delete_varian_private_attributes(self):
        self.ds.remove_private_tags() 

a = ASyncSweepingGapField(f_name = '6XFFF_DLG_HD120.dcm')
a.delete_varian_private_attributes() 
a.write_dcm_beams_to_txt()
a.create_beam_30mm()
a.create_async_fields("20mm")
a.write_new_dataset(f_out = "6XFFF_DLG_HD120_LSt.dcm")

b = ASyncSweepingGapField(f_name = "6XFFF_DLG_HD120_LSt.dcm")
b.write_dcm_beams_to_txt()
