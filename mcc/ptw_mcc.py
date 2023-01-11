from datetime import datetime as dt 
from os import path 

class PTW_mcc():
    '''
        PTW_mcc Class 
            - export to .mcc, ascii 
            - 1 file per profile per depth
            - adds missing attributes to PDD.mcc and PROFILE.mcc in ./template 
            - use carefully, accuracy is not guaranteed 

        Properties:
            template_path
                path to template.mcc files
            curve_type 
                input as e.g. pdd, x, y converted to... 
                .mcc PDD, CROSSPLANE_PROFILE or INPLANE_PROFILE 
            mcc
                .mcc file as a list of lines 
            f_root
                project root directory 
            f_name
                resulting .mcc file name
                Constructed from curve_type, field size and depth 
            creation_time 
                dt.now() 
                Used in .mcc attributes.  

        Methods:
            read_template_file
            write_mcc
            update_line_in_mcc
            update_data_block_in_mcc

        Known limitations: 
            - Assumes collimator and gantry at zero
            - Assumes measured in water 
            - FFF energies come in as X.3 e.g 6FFF will be represented as 6.3
            - Field Type will be IRREGULAR, this may limit some analysis options in
              MEPHYSTO 
            - Reference field: 10x10, 5cm deep, ISOCENTER 

        It is instanstiated from: 
            • RayCurves object, defined in raystation_curves.py 
            • a curve_type: str  e.g "x", "y", "pdd" 
            • measurement depth: float 
            • an energy label for PTW Software: float. 6.3 for 6X FFF etc. 
            • positions: list 
            • dose: list 
            • f_root: a path to a root directory of the following form 
                root/ 
                    mcc/
                        template/
                            PROFILE.mcc
                            PDD.mcc
                        raystation_data_out/
                    rs_macros
                    

    '''

    def __init__(
        self, beam_dose, curve_type: str, 
        depth: float, energy: float,
        positions, dose, f_root
    ):
        if "profile" in curve_type:
            self.template_path = path.join(f_root,"mcc/template","PROFILE.mcc")

            if "y" in curve_type:
                self.curve_type = "INPLANE_PROFILE"
            elif "x" in curve_type:
                self.curve_type = "CROSSPLANE_PROFILE"
            
        elif "pdd" in curve_type:
            self.curve_type = "PDD"
            self.template_path = path.join(f_root,"mcc/template","PDD.mcc") 


        self.mcc = self.read_template_file(self.template_path)
        self.creation_time = dt.now().strftime("%d-%b-%Y %H:%M:%S")
        self.f_root = f_root


        self.update_line_in_mcc(
            "SCAN_CURVETYPE",
            self.curve_type,
            2
        )

        if depth: 
            self.update_line_in_mcc(
                "SCAN_DEPTH",
                depth*10,
                2
            )
            self.f_name = beam_dose.beam_name + "_depth_" + str(round(depth)) + "_" + self.curve_type + ".mcc"
        else: 
            self.f_name = beam_dose.beam_name + "_" + self.curve_type + ".mcc"

        # -- UPDATE FIELDS IN MCC -- # 

        self.update_line_in_mcc(
            "FILE_CREATION_TIME",
            self.creation_time,
            1
            )

        self.update_line_in_mcc(
            "MEAS_DATE",
            self.creation_time,
            2
            )

        self.update_line_in_mcc(
            "LAST_MODIFIED",
            self.creation_time,
            1
        )

        self.update_line_in_mcc(
            "ENERGY",
            energy,
            2
        )

        self.update_line_in_mcc(
            "SSD",
            beam_dose.ssd,
            2
        )

        self.update_line_in_mcc(
            "FIELD_INPLANE",
            beam_dose.field_size[0]*10,
            2
        )

        self.update_line_in_mcc(
            "FIELD_CROSSPLANE",
            beam_dose.field_size[1]*10,
            2
        )

        self.update_data_block(
            positions,
            dose,
        )

    def read_template_file(self, f_path: str):
        '''
            Read the template mcc file
        '''
        with open(f_path, 'r', encoding="UTF-8") as f: 
            return f.readlines()

    def write_mcc(self):
        '''
            Write an mcc file from properties. 
        '''
        with open(path.join(self.f_root,"mcc/raystation_data_out", self.f_name), 'w', encoding="utf-8") as f:
            f.writelines(self.mcc)

    def update_line_in_mcc(self, tag: str, value, indent: int):
        '''
            Update a line in a .mcc file.
        '''
        indices = [index for index in range(len(self.mcc)) if tag in self.mcc[index]]
        for index in indices:
            self.mcc[index] = "".join(['\t' for i in range(indent)]) + tag + "=" + str(value) + "\n"

    def update_data_block(self, positions, measurements):
        '''
            Update a data block in .mcc file  
        '''
        start_index = [index for index in range(len(self.mcc)) 
        if "BEGIN_DATA" in self.mcc[index]][0]
        # only one data block per mcc for now 

        one = "{:.4e}".format(1)
        for pos, meas in zip(positions, measurements):
            start_index += 1
            pos = str(round(pos,2))
            meas = "{:.4e}".format(meas)
            line = "\t\t".join(["\t", pos, meas, one]) + "\n"
            self.mcc.insert(
                start_index,
                line
                )