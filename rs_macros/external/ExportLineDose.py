###Dott. Claudio Vecchi - Tecnologie Avanzate s.r.l.###
###Torino, Via Lungo Dora Voghera 36/A###
###E-mail: claudio.vecchi@tecnologieavanzate.com###

# PURPOSE: Script to write out dose profiles (for selected beamset) into RayStation format.
# Input coordinates in centimeters using "." as decimal point.
# Output is a .csv file and it's tested for HFS (in other patient position we should change x,y,z)
# Absolute coordinates in export as they are shown on TPS

from connect import*
import math
import os
import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Point
from System.Windows.Forms import Application, Button, Form, Label, TextBox
import System.Windows.Forms as WinForms
from System.Windows.Forms import DialogResult, FolderBrowserDialog

plan = get_current("Plan")
patient = get_current("Patient")
bs = get_current("BeamSet")

class SimpleTextBoxForm(Form):

    def __init__(self):
        self.Text = "Line dose export"

        self.Width = 550
        self.Height = 320
        self.CenterToScreen()

        self.label01 = Label()
        self.label01.Text = "X start [cm]"
        self.label01.Location = Point(25, 35)
        self.label01.Height = 25
        self.label01.Width = 80

        self.textbox01 = TextBox()
        self.textbox01.Text = "0.0"
        self.textbox01.Location = Point(25, 60)
        self.textbox01.Width = 70

        self.label05 = Label()
        self.label05.Text = "Sampling step [cm]"
        self.label05.Location = Point(250, 155)
        self.label05.Height = 25
        self.label05.Width = 100

        self.textbox05 = TextBox()
        self.textbox05.Text = "0.1"
        self.textbox05.Location = Point(250, 180)
        self.textbox05.Width = 70

        self.label02 = Label()
        self.label02.Text = "X end [cm]"
        self.label02.Location = Point(110, 35)
        self.label02.Height = 25
        self.label02.Width = 80

        self.textbox02 = TextBox()
        self.textbox02.Text = "0.0"
        self.textbox02.Location = Point(110, 60)
        self.textbox02.Width = 70

        self.label = Label()
        self.label.Text = "Y start [cm]"
        self.label.Location = Point(25, 95)
        self.label.Height = 25
        self.label.Width = 80

        self.textbox = TextBox()
        self.textbox.Text = "0.0"
        self.textbox.Location = Point(25, 120)
        self.textbox.Width = 70

        self.label03 = Label()
        self.label03.Text = "Y end [cm]"
        self.label03.Location = Point(110, 95)
        self.label03.Height = 25
        self.label03.Width = 80

        self.textbox03 = TextBox()
        self.textbox03.Text = "0.0"
        self.textbox03.Location = Point(110, 120)
        self.textbox03.Width = 70
		
        self.label1 = Label()
        self.label1.Text = "Z start [cm]"
        self.label1.Location = Point(25, 155)
        self.label1.Height = 25
        self.label1.Width = 80

        self.textbox1 = TextBox()
        self.textbox1.Text = "0.0"
        self.textbox1.Location = Point(25, 180)
        self.textbox1.Width = 70

        self.label04 = Label()
        self.label04.Text = "Z end [cm]"
        self.label04.Location = Point(110, 155)
        self.label04.Height = 25
        self.label04.Width = 80

        self.textbox04 = TextBox()
        self.textbox04.Text = "0.0"
        self.textbox04.Location = Point(110, 180)
        self.textbox04.Width = 70

        #Save button
        self.button1 = Button()
        self.button1.Text = 'Save'
        self.button1.Location = Point(25, 225)
        self.button1.Click += self.getlinedose

        #Reset button
        self.button2 = Button()
        self.button2.Text = 'Reset'
        self.button2.Location = Point(110, 225)
        self.button2.Click += self.reset


        self.label7 = Label()
        self.label7.Text = "X is the first displayed coordinates on patient images. \nZ the 2nd ones. Y the last ones. \nY coordinates are inverted automatically \n(input the same coordinates you see on patient images). \nLeave the same coordinates as start-end position if you don't want to change them."
        self.label7.Location = Point(250, 35)
        self.label7.Height = 50
        self.label7.Width = 500
		
		
        self.AcceptButton = self.button1
        self.CancelButton = self.button2

        self.Controls.Add(self.label01)
        self.Controls.Add(self.textbox01)
        self.Controls.Add(self.label1)
        self.Controls.Add(self.textbox1)
        self.Controls.Add(self.label)
        self.Controls.Add(self.textbox)
        self.Controls.Add(self.label7)
        self.Controls.Add(self.button1)
        self.Controls.Add(self.button2)
        self.Controls.Add(self.label02)
        self.Controls.Add(self.textbox02)
        self.Controls.Add(self.label03)
        self.Controls.Add(self.textbox03)
        self.Controls.Add(self.label04)
        self.Controls.Add(self.textbox04)
        self.Controls.Add(self.textbox05)
        self.Controls.Add(self.label05)
		
    def reset(self, sender, event):
        self.textbox.Text = "0.0"
        self.textbox1.Text = "0.0"
        self.textbox01.Text = "0.0"
        self.textbox02.Text = "0.0"
        self.textbox03.Text = "0.0"
        self.textbox04.Text = "0.0"
        self.textbox05.Text = "0.1"
		
    def getlinedose(self,sender,event):

        coord_x_start = self.textbox01.Text
        coord_x_start = float(coord_x_start)
        #coord_x_start = round(coord_x_start,1)

        coord_x_end = self.textbox02.Text
        coord_x_end = float(coord_x_end)
        #coord_x_end = round(coord_x_end,1)

        coord_y_start = self.textbox.Text
        coord_y_start = float(coord_y_start)
        #coord_y_start = round(coord_y_start,1)

        coord_y_end = self.textbox03.Text
        coord_y_end = float(coord_y_end)
        #coord_y_end = round(coord_y_end,1)
		
        coord_z_start = self.textbox1.Text
        coord_z_start = float(coord_z_start)
        #coord_z_start = round(coord_z_start,1)

        coord_z_end = self.textbox04.Text
        coord_z_end = float(coord_z_end)
        #coord_z_end = round(coord_z_end,1)
		
        #remember y is negative of actual # displayed in RS - check statetree to verify
        start = {'x': coord_x_start, 'y': -coord_y_start, 'z': coord_z_start} # cm
        end = {'x': coord_x_end, 'y': -coord_y_end, 'z': coord_z_end} # cm
		
        xdistance = end['x'] - start['x']
        ydistance = end['y'] - start['y']
        zdistance = end['z'] - start['z']
        
        discretization = float(self.textbox05.Text) # Set the sampling step in cm
		
        totdistance=(xdistance**2+ydistance**2+zdistance**2)**0.5
        num_of_pts = math.ceil(totdistance/discretization)

        xdiscretization=xdistance/num_of_pts
        ydiscretization=ydistance/num_of_pts
        zdiscretization=zdistance/num_of_pts

        points_list=[]
        for i in xrange(num_of_pts+1):
            points_list.append({'x': '%.3f'%(start['x']+i* xdiscretization), 'y': '%.3f'%(start['y'] + i * ydiscretization), 'z': '%.3f'%(start ['z']+i* zdiscretization) })

        dose_list = bs.FractionDose.InterpolateDoseInPoints(Points = points_list, PointsFrameOfReference=bs.FrameOfReference)

        self.dialog = FolderBrowserDialog()
        if self.dialog.ShowDialog() == DialogResult.OK:
           try:
              folder = self.dialog.SelectedPath
              check = True
           except IOError, e:
              print 'An error occurred:'

        script_folder = os.path.dirname(os.path.abspath(__file__))
        newpath = r"{0}\{1}_{2}_{3}_line_dose_X{4}_{5}_Y{6}_{7}_Z{8}_{9}.csv".format(folder,patient.Name,patient.PatientID,bs.AccurateDoseAlgorithm.DoseAlgorithm,coord_x_start,coord_x_end,coord_y_start,coord_y_end,coord_z_start,coord_z_end)

        with open(newpath, 'w') as f:
             f.write('#######################################################\n')
             try:
                f.write('#RayStationVersion:  \t{0}\n'.format(patient.ModificationInfo.SoftwareVersion))
             except:
                f.write('#TPSVersion:      \t{0}\n'.format("None"))
             f.write('#PatientName:        \t{0}\n'.format(patient.Name))
             f.write('#PatientId:          \t{0}\n'.format(patient.PatientID))
             f.write('#CoordinateSystem:   \t{0}\n'.format('IEC patient coordinate system'))
             f.write('#LineName:           \tX{0}_{1}_Y{2}_{3}_Z{4}_{5}\n'.format(coord_x_start,coord_x_end,coord_y_start,coord_y_end,coord_z_start,coord_z_end))
             f.write('#DoseName:           \t{0}\n'.format(bs.DicomPlanLabel))
             try:
                f.write('#DoseEngine:         \t{0}\n'.format(bs.AccurateDoseAlgorithm.DoseAlgorithm))
             except:
                f.write('#DoseEngine:         \t{0}\n'.format("None"))
             f.write('#TreatmentMachine:   \t{0}\n'.format(bs.MachineReference.MachineName))
             f.write('#X [cm];Y [cm];Z [cm];Dose [cGy]\n')
             for i in xrange(num_of_pts+1):
                f.write('{0:3.3f}; {1:3.3f}; {2:3.3f}; {3:3.3f}\n'.format(start['x']+i* xdiscretization,start['z'] + i * zdiscretization,-(start['y'] + i * ydiscretization), bs.FractionationPattern.NumberOfFractions * dose_list[i] ))
             f.write('#######################################################')
        #WinForms.MessageBox.Show("Done!", "Y dose profile")  #Display message at the end
        Application.ExitThread()

form = SimpleTextBoxForm()
Application.Run(form)
