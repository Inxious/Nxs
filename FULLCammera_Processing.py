
import threading
from wx.lib.pubsub import pub
import wx
import ConfigParser


class FULLRotatingVolume():

    def __init__ (self, must_value):
        self.Must_Value = must_value

        try:
            self.RotateTrial_Count = int(self.RotateTrial_Count)
        except Exception as e:
            self.RotateTrial_Count = 0

        try:
            self.RotateTrial_Limit = int(self.RotateTrial_Limit)
        except Exception as e:
            self.RotateTrial_Limit = 5

        try:
            self.RotateError_Limit = int(self.RotateError_Limit)
        except Exception as e:
            self.RotateError_Limit = 3

        try:
            self.ScanMoving_Value = int(self.ScanMoving_Value)
        except Exception as e:
            self.ScanMoving_Value = 10

        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.Upper_Range = config.get('Rotate Moving Configuration', 'UpperRange')
        self.Upper_MissRange = config.get('Rotate Moving Configuration', 'UpperMissRange')
        self.Lower_Range = config.get('Rotate Moving Configuration', 'LowerRange')
        self.Lower_MissRange = config.get('Rotate Moving Configuration', 'LowerMissRange')

    def Volume_Passer(self , must_value):
        if float(must_value) < float(11):
            self.Camera_Reading_Type = "1-10"
        elif float(must_value) >= float(11):
            self.Camera_Reading_Type = "10-100"

        # SPLIT MUST VALUE
       # print  "MUST" + str(must_value)


        self.Koordinate_Volume = str(must_value).split(".")
        self.Koordinate_Upper_Volume = self.Koordinate_Volume[0]
        self.Koordinate_Lower_Volume = self.Koordinate_Volume[1]


        self.CameraDetect(1, str(must_value))

        #SET THE UPPER VOLUME FIRST
        self.FirstVolume(self.Koordinate_Upper_Volume)


        #SET THE LOWER VOLUME SECOND
        self.SecondVolume(self.Koordinate_Lower_Volume)


    def FirstVolume(self,must_value):
        # Read Upper Volume
        self.Volume_Setting = '1st'
        self.Camera_Crop = 'UPPER'
        self.CameraRead(1)
        #self.Volume_Setting = 'END'

    def SecondVolume(self,must_value):
        # Read Upper Volume
        self.Volume_Setting = '2nd'
        self.Camera_Crop = 'LOWER'
        self.CameraRead(2)
        #self.Volume_Setting = 'END'

    def InProgramFilter(self, mode , strings):
        if mode == 1: # Volume Besar
            if self.Pipete_Used == '1-10':
                numlist = [x+1 for x in range(10)]
            elif self.Pipete_Used == '10-100':
                numlist = [x for x in range(10,105,5)]
            else:
                return('FAILED')

            if strings not in numlist:
                return ('FAILED')
            else:
                return ('SUCCES')

        elif mode == 2: # Volume kecil
            if self.Pipete_Used == '1-10':
                numlist = [x for x in range(10, 105, 5)]
            elif self.Pipete_Used == '10-100':
                numlist = [x + 1 for x in range(10)]
            else:
                return('FAILED')

            if strings not in numlist:
                return ('FAILED')
            else:
                return ('SUCCES')


    def CameraCompare(self, mode, array):

        # COMPARING IMAGE RESULT FROM CAMERA
        if array[0] == 'FAILED':
            if array[1] == 'FAILED':
                if array[2] == 'FAILED':
                    if mode == 1:
                        return ("FAILED")
                    elif mode == 2:
                        return (1)
                else:
                    if mode == 1:
                        return (array[2])
                    elif mode == 2:
                        return (2)
            else:
                if mode == 1:
                    return (array[1])
                elif mode == 2:
                    return (1)
        else:
            if mode == 1:
                return (array[0])
            elif mode == 2:
                return (1)

    def CameraRead(self, mode):
        #UPPER
        if mode == 1:
            # READING VALUE NOW
            self.Camera_Crop = "UPPER"
            self.Camera_Reading = "ON"

            # WAIT CAMERA READING
            print '-- -- Wait Reading Camera -- --'
            while self.Camera_Reading == "ON":
                pass
            print '-- -- Done Reading Camera -- --'

            if self.Camera_Readed_Status == "FAILED":
                print 'stases' + self.Camera_Readed_Status
                self.RoboCalibrate("UPPER",1)
            else:
                print 'stases' + self.Camera_Readed_Status
                if self.Volume_Setting == "END":
                    self.Camera_Procedure = False
                    return
                else:
                    self.CameraDetect(2,self.Camera_Readed_Value)
                    self.GetCalibration("UPPER")
        #LOWER
        elif mode == 2:
            # READING VALUE NOW
            self.Camera_Crop = "LOWER"
            self.Camera_Reading = "ON"

            # WAIT CAMERA READING
            print '-- -- Wait Reading Camera -- --'
            while self.Camera_Reading == "ON":
                pass
            print '-- -- Done Reading Camera -- --'

            if self.Camera_Readed_Status == "FAILED":
                print 'stases' + self.Camera_Readed_Status
                self.RoboCalibrate("LOWER", self.Array_of_Truth)
            else:
                print 'stases' + self.Camera_Readed_Status
                if self.Volume_Setting == "END":
                    self.Camera_Procedure = False
                    return
                else:
                    self.CameraDetect(2,self.Camera_Readed_Value)
                    self.GetCalibration("LOWER")

        #ONLY READ WITH NO ACTION
        elif mode == 3:
            # READING VALUE NOW
            self.Camera_Reading = "ON"

            # WAIT CAMERA READING
            while self.Camera_Reading == "ON":
                pass

            if self.Camera_Readed_Status == "FAILED":
                return("FAILED")
            else:
                return("SUCCESS")

    def CameraDetect(self, mode,value):

        print '-=--=-=-=-=-=-='
        print value
        print '-=-=-=-=-=-=-=-='

        if mode == 1:
            data = value.split(".")
            if self.Pipete_Used == "10-100":
                print 'detect 11'
                self.Pipete_Upper_Value = data[0][0:1]
                self.Pipete_Lower_Value = data[0][2] + "." + data[1]

            elif self.Pipete_Used == "1-10":
                print 'detect 22'
                self.Pipete_Upper_Value = data[0]
                self.Pipete_Lower_Value = data[1]
            elif self.Pipete_Used == 'ERROR':
                pass
            print self.Pipete_Used

        elif mode == 2:
            data = value.split(".")
            if self.Pipete_Used == "10-100":
                print 'detect 1'
                self.Pipete_Upper_Value = data[0][0:1]
                self.Pipete_Lower_Value = data[0][2] + "." + data[1]

            elif self.Pipete_Used == "1-10":
                print 'detect 2'
                self.Pipete_Upper_Value = data[0]
                self.Pipete_Lower_Value = data[1]


            elif self.Pipete_Used == 'ERROR':
                pass

            print self.Pipete_Used
        elif mode == 3:
            data = value.split(".")
            if len(data[0]) == 3 and len(data[1]) == 1 and float(value) >= 10.95:
                self.Pipete_Used = "10-100"

            elif len(data[0]) <= 2 and len(data[1]) == 2 and float(value) <= 10.95:
                self.Pipete_Used = "1-10"

            elif self.Pipete_Used == 'ERROR':
                pass
            print self.Pipete_Used


    def GetCalibration(self, mode):
        print("GET CALIBRATION")
        print mode
        print self.Pipete_Used
        #SET UPPER VOLUME
        self.Pulse_Calibration = 0

        if mode == 'UPPER':

            print '---sts'
            print self.Koordinate_Upper_Volume
            print self.Pipete_Upper_Value
            print '---sts'

            if str(self.Koordinate_Upper_Volume) == str(self.Pipete_Upper_Value):
                self.Pulse_Calibration = 0
                print 'ITS THE SAME VALUE'
                x = 'ITS THE SAME VALUE'
            else:
                # 1-10 PIPET , 1st Movement
                if self.Pipete_Used == "1-10":
                    x = 'a'
                    if (float(self.Koordinate_Upper_Volume) - float(self.Pipete_Upper_Value)) != 0:
                        #ToDo = ADD Pulse Value / Number On Database
                        Range = float(self.Upper_Range) #ToDo : GET DATA RANGE / NUMBER
                        Miss_Range = float(self.Upper_MissRange) #ToDo : GET DATA RANGE MISS ON 1st Rotation / NUMBER
                        if self.R_Movement > 0:
                            Miss_Range = 0
                        else:
                            self.R_Movement += 1

                        if float(float(self.Koordinate_Upper_Volume)  - float(self.Pipete_Upper_Value)) < 0:
                            plus = 10
                        else:
                            plus = 0

                        self.Pulse_Calibration = float((((float(self.Koordinate_Upper_Volume) + plus ) - float(self.Pipete_Upper_Value)) * float(Range)) + float(Miss_Range)) * -1
                        print 'PULSE CALIBRATION ===??? ' + str(self.Pulse_Calibration)

                # 10-100 PIPET , 1st Movement
                elif self.Pipete_Used == "10-100":
                    x =  'b'
                    if (float(self.Koordinate_Upper_Volume) - float(self.Pipete_Upper_Value)) != 0:
                        # ToDo = ADD Pulse Value / Number On Database
                        Range = float(self.Upper_Range)  # ToDo : GET DATA RANGE / NUMBER
                        Miss_Range = float(self.Upper_MissRange) # ToDo : GET DATA RANGE MISS ON 1st Rotation / NUMBER
                        if self.R_Movement > 0:
                            Miss_Range = 0
                        else:
                            self.R_Movement += 1

                        if float(float(self.Koordinate_Upper_Volume)  - float(self.Pipete_Upper_Value)) < 0:
                            plus = 10
                        else:
                            plus = 0

                        self.Pulse_Calibration = float(((( float(self.Koordinate_Upper_Volume) + plus) - float(self.Pipete_Upper_Value)) * float(Range)) +  float(Miss_Range)) * -1
                        print 'PULSE CALIBRATION ===??? ' + str(self.Pulse_Calibration)

            print  x + ' ' + str(self.Pulse_Calibration)
            # ================ RUN ROTATION ====================
            if self.Pulse_Calibration != 0:
                self.RoboRotate('UPPER', self.Pulse_Calibration)
            else:
                self.Volume_Setting = '1st DONE'

            #==================================================


        # SET LOWER VOLUME
        if mode == 'LOWER':

            print '---sts'
            print self.Koordinate_Lower_Volume
            print self.Pipete_Lower_Value
            print '---sts'

            if str(self.Koordinate_Lower_Volume) == str(self.Pipete_Lower_Value):
                self.Pulse_Calibration = 0
                print 'ITS THE SAME VALUE'
                x = 'ITS THE SAME VALUE'
            else:
                # 1-10 PIPET , 1st Movement
                if self.Pipete_Used == "1-10":
                    x = 'c'
                    if (float(self.Koordinate_Lower_Volume) - float(self.Pipete_Lower_Value)) != 0:
                        # ToDo = ADD Pulse Value / Number On Database
                        Range = float(self.Lower_Range)  # ToDo : GET DATA RANGE / NUMBER
                        Miss_Range = float(self.Lower_MissRange) # ToDo : GET DATA RANGE MISS ON 1st Rotation / NUMBER

                        if float(float(self.Koordinate_Lower_Volume)  -  float(self.Pipete_Lower_Value)) < 0:
                            if self.lastrotate == 'PLUS':
                                self.R_Movement = 0
                        else:
                            if self.lastrotate == 'MINUS':
                                self.R_Movement = 0

                        if self.R_Movement > 0:
                            Miss_Range = 0
                        else:
                            self.R_Movement += 1

                        self.Pulse_Calibration = float(((((float(self.Koordinate_Lower_Volume) - float(self.Pipete_Lower_Value)) / 5) *
                                                         float(Range)) + float(Miss_Range))) * -1
                        print 'PULSE CALIBRATION ===??? ' + str(self.Pulse_Calibration)

                # 10-100 PIPET , 1st Movement
                elif self.Pipete_Used == "10-100":
                    x =  'd'
                    if (float(self.Koordinate_Lower_Volume) - float(self.Pipete_Lower_Value)) != 0:
                        # ToDo = ADD Pulse Value / Number On Database
                        Range = float(self.Lower_Range)  # ToDo : GET DATA RANGE / NUMBER
                        Miss_Range = float(self.Lower_MissRange) # ToDo : GET DATA RANGE MISS ON 1st Rotation / NUMBER


                        if float(float(self.Koordinate_Lower_Volume)  -  float(self.Pipete_Lower_Value)) < 0:
                            if self.lastrotate == 'PLUS':
                                self.R_Movement = 0
                        else:
                            if self.lastrotate == 'MINUS':
                                self.R_Movement = 0

                        if self.R_Movement > 0:
                            Miss_Range = 0
                        else:
                            self.R_Movement += 1

                        self.Pulse_Calibration = float(((((float(self.Koordinate_Lower_Volume)  -  float(self.Pipete_Lower_Value)) / 5) * 10) *
                                                        float(Range)) + float(Miss_Range)) * -1
                        print 'PULSE CALIBRATION ===???' + str(self.Pulse_Calibration)

            print  x + ' ' + str(self.Pulse_Calibration)
            # ================ RUN ROTATION ====================
            if self.Pulse_Calibration != 0:
                self.RoboRotate('LOWER', self.Pulse_Calibration)
            else:
                self.Volume_Setting = '2nd DONE'

            # ==================================================

    def RoboCalibrate(self, mode , rotate_type):
        print "ROBO CALIBRATE"
        print rotate_type

        if mode == 'UPPER':

            for i in range(self.RotateError_Limit):
                #NORMAL [NOT DETECTED AT ALL OR DETECT : ]
                if rotate_type == 1 or rotate_type == 0:
                    Pulse = float(self.RNow) + int(self.ScanMoving_Value)  # ToDo : MOVING A LITTLE
                # CROP 2 IS DETECTED [.]
                elif rotate_type == 2:
                    Pulse = float(self.RNow) - int(self.ScanMoving_Value)  # ToDo : ANOTHER MOVING A LITTLE
                # CROP 3 IS DETECTED [.]
                elif rotate_type == 3:
                    Pulse = float(self.RNow) + int(self.ScanMoving_Value)  # ToDo : ANOTHER MOVING A LITTLE

                print Pulse
                self.RoboGO(17, values=Pulse, home=0, ex="NONE", serial=1) # ToDO : Move by Pulse Variable ()

                self.UNO_Readings = "STARTED"
                self.ReadAINO(1, 1, "MOTOR_R")

                while not self.UNO_Readings == "ENDED":
                    pass

                # Read Upper Volume
                self.Camera_Crop = 'UPPER'
                self.CameraRead(3)
                Is_Success = False

                print 'camera stasss = ' + str(self.Camera_Readed_Status)
                if self.Camera_Readed_Status == "FAILED" or self.Camera_Readed_Value == 'FAILED':
                    Is_Success = False
                else:
                    Is_Success = True
                    break

            if Is_Success == True:
                self.Camera_Procedure = False
                self.CameraDetect(2, self.Camera_Readed_Value)
                self.GetCalibration("UPPER")
            elif Is_Success == False:

                #GO TO Func FrameEX on View to View Messagebox
                wx.CallAfter(pub.sendMessage, 'MessageLoad', mode=2 , ex=0)
                self.RoboWAIT(1)


                while self.option != 'DONE':
                    self.PlaySound(1)

                # Continue ON MODEL
                self.Camera_Procedure = True

        elif mode == 'LOWER':

            for i in range(self.RotateError_Limit):
                #NORMAL [NOT DETECTED AT ALL OR DETECT : ]
                if rotate_type == 1 or rotate_type == 0:
                    Pulse = float(self.RNow) + int(self.ScanMoving_Value)  # ToDo : MOVING 10 PULSE
                # CROP 2 IS DETECTED [.]
                elif rotate_type == 2:
                    Pulse = float(self.RNow) - int(self.ScanMoving_Value)  # ToDo : MOVING 10 PULSE
                # CROP 3 IS DETECTED [.]
                elif rotate_type == 3:
                    Pulse = float(self.RNow) + int(self.ScanMoving_Value)  # ToDo : MOVING 10 PULSE


                self.RoboGO(17, values=Pulse, home=0, ex="NONE", serial=1)  # ToDO : Move by Pulse Variable ()

                self.UNO_Readings = "STARTED"
                self.ReadAINO(1, 1, "MOTOR_R")

                while not self.UNO_Readings == "ENDED":
                    pass

                # Read Lower Volume
                self.Camera_Crop = 'LOWER'
                self.CameraRead(3)

                Is_Success = False

                print 'camera stasss = ' + str(self.Camera_Readed_Status)
                if self.Camera_Readed_Status == "FAILED" or self.Camera_Readed_Value == 'FAILED':
                    Is_Success = False
                else:
                    Is_Success = True
                    break

            print 'roziks ==-=-=-=' + str(self.Camera_Readed_Status)
            if Is_Success == True:
                self.Camera_Procedure = False
                self.CameraDetect(2, self.Camera_Readed_Value)
                self.GetCalibration("LOWER")
            elif Is_Success == False:

                wx.CallAfter(pub.sendMessage, 'MessageLoad', mode=2 , ex=0)
                self.RoboWAIT(1)


                while self.option != 'DONE':
                    self.PlaySound(1)

                #Continue ON MODEL
                self.Camera_Procedure = True


    def RoboRotate(self, mode, pulse_value):
        #IF Reach Limit
        if int(self.RotateTrial_Count) > int(self.RotateTrial_Limit):
            # GO TO Func FrameEX on View to View Messagebox
            wx.CallAfter(pub.sendMessage, 'MessageLoad', mode=2, ex=0)
            self.RoboWAIT(1)

            while self.option != 'DONE':
                self.PlaySound(1)

            self.RotateTrial_Count = 0
            # Continue ON MODEL
            self.Camera_Procedure = True


        if mode == "UPPER":
            Pulse = float(self.RNow) + float(pulse_value)
            self.RoboGO(17, values=Pulse, home=0, ex="NONE", serial=1)

            self.Camera_Crop = 'UPPER'

            # READING VALUE NOW
            self.CameraRead(1)
            self.RotateTrial_Count += 1


        elif mode == "LOWER":
            Pulse = float(self.RNow) + float(pulse_value)
            self.RoboGO(17, values=Pulse, home=0, ex="NONE", serial=1)

            self.Camera_Crop = 'LOWER'

            # READING VALUE NOW
            self.CameraRead(2)
            self.RotateTrial_Count += 1







        

