from connect import  get_current 
from numpy import arange

case = get_current("Case")
exam = get_current("Examination")


class RayCurves():
    '''
        Class container for RayStation phantom curves. 

        Properties: 
            beam_dose: 
                RayStation beam_set.FractionDose.BeamDoses object
            resolution: 
                 resolution controls the dose interpolation density along the curve in [mm]
            pois: --> list 
                RayStation PoiGeometries object list 
            beam_name: --> str 
                Combination of beam ID and beam description 
            energy: --> str 
                Nominal beam quality identifier in RayStation 
            field_size: [X, Y] [cm]
                Uses initial jaw positions 
                This may fail for beams of type not 3D-CRT 
            depths: --> list 
                Depths use pois with cm in their label. 
            cax_depths: --> list 
                As above, only the depth is the ANT-POST distance from the AXIS poi. 
            FoR: --> str 
                DICOM FoR UID from current image set.  
            ssd: --> float
                SSD [cm]
            inplane_profiles: --> list of lists
                List of interpolated inplane profiles at each depth in depths. 
            inplane_positions: --> list 
                List of positions along inplane_profile axis at which profiles
                are extracted. 
                Inplane goes from GUN to TARGET. 
            crossplane_profiles: --> list of lists 
                As inplane_profiles. 
            crossplane_positions: --> list
                As inplane_profiles. 
                Crossplane profiles go from RIGHT to LEFT.

        Methods: 
            return_field_size_for_beam 
            return_energy_for_beam
            get_dose_at_points
            get_crossplane_profiles 
            get_inplane_profiles 
            get_pdd 

        Limitations: 
            All crossplane, inplane and PDD extraction performed on initialisation. 
            Assumes certain RayStation state including: 
                Current beam_set is a 3D-CRT beam_set with calculated dose.
                POIs defining: 
                    • TARGET
                    • GUN 
                    • LEFT 
                    • RIGHT 
                    • AXIS
            Crossplane profiles go from RIGHT POI to LEFT POI. 
            Inplane profiles go from GUN to TARGET POI irresepctive of their position. 
            Profiles are taken at the depths of all POIs that have "cm" in their label. 
            PDDs are taken from the AXIS POI in the ANT POST direction. 
            No check of RayStation state before execution. 
            HINT: use descriptive field names and IDs. 
    '''

    def __init__(self, beam_dose, resolution: float = 0.05): 
        '''
        Parameters: 
            beam_dose is a RayStation beam_set.FractionDose.BeamDoses object. 
            resolution controls the dose interpolation density along the curve in [mm]  

        Curves are extracted on initialisation.  
        '''
        self.pois = case.PatientModel.StructureSets[exam.Name].PoiGeometries
        self.resolution = resolution
        self.beam_dose = beam_dose 
        self.beam_name = " ".join(
            [
                self.beam_dose.ForBeam.Name.strip(),
                self.beam_dose.ForBeam.Description.strip(),
            ]
        )

        self.energy = self.return_energy_for_beam() 
        self.ssd = self.beam_dose.ForBeam.GetSSD() * 10.0
        self.field_size = self.return_field_size_for_beam() 
        self.depths = [
            poi.Point["y"]
            for poi in self.pois 
            if "cm" in poi.OfPoi.Name
        ]
        self.cax_depths = [
            poi.Point["y"]-self.pois["AXIS"].Point["y"]
            for poi in self.pois if "cm" in poi.OfPoi.Name
        ]

        self.FoR = exam.EquipmentInfo.FrameOfReference

        self.get_crossplane_profiles() 
        self.get_inplane_profiles() 
        self.get_pdd() 

    def return_field_size_for_beam(self):
        '''
            Uses initial jaw positions to calculate field width in X and Y. 
            Likley fails for anything other than 3D-CRT beams. 
        '''
        jaws = self.beam_dose.ForBeam.InitialJawPositions
        # will only work for 3D-CRT beams. 
        return [jaws[1]-jaws[0],jaws[3]-jaws[2]]

    def return_energy_for_beam(self):
        '''
            Returns energy for FFF beam qualities of the form X.3 
            e.g 6X FFF will come across as 6.3. 
        '''
        return  str(float(self.beam_dose.ForBeam.BeamQualityId) + 0.3)

    def get_dose_at_points(self, points):
        '''
            Performs RayStation InterpolateDoseInPoints method across beam_dose object. 
        '''
        return self.beam_dose.InterpolateDoseInPoints(
        Points=points,
        PointsFrameOfReference=self.FoR
        ) 

    def get_crossplane_profiles(self): 
        '''
            Extracts crossplane LEFT-RIGHT profiles at all depths. 
        '''
        self.crossplane_positions = [x for x in 
        arange(self.pois["RIGHT"].Point["x"],self.pois["LEFT"].Point["x"], self.resolution)
        ]
        list_of_points = [
            [
                    {
                        "x": item,
                        "y": depth,
                        "z": self.pois["LEFT"].Point["z"],
                    }
                    for item in self.crossplane_positions
            ]
            for depth in self.depths 
        ]
        self.crossplane_profiles = [
            self.get_dose_at_points(points) for points in list_of_points
        ] 
    
    def get_inplane_profiles(self): 
        '''
            Extracts inplane TARGET-GUN profiles at all depths. 
        '''
        self.inplane_positions = [x for x in 
        arange(self.pois["TARGET"].Point["z"],self.pois["GUN"].Point["z"], self.resolution) 
        ]
        list_of_points = [
            [
                    {
                        "x": self.pois["GUN"].Point["x"],
                        "y": depth,
                        "z": item
                    }
                    for item in self.inplane_positions
            ]
            for depth in self.depths 
        ]
        self.inplane_profiles = [
            self.get_dose_at_points(points) for points in list_of_points
        ]


    def get_pdd(self): 
        '''
            Extracts PDD from POI labelled as AXIS in ANT-POST direction 50cm.
        '''

        self.pdd_positions = [
            a  for a in arange(self.pois["AXIS"].Point["y"],50+self.pois["AXIS"].Point["y"], self.resolution)
            ]

        points = [
             {
                        "x": self.pois["AXIS"].Point["x"],
                        "y": item,
                        "z": self.pois["AXIS"].Point["z"]
                    }
                    for item in self.pdd_positions
        ]
        self.pdd = self.get_dose_at_points(points)