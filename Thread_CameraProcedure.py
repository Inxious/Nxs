
class Camera_Proceed():

    def __init__(self):
        self.Camera_Crop = ""
        self.ProcedureStart = False
        while True:
            if self.ProcedureStart == True:
                must_value = self.Must_Value
                if float(must_value) <= float(10):
                    self.Camera_Reading_Type = "1-10"
                    self.Pipete_Used = "1-10"
                elif float(must_value) > float(10):
                    self.Camera_Reading_Type = "10-100"
                    self.Pipete_Used = "10-100"
                else:
                    self.Pipete_Used = 'ERROR'


                print  'ssssaaaa' + str(self.Pipete_Used)

                # SPLIT MUST VALUE
                print  "MUST" + str(must_value)

                if self.Pipete_Used =="1-10":
                    self.Koordinate_Volume = str(must_value).split(".")
                    self.Koordinate_Upper_Volume = self.Koordinate_Volume[0]
                    self.Koordinate_Lower_Volume = self.Koordinate_Volume[1]
                elif self.Pipete_Used =="10-100":
                    self.Koordinate_Volume = str(must_value).split(".")
                    if len(self.Koordinate_Volume[0]) == 3:
                        self.Koordinate_Upper_Volume = self.Koordinate_Volume[0][0:1]
                        self.Koordinate_Lower_Volume = str(self.Koordinate_Volume[0][2]) + str('.') + str(self.Koordinate_Volume[1])
                    else:
                        self.Koordinate_Upper_Volume = self.Koordinate_Volume[0][0]
                        self.Koordinate_Lower_Volume = str(self.Koordinate_Volume[0][1]) + str('.') + str(self.Koordinate_Volume[1])

                #SET CAMERA ON START POSITION
                #rotate mode
                #1 = start
                #2 = 1st
                #3 = 2nd
                #4 = end
                #self.TableGet(2,rotatemode=1)
                #self.TableGet(2, rotatemode=2)

                #SET TO INITIALIZE POSITION
                self.GetMovement(1)
                self.GetMovement(2)

                #self.Volume_Setting = "STARTED"
                #self.CameraDetect(3, str(must_value))

                self.R_Movement = 0

                # SET THE UPPER VOLUME FIRST
                print 'SETTING FIRST VOLUME'
                self.Volume_Setting = '1st'
                self.Camera_Crop = "UPPER"
                print "============+++++===============++++++=========="
                print self.Volume_Setting
                print self.Camera_Procedure
                print self.ProcedureStart
                print "============+++++===============++++++=========="
                self.FirstVolume(self.Koordinate_Upper_Volume)


                while  self.Volume_Setting == '1st':
                    pass

                if self.Volume_Setting == "END":
                    pass
                else:
                    #self.Volume_Setting = "STARTED"
                    self.Proc_once = 0

                    #SET TO SECOND VOLUME POSITION
                    self.TableGet(2, rotatemode=3)
                    #self.GetMovement(3)

                    # SET THE LOWER VOLUME SECOND

                    # To Know what last rotate direction
                    self.lastrotate = 'PLUS'

                    print 'SETTING SECOND VOLUME'
                    self.Volume_Setting = '2nd'
                    self.Camera_Crop = "LOWER"
                    self.SecondVolume(self.Koordinate_Lower_Volume)


                    while self.Volume_Setting == '2nd':

                        pass

                #SET TO END SET POSITION
                self.TableGet(2, rotatemode=4)
                #self.GetMovement(4)

                while self.Ending_Procedure == True:
                    pass

                self.ProcedureStart = False
                if self.UNO_Boards == 1:
                    self.Proces_Step = "Finished"
                    self.UNO_Boards = ''

                elif self.DUAL_Boards == 1:
                    self.Proces_Step = "Finished"
                    self.DUAL_Boards = ''
                self.Camera_Procedure = False
