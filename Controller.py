import wx
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub


import serial
import time
import threading
import multiprocessing
import ConfigParser
import sys
import os
from platform import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command


#APPEND CURR DIRECTORY TO SYSd
sys.path.append(os.getcwd())


#MODULE FILE
import Threads_Master
import Threads_Board1
import Threads_Board2
import Threads_Camera
import Thread_CameraProcedure
import View
import Model
import Frame_ManualCmd
import FULLCammera_Processing
import Frame_LogSuhu
from serialscan import serial_scan


# Implementing MainFrame
class Controller(View.View, Model.Model, FULLCammera_Processing.FULLRotatingVolume,
                 Threads_Master.ThreadsPasser, Threads_Board1.ThreadsB1, Thread_CameraProcedure.Camera_Proceed,
                 Threads_Board2.ThreadsB2, Threads_Camera.Camera, Frame_ManualCmd.Mnl_Frame,
                 Frame_LogSuhu.Frm_SaveLogSuhu):

    def __init__(self):


        #IMPORT SETTING
        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.X_TrueSpeed = config.get('Motor Configuration', 'X_Speed')
        self.Y_TrueSpeed = config.get('Motor Configuration', 'Y_Speed')

        #IMPORT SETTING
        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.X_TrueSpeed = config.get('Motor Configuration', 'X_Speed')
        self.Y_TrueSpeed = config.get('Motor Configuration', 'Y_Speed')
        self.Z_TrueSpeed = config.get('Motor Configuration', 'Z_Speed')
        self.A_TrueSpeed = config.get('Motor Configuration', 'A_Speed')
        self.B_TrueSpeed = config.get('Motor Configuration', 'B_Speed')
        self.C_TrueSpeed = config.get('Motor Configuration', 'C_Speed')
        self.R_TrueSpeed = config.get('Motor Configuration', 'R_Speed')

        self.X_TrueAccel = config.get('Motor Configuration', 'X_Accel')
        self.Y_TrueAccel = config.get('Motor Configuration', 'Y_Accel')
        self.Z_TrueAccel = config.get('Motor Configuration', 'Z_Accel')
        self.A_TrueAccel = config.get('Motor Configuration', 'A_Accel')
        self.B_TrueAccel = config.get('Motor Configuration', 'B_Accel')
        self.C_TrueAccel = config.get('Motor Configuration', 'C_Accel')
        self.R_TrueAccel = config.get('Motor Configuration', 'R_Accel')


        #SERIAL SETTING
        #Mode
        self.Serial_Mode = config.get('Serial Configuration', 'Serial_Mode')

        #COM PORT
        self.Cport_Motor = config.get('Serial Configuration', 'Motor_Port')
        self.Cport_Heater = config.get('Serial Configuration', 'Heater_Port')
        self.Cport_Camera = config.get('Serial Configuration', 'Camera_Port')

        #BAUDRATE
        self.Brate_Motor = config.get('Serial Configuration', 'Motor_Baudrate')
        self.Brate_Heater = config.get('Serial Configuration', 'Heater_Baudrate')
        self.Brate_Camera = config.get('Serial Configuration', 'Camera_Baudrate')

        #LIMIT CAMERA LOOP
        self.RotateTrial_Count = 0
        self.RotateTrial_Limit = config.get('SetPipete Configuration', 'Main_RotateLimit')
        self.RotateError_Limit = config.get('SetPipete Configuration', 'Error_RotateLimit')
        self.ScanMoving_Value = config.get('SetPipete Configuration', 'AjustingRotateValue')

        #APPLY THE SPEED
        self.Settings('Speed')

        # SCANING AVAILABLE PORT ON CLIENT
        self.PortList = serial_scan()

        # CONSTANT
        self.Starter(0)
        #SUHU
        self.SuhuCounter = 0

        #PubSub Reciever
        pub.subscribe(self.FrameLoad,'ManualLoad')
        pub.subscribe(self.FrameEx,'TimerLoad')
        pub.subscribe(self.FrameEx,'MessageLoad')
        #pub.subscribe(self.FrameLoad,'ImageFrame')
        #pub.subscribe(self.FrameLoad, 'ManualLoad')


        # THREAD CONTAINER
        self.ThreadList = []
        self.Proces_UnfinishedList = []
        self.Frame_List = {}

        #THREAD MODULE INIT
        T_Master = threading.Thread( target = Threads_Master.ThreadsPasser.__init__ , args = (self,),
                                     name = "Thread Master")
        T_B1 = threading.Thread( target = Threads_Board1.ThreadsB1.__init__ , args = (self,),
                                     name = "Thread Board 1")
        T_B2 = threading.Thread( target = Threads_Board2.ThreadsB2.__init__ , args = (self,),
                                     name = "Thread Board 2")
        T_Cam = threading.Thread(target=Threads_Camera.Camera.__init__, args=(self,),
                                name="Thread Camera")
        T_Cam_Proc = threading.Thread(target=Thread_CameraProcedure.Camera_Proceed.__init__, args=(self,),
                                 name="Thread Camera 2")

        T_Master.daemon = True
        T_B1.daemon = True
        T_B2.daemon = True
        T_Cam.daemon = True
        T_Cam_Proc.daemon = True

        T_Master.start()
        T_B1.start()
        T_B2.start()
        T_Cam.start()
        T_Cam_Proc.start()

        self.ThreadList.append(T_Master)
        self.ThreadList.append(T_B1)
        self.ThreadList.append(T_B2)
        self.ThreadList.append(T_Cam)
        self.ThreadList.append(T_Cam_Proc)

        #MODUL INIT
        Model.Model.__init__(self)
        View.View.__init__(self)

        #SPEED INIT
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

    #Apply Settingd
    #self.Settings('Speed')
    def Settings(self, mode):
        if mode == 'Speed':
            id = {'X': 6, 'Y': 4, 'Z': 1, 'A': 3, 'B': 2, 'C': 5, 'R': 17}
            for ids in id:
                if ids == 'X':
                    speeds = self.X_TrueSpeed
                    accels = self.X_TrueAccel
                if ids == 'Y':
                    speeds = self.Y_TrueSpeed
                    accels = self.Y_TrueAccel
                if ids == 'Z':
                    speeds = self.Z_TrueSpeed
                    accels = self.Z_TrueAccel
                if ids == 'A':
                    speeds = self.A_TrueSpeed
                    accels = self.A_TrueAccel
                if ids == 'B':
                    speeds = self.B_TrueSpeed
                    accels = self.B_TrueAccel
                if ids == 'C':
                    speeds = self.C_TrueSpeed
                    accels = self.C_TrueAccel
                if ids == 'R':
                    speeds = self.R_TrueSpeed
                    accels = self.R_TrueAccel

                #if speeds not in (0,'',None) and accels not in (0,'',None):
                #    self.RoboSPEED(id[ids], speeds, serial=1)
                #    self.RoboACCEL(id[ids], accels, serial=1)

                #NOT USED

    #CURRENT TIME
    def CurTime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

    #STARTER PACK ON CONTROLLER CLASS INIT
    def Starter(self, mode):
        self.XNow = str("")
        self.YNow = str("")
        self.ZNow = str("")
        self.ANow = str("")
        self.BNow = str("")
        self.CNow = str("")
        self.RNow = 0
        self.F1Now = str("")
        self.F2Now = str("")
        self.F3Now= str("")
        self.loop2 = ""
        self.MaxLimitTemp = 38
        self.MinLimitTemp = 36
        self.Camera_Connection = "OFF"
        self.ProcedureStart = False
        self.Rotataing = False
        self.SpeedChanged = False
        self.MotorIDBefore = 'None'
        self.SpeedBefore = 'None'
        self.AccelBefore = 'None'
        self.SerBefore = 'None'
        self.Proces_Selected = ''

        #Diagnostik V2
        self.GUID_Proces = ''
        self.GUID_Config = ''
        self.GUID_Motor = ''
        self.ID_Proces = ''
        self.ID_Config = ''
        self.ID_ConfigDetail = ''
        self.ID_Motor = ''

        #Suhu Record
        self.LogSuhuRt = {}

        self.X_Speed = ""
        self.Y_Speed = ""
        self.Z_Speed = ""
        self.A_Speed = ""
        self.B_Speed = ""
        self.C_Speed = ""
        self.R_Speed = ""

        self.X_Accel = ""
        self.Y_Accel = ""
        self.Z_Accel = ""
        self.A_Accel = ""
        self.B_Accel = ""
        self.C_Accel = ""
        self.R_Accel = ""


        #ORIGINAL SET SPEED
        #self.X_TrueSpeed = None
        #self.Y_TrueSpeed = None
        #self.Z_TrueSpeed = None
        #self.A_TrueSpeed = None
        #self.B_TrueSpeed = None
        #self.C_TrueSpeed = None
        #self.R_TrueSpeed = None

        # ORIGINAL SET ACCEL
        #self.X_TrueAccel = None
        #self.Y_TrueAccel = None
        #self.Z_TrueAccel = None
        #self.A_TrueAccel = None
        #self.B_TrueAccel = None
        #self.C_TrueAccel = None
        #self.R_TrueAccel = None

        #Thread STARTER
        self.Event_Status = "OFF"
        if mode == 0:
            self.Board1_Connection = "OFF"
            self.Board2_Connection = "OFF"
        elif mode == 1:
            self.Board1_Connection = "OFF"
        elif mode == 2:
            self.Board2_Connection = "OFF"


    # ========= KONEKSI ========
    def SerialConn(self, board, com, brate, timeout):

        if board == 1:
            self.Board1_Connection = "OFF"
            self.ser1 = serial.Serial()
            self.ser1.port = com
            self.ser1.baudrate = brate
            self.ser1.timeout = timeout
            if self.ser1.is_open == True:
                self.ser1.close()
            self.ser1.open()
            self.LbLog.AppendItems("BOARD 1 CONNECT >> " + str(self.ser1.port) + " , " + str(self.ser1.baudrate))
            print("GOOD")
            time.sleep(2)
            self.LblComNow1.SetLabel(self.ser1.port)
            self.LblStat1.SetLabel("CONNECTED")
            self.Starter(1)
            self.Board1_Connection = "ON"
            self.Board1_Reading = "OFF"
            self.PortList = serial_scan()
            self.FrameAction(6, serial=self.PortList, portser=1)

        elif board == 2:
            self.Board2_Connection = "OFF"
            self.ser2 = serial.Serial()
            self.ser2.port = com
            self.ser2.baudrate = brate
            self.ser2.timeout = timeout
            if self.ser2.is_open == True:
                self.ser2.close()
            self.ser2.open()
            self.LbLog.AppendItems("BOARD 2 CONNECT >> " + str(self.ser2.port) + " , " + str(self.ser2.baudrate))
            print("GOOD")
            time.sleep(2)
            self.LblComNow2.SetLabel(self.ser2.port)
            self.LblStat2.SetLabel("CONNECTED")
            self.Starter(2)
            self.Ser2_Active = True
            self.SuhuReadCount = 1

            # ADD LOG
            self.CurrentFileSuhu = self.MFCreateFile(str(self.CurTime()) + ' - ' + str(self.SuhuCounter))
            self.SuhuCounter += 1
            self.SaveLogSuhuActive = True

            self.Board2_Connection = "ON"
            self.Board2_Reading = "ON"
            self.PortList = serial_scan()
            self.FrameAction(6, serial=self.PortList, portser=2)
            self.FrameAction(8, )
            if self.Standby_Start:
                self.ActionPasser("Frame", "Temperature StandBy", )






        elif board == 3:
            self.Board3_Connection = "OFF"
            self.ser3 = serial.Serial()
            self.ser3.port = com
            self.ser3.baudrate = brate
            self.ser3.timeout = timeout
            if self.ser3.is_open == True:
                self.ser3.close()
            self.ser3.open()
            self.LbLog.AppendItems("CAMERA CONNECT >> " + str(self.ser3.port) + " , " + str(self.ser3.baudrate))
            print("GOOD")
            time.sleep(2)
            self.LblComNow3.SetLabel(self.ser3.port)
            self.LblStat3.SetLabel("CONNECTED")
            self.Starter(2)
            self.Ser3_Active = True
            self.Camera_Connection = "ON"
            self.Camera_Reading = "OFF"
            self.PortList = serial_scan()
            self.FrameAction(6, serial=self.PortList, portser=3)

    #====== CUT THE CONNECTION ========
    def SerialDisconn(self, board):

        if board == 1:
            if self.ser1.is_open == True:
                self.Board1_Connection = "OFF"
                self.Board1_Reading = "OFF"
                self.ser1.close()
                self.LbLog.AppendItems("BOARD 1 DISCONNECT >> DONE")
                self.Ser1_Active = False
                self.PortList = serial_scan()
                self.FrameAction(6, serial=self.PortList , portser=1)
                self.LblComNow1.SetLabel("-")
                self.LblStat1.SetLabel("-")

        elif board == 2:
            if self.ser2.is_open == True:
                self.ActionPasser("Frame", "Temperature StandBy Off", )
                self.Board2_Connection = "OFF"
                self.Board2_Reading = "OFF"
                if self.Cmd_SET_Temp.GetLabel() == 'STOP':
                    self.ActionPasser("Frame", "Temperature StandBy", )
                self.Ser2_Active = False
                self.SaveLogSuhuActive = False

                #Run Event
                self.Event_Types = "Action"
                self.Event_Name = "Temperature"
                self.Event_Temperature = "Stop"
                self.Event_Status = "ON"

                time.sleep(1)
                self.ser2.close()
                self.LbLog.AppendItems("BOARD 2 DISCONNECT >> DONE")
                self.PortList = serial_scan()
                self.FrameAction(6, serial=self.PortList, portser=2)
                self.LblComNow2.SetLabel("-")
                self.LblStat2.SetLabel("-")



        elif board == 3:
            if self.ser3.is_open == True:
                self.Board3_Connection = "OFF"
                self.Board3_Reading = "OFF"
                self.ser3.close()
                self.LbLog.AppendItems("CAMERA DISCONNECT >> DONE")
                self.Ser3_Active = False
                self.PortList = serial_scan()
                self.FrameAction(6, serial=self.PortList , portser=3)
                self.LblComNow3.SetLabel("-")
                self.LblStat3.SetLabel("-")

    def CSerialRecon(self,mode):
        if mode == 3:
            self.SerialDisconn(3)
            time.sleep(1)
            self.SerialConn(3, self.CmbPort3.GetValue(), self.CmbBRate3.GetValue(), 0)


    def CAutoConnect(self,mode):

        self.CmbPort1.SetValue(str(self.Cport_Motor))
        self.CmbPort2.SetValue(str(self.Cport_Heater))
        self.CmbPort3.SetValue(str(self.Cport_Camera))

        self.CmbBRate1.SetValue(str(self.Brate_Motor))
        self.CmbBRate2.SetValue(str(self.Brate_Heater))
        self.CmbBRate3.SetValue(str(self.Brate_Camera))

        if mode == 1:
            self.SerialConn(1, self.CmbPort1.GetValue(), self.CmbBRate1.GetValue(), 0)
            self.SerialConn(2, self.CmbPort2.GetValue(), self.CmbBRate2.GetValue(), 0)
            self.SerialConn(3, self.CmbPort3.GetValue(), self.CmbBRate3.GetValue(), 0)


    #===================================================================================================================
    #                                           -- --- --- ROBOT COMMAND --- --- --
    #===================================================================================================================

    # -- MOTOR RECORD SAVING --
    # Save Current Value On Variable

    def CCameraCommand(self,mode):
        #START MOTION
        if mode == 1:
            try:
                self.ser3.write('START_MOTION' + '\n\r')
            except Exception as e:
                print e

        elif mode == 2:
            try:
                self.ser3.write('STOP_MOTION' + '\n\r')
            except Exception as e:
                print e
        elif mode == 3:
            try:
                self.ser3.write('END' + '\n\r')
            except Exception as e:
                print e


    def Nows(self, mode, motorid, values):
        motor = self.GetMotor(1,motorid) # ToDo : Make func GetMotor in Model

        # -- SAVE COORDINATE RECORD
        if mode == 1:
            if motor == "MOTOR_X":
                print('GO TO =>' + ' X = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'X = ' + str(self.XNow) + '')
                self.XNow = values
            elif motor == "MOTOR_Y":
                print('GO TO =>' + ' Y = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'Y = ' + str(self.YNow) + '')
                self.YNow = values
            elif motor == "MOTOR_Z":
                print('GO TO =>' + ' Z = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'Z = ' + str(self.ZNow) + '')
                self.ZNow = values
            elif motor == "MOTOR_A":
                print('GO TO =>' + ' A = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'A = ' + str(self.ANow) + '')
                self.ANow = values
            elif motor == "MOTOR_B":
                print('GO TO =>' + ' B = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'B = ' + str(self.BNow) + '')
                self.BNow = values
            elif motor == "MOTOR_C":
                print('GO TO =>' + ' C = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'C = ' + str(self.CNow) + '')
                self.CNow = values
            elif motor == "MOTOR_R":
                print('GO TO =>' + ' R = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'R = ' + str(self.RNow) + '')
                self.RNow = values
            elif motor == "MOTOR_FLIP1":
                print('GO TO =>' + ' F1 = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'F1 = ' + str(self.F1Now) + '')
                self.F1Now = values
            elif motor == "MOTOR_FLIP2":
                print('GO TO =>' + ' F2 = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'F2 = ' + str(self.F2Now) + '')
                self.F2Now = values
            elif motor == "MOTOR_FLIP3":
                print('GO TO =>' + ' F3 = ' + str(values) + ' || ' +
                      ' FROM ' + ' || ' + 'F3 = ' + str(self.F3Now) + '')
                self.F3Now = values
            elif motor == "MOTOR_HEAT":
                if values == 1:
                    self.Lbl_MF_Temp_Status.SetLabel("ON")
                elif values == 0:
                    self.Lbl_MF_Temp_Status.SetLabel("OFF")

                self.HtNow = values
            elif motor == "MOTOR_BLOW":
                self.BlNow = values



        # -- SAVE SPEED RECORD
        elif mode == 2:
            if motor == "MOTOR_X":
                self.X_Speed = values
            elif motor == "MOTOR_Y":
                self.Y_Speed = values
            elif motor == "MOTOR_Z":
                self.Z_Speed = values
            elif motor == "MOTOR_A":
                self.A_Speed = values
            elif motor == "MOTOR_B":
                self.B_Speed = values
            elif motor == "MOTOR_C":
                self.C_Speed = values
            elif motor == "MOTOR_R":
                self.R_Speed = values

        # -- SAVE ACCEL RECORD
        elif mode == 3:
            if motor == "MOTOR_X":
                self.X_Accel = values
            elif motor == "MOTOR_Y":
                self.Y_Accel = values
            elif motor == "MOTOR_Z":
                self.Z_Accel = values
            elif motor == "MOTOR_A":
                self.A_Accel = values
            elif motor == "MOTOR_B":
                self.B_Accel = values
            elif motor == "MOTOR_C":
                self.C_Accel = values
            elif motor == "MOTOR_R":
                self.R_Accel = values

        # -- SAVE SPEED RECORD
        elif mode == 4:
            if motor == "MOTOR_X":
                self.X_TrueSpeed = values
            elif motor == "MOTOR_Y":
                self.Y_TrueSpeed = values
            elif motor == "MOTOR_Z":
                self.Z_TrueSpeed = values
            elif motor == "MOTOR_A":
                self.A_TrueSpeed = values
            elif motor == "MOTOR_B":
                self.B_TrueSpeed = values
            elif motor == "MOTOR_C":
                self.C_TrueSpeed = values
            elif motor == "MOTOR_R":
                self.R_TrueSpeed = values

        # -- SAVE ACCEL RECORD
        elif mode == 5:
            if motor == "MOTOR_X":
                self.X_TrueAccel = values
            elif motor == "MOTOR_Y":
                self.Y_TrueAccel = values
            elif motor == "MOTOR_Z":
                self.Z_TrueAccel = values
            elif motor == "MOTOR_A":
                self.A_TrueAccel = values
            elif motor == "MOTOR_B":
                self.B_TrueAccel = values
            elif motor == "MOTOR_C":
                self.C_TrueAccel = values
            elif motor == "MOTOR_R":
                self.R_TrueAccel = values

    def CurrSpeedSET(self,mode,motor):
        if mode == 1:
            if motor == "MOTOR_X":
                return self.X_Speed
            elif motor == "MOTOR_Y":
                return self.Y_Speed
            elif motor == "MOTOR_Z":
                return self.Z_Speed
            elif motor == "MOTOR_A":
                return self.A_Speed
            elif motor == "MOTOR_B":
                return self.B_Speed
            elif motor == "MOTOR_C":
                return self.C_Speed
            elif motor == "MOTOR_R":
                return self.R_Speed

        # -- SAVE ACCEL RECORD
        elif mode == 2:
            if motor == "MOTOR_X":
                return self.X_Accel
            elif motor == "MOTOR_Y":
                return self.Y_Accel
            elif motor == "MOTOR_Z":
                return self.Z_Accel
            elif motor == "MOTOR_A":
                return self.A_Accel
            elif motor == "MOTOR_B":
                return self.B_Accel
            elif motor == "MOTOR_C":
                return self.C_Accel
            elif motor == "MOTOR_R":
                return self.R_Accel

    def GETNows(self, mode, motorid):
        motor = self.GetMotor(1,motorid) # ToDo : Make func GetMotor in Model

        if motor == "MOTOR_X":
            if mode == 1:
                return(self.X_Speed)
            elif mode == 2:
                return (self.XNow)
            elif mode == 3:
                return (self.X_Accel)
            elif mode == 4:
                return (self.X_TrueSpeed)
            elif mode == 5:
                return (self.X_TrueAccel)
            else:
                return (0)

        elif motor == "MOTOR_Y":
            if mode == 1:
                return (self.Y_Speed)
            elif mode == 2:
                return (self.YNow)
            elif mode == 3:
                return (self.Y_Accel)
            elif mode == 4:
                return (self.Y_TrueSpeed)
            elif mode == 5:
                return (self.Y_TrueAccel)
            else:
                return (0)

        elif motor == "MOTOR_Z":
            if mode == 1:
                return (self.Z_Speed)
            elif mode == 2:
                return (self.ZNow)
            elif mode == 3:
                return (self.Z_Accel)
            elif mode == 4:
                return (self.Z_TrueSpeed)
            elif mode == 5:
                return (self.Z_TrueAccel)
            else:
                return (0)

        elif motor == "MOTOR_A":
            if mode == 1:
                return (self.A_Speed)
            elif mode == 2:
                return (self.ANow)
            elif mode == 3:
                return (self.A_Accel)
            elif mode == 4:
                return (self.A_TrueSpeed)
            elif mode == 5:
                return (self.A_TrueAccel)
            else:
                return (0)

        elif motor == "MOTOR_B":
            if mode == 1:
                return (self.B_Speed)
            elif mode == 2:
                return (self.BNow)
            elif mode == 3:
                return (self.B_Accel)
            elif mode == 4:
                return (self.B_TrueSpeed)
            elif mode == 5:
                return (self.B_TrueAccel)
            else:
                return (0)

        elif motor == "MOTOR_C":
            if mode == 1:
                return (self.C_Speed)
            elif mode == 2:
                return (self.CNow)
            elif mode == 3:
                return (self.C_Accel)
            elif mode == 4:
                return (self.C_TrueSpeed)
            elif mode == 5:
                return (self.C_TrueAccel)
            else:
                return (0)

        elif motor == "MOTOR_R":
            if mode == 1:
                return (self.R_Speed)
            elif mode == 2:
                return (self.RNow)
            elif mode == 3:
                return (self.R_Accel)
            elif mode == 4:
                return (self.R_TrueSpeed)
            elif mode == 5:
                return (self.R_TrueAccel)
            else:
                return (0)

        else:
            return("NONE")
        #elif motor == "MOTOR_FLIP1":
        #elif motor == "MOTOR_FLIP2":
        #elif motor == "MOTOR_FLIP3":
        #elif motor == "MOTOR_HEAT":
        #elif motor == "MOTOR_BLOW":

    def RoboHEAT(self, mode):
        if mode == 0:
            print(self.ser2.is_open)
            data = (r'NEXUS=HEATER_OFF#')
            self.ser2.write(data + '~$' + '\r\n')
            print('HEATER OFF')
            self.Lbl_MF_Temp_Status.SetLabel('HEATER OFF')
            self.suhus = "off"

        elif mode == 1:
            print(self.ser2.is_open)
            data = (r'NEXUS=HEATER_ON#')
            self.ser2.write(data + '~$' + '\r\n')
            print('HEATER ON')
            self.Lbl_MF_Temp_Status.SetLabel('HEATER ON')
            self.suhus = "on"

    # -- MOTOR MOVEMENT COMMAND --
    def RoboGO(self, motorid, **kwargs):

        if self.GETNows(2,motorid) in (0,None,float(0),""):
            self.Nows(1,motorid,values=0)

        #PASS THE SAME KOOR MOVEMENT

        check = True

        if self.GETNows(2,motorid) in ("NONE",None):
            check = False

        if check == True:
            if float(self.GETNows(2,motorid)) == float(kwargs['values']) and kwargs['home'] == 0:
                self.Nows(1, motorid, values=float(kwargs['values']))
                self.LbLog.AppendItems("PASS >> " + self.GetMotor(1,motorid) + " [ALREADY ON POSITION] ")
                self.lastcommand =  (r'NEXUS=' + self.MoveCommand(motorid) + str(kwargs['values']))
                self.lastflag = self.GetMotor(7, motorid)
                return("DONE")
        elif check == False:
            pass


        if kwargs['home'] == 0:
            if kwargs['ex'] == "HEAT" or kwargs['ex'] == "BLOW":
                final_value = 0
                #if int(kwargs['values']) == 0:
                #    data = (r'NEXUS=' + self.HomeCommand(motorid))
                if int(kwargs['values']) == 1:
                    data = (r'NEXUS=' + self.MoveCommand(motorid))
            else:
                print kwargs['values']
                final_value = float(kwargs['values']) + float(self.GetMotor(6, motorid))
                data = (r'NEXUS=' + str(self.MoveCommand(motorid)) + str(final_value))

            #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
            self.LogView(2, board=kwargs['serial'], line=data)

            data = (data + '~$' + '\n')
            data = data.encode()
            if kwargs['serial'] == 1:
                self.ser1.write(data + '~$' + '\n')
            elif kwargs['serial'] == 2:
                self.ser2.write(data + '~$' + '\n')

            if kwargs['ex'] == "HEAT":
                self.Lbl_MF_Temp_Status.SetLabel("ON")

            self.Nows(1, motorid,final_value)

        elif kwargs['home'] == 1:

            if kwargs['ex'] == "HEAT" or kwargs['ex'] == "BLOW":
                data = (r'NEXUS=' + self.HomeCommand(motorid))
            else:
                final_value = float(kwargs['values']) + int(self.GetMotor(6, motorid))
                data = (r'NEXUS=' + self.HomeCommand(motorid)) #+ str(final_value))

            #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
            self.LogView(2, board=kwargs['serial'], line=data)

            data = (data + '~$' + '\n')
            data = data.encode()
            if kwargs['serial'] == 1:
                self.ser1.write(data)
            elif kwargs['serial'] == 2:
                self.ser2.write(data)


            if kwargs['ex'] == "HEAT":
                self.Lbl_MF_Temp_Status.SetLabel("OFF")

            self.Nows(1, motorid, 0)

        try:
            data
        except Exception as e:
            pass
        else:
            self.lastcommand = data

        print 'KKKKKKKKKKKKKKKKKKKKKKKKKKKKK ' + str(kwargs['serial']) + ' ' + str(data)

    #-- MOTOR SPEED COMMAND --
    def RoboSPEED(self, motorid, speed, **kwargs):

        if self.GETNows(1,motorid) == speed:
            return

        data = (r'NEXUS=' + str(self.SpeedCommand(motorid)) + str(speed))
        print data
        #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
        self.LogView(2, board=kwargs['serial'], line=data)

        if kwargs['serial'] == 1:
            self.ser1.write(data + '~$' + '\r\n')
        elif kwargs['serial'] == 2:
            self.ser2.write(data + '~$' + '\r\n')

        self.Nows(2, motorid, speed)

    # -- MOTOR ACCELERATION COMMAND --
    def RoboACCEL(self, motorid, accel, **kwargs):
        if self.GETNows(1,motorid) == accel:
            return

        data = (r'NEXUS=' + str(self.AccelCommand(motorid)) + str(accel))
        print data
        #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
        self.LogView(2, board=kwargs['serial'], line=data)

        if kwargs['serial'] == 1:
            self.ser1.write(data + '~$' + '\r\n')
        elif kwargs['serial'] == 2:
            self.ser2.write(data + '~$' + '\r\n')

        self.Nows(3, motorid, accel)

    # -- MOTOR WAITING COMMAND --
    def RoboWAIT(self, timevalue):
        time.sleep(timevalue)
        print timevalue

    def RoboVolumes(self, must_value):
        FULLCammera_Processing.FULLRotatingVolume.__init__(self,must_value)

    # -- MOTOR MANUAL COMMAND --
    def ManualCmd(self, ser, command):

        print ser
        data = command.encode()
        print command

        if int(ser) == 1:
            self.ser1.write(data  + '\r\n')
        elif int(ser) == 2:
            self.ser2.write(data  + '\r\n')
        elif int(ser) == 3:
            self.ser3.write(data  + '\r\n')
        self.LbLog.AppendItems("COMMAND >> " + str(data) )
    #===================================================================================================================
    #===================================================================================================================

    # ANTI BACKLASH FOR MOTOR
    #============================
    def AntiBacklash(self, mode, koor, koorbefore, motor, lash):
        if mode == 1:
            pass

            #print ("EXECUTING ANTIBACKLASH")
            #koor += self.Offset(1, motor)

            #if koorbefore == "":
            #    koorbefore = 0

            #if int(koor) >= 500 and koorbefore >= 500 and koor < koorbefore:
                #if motor == "X":
                   # antilash = int(koor) - int(lash)
                    #if self.RoboGOX(antilash, 0, 0) == "DONE":
                    #    return
                    #if self.ReadAINO(1, 1, "X") == "DONE":
                #pass
                #return

                #elif motor == "Y":
                    #antilash = int(koor) - int(lash)
                    #if self.RoboGOY(antilash, 0, 0) == "DONE":
                    #    return
                    #if self.ReadAINO(1, 1, "Y") == "DONE":
                    #    return

    def NFS(self,speed,accel):
        listmot = ['A']
        for motor in listmot:
            time.sleep(0.5)
            self.RoboSPEED(motor,speed)
            self.RoboACCEL(motor,accel)


    #===================================================================================================================
    #                                       -- --- --- MOTOR ON OFF AND EXTRA--- --- --
    #===================================================================================================================

    # -- HEATER --
    #def RoboHEAT(self, mode):

        #if mode == 0:
            #data = (self.HomeCommand(motorid))
            #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
            #self.ser2.write(data + '~$' + '\r\n')
            #print('HEATER OFF')
            #self.Lbl_MF_Temp_Status.SetLabel("OFF")

        #elif mode == 1:
            #data = (self.MoveCommand(motorid))
            #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
            #self.ser2.write(data + '~$' + '\r\n')
            #print('HEATER ON')
            #self.Lbl_MF_Temp_Status.SetLabel("ON")


    #===================================================================================================================
    #                                    NOT USED
    #===================================================================================================================
    def RoboONOFF(self, mode, stat):
        if mode == 1:
            if stat == "OFF":
                data = (r'MOVE_F1#F1=90')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=1, line=data)
                self.ser1.write(data + '~$' + '\r\n')
                print('FLIP 1 ON')

            elif stat == "ON":
                data = (r'MOVE_F1#F1=0')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=1, line=data)
                self.ser1.write(data + '~$' + '\r\n')
                print('FLIP 1 OFF')

        elif mode == 2:
            if stat == "OFF":
                data = (r'MOVE_F2#F2=#0')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=1, line=data)
                self.ser1.write(data + '~$' + '\r\n')
                print('FLIP 2 ON')

            elif stat == "ON":
                data = (r'MOVE_F2#F2=180')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=1, line=data)
                self.ser1.write(data + '~$' + '\r\n')
                print('FLIP 2 OFF')

#        elif mode == 3:

        elif mode == 4:
            if stat == "OFF":
                data = (r'HEATER_ON#')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=2, line=data)
                self.ser2.write(data + '~$' + '\r\n')
                print('HEATER ON')

            elif stat == "ON":
                data = (r'HEATER_OFF#')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=2, line=data)
                self.ser2.write(data + '~$' + '\r\n')
                print('HEATER OFF')

        elif mode == 5:
            if stat == "OFF":
                data = (r'MOVE_F3#F3=')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=1, line=data)
                self.ser1.write(data + '~$' + '\r\n')
                print('FLIP3 ON')

            elif stat == "ON":
                data = (r'MOVE_F3#F3=')
                #self.LbLog.AppendItems("COMMAND >> " + str(data) + '~$')
                self.LogView(2, board=1, line=data)
                self.ser1.write(data + '~$' + '\r\n')
                print('FLIP3 OFF')

    #===================================================================================================================
    #                                           END OF NOT USED
    #===================================================================================================================

    #-- PANEL TEMPERATURE --
    def GOON(self, mode):
        if mode == 3:
            if self.Cmd_MF_Temp_Standby.GetLabel() == "STANDBY":
                self.StandbyTemp = True
                self.LimitTemp = 37
                self.TimerTemp = 0
                self.suhus = ""
                self.Cmd_MF_Temp_Standby.SetLabel("STOP")
            elif self.Cmd_MF_Temp_Standby.GetLabel() == "STOP":
                self.STOPIT(3)

    #-- STOPING STANDBY THREAD --
    def STOPIT(self, mode):
        if mode == 3:
            self.StandbyTemp = False
            self.suhus = ""
            self.RoboHEAT(0)
            self.Cmd_MF_Temp_Standby.SetLabel("STANDBY")

    #-- READING FROM ARDUINO FOR END FLAG OF MOVEMENT --
    def ReadAINO(self, mode, ser, motorname):
        print("READAINO=======================")
        print ser
        print self.Board1_Connection
        print self.Board1_Reading
        motorid = self.GetMotor(12,motorname)

        if mode == 1:
            FLAG = self.GetMotor(7, motorid)
            self.lastflag = str(FLAG)
            print("READAINO======================= 1")
            print FLAG
            self.timesoon = self.CurTime()
            if ser == 1:
                self.Board1_Reading_Flag = FLAG
                self.Board1_Reading = "ON"
            elif ser == 2:
                self.Board2_Reading_Flag = FLAG
                self.Board2_Reading = "ON"

        elif mode == 2:
            FLAG = self.GetMotor(8, motorid)
            self.lastflag = str(FLAG)
            print("READAINO======================= 2")
            print FLAG
            self.timesoon = self.CurTime()
            if ser == 1:
                self.Board1_Reading_Flag = FLAG
                self.Board1_Reading = "ON"
            elif ser == 2:
                self.Board2_Reading_Flag = FLAG
                self.Board2_Reading = "ON"

    # -- VIEWING LOG MACHINE ON ListBox --
    def LogView(self, mode, **kwargs):
        if mode == 1: #ARDUINO
            if kwargs["board"] == 1:
                self.LbLog.AppendItems("Board 1 >> "+ str(kwargs["line"]))
                self.LbLog.SetSelection(int(self.LbLog.GetCount()) - 1)
            elif kwargs["board"] == 2:
                self.LbLog.AppendItems("Board 2 >> "+ str(kwargs["line"]))
                self.LbLog.SetSelection(int(self.LbLog.GetCount()) - 1)
            elif kwargs["board"] == 3:
                self.LbLog.AppendItems("Camera  >> "+ str(kwargs["line"]))
                self.LbLog.SetSelection(int(self.LbLog.GetCount()) - 1)

        #COMMAND
        elif mode == 2:
            if kwargs["board"] == 1:
                self.LbLog.AppendItems("SEND TO Board 1 >> "+ str(kwargs["line"]))
                self.LbLog.SetSelection(int(self.LbLog.GetCount()) - 1)
            elif kwargs["board"] == 2:
                self.LbLog.AppendItems("SEND TO Board 2 >> "+ str(kwargs["line"]))
                self.LbLog.SetSelection(int(self.LbLog.GetCount()) - 1)
            elif kwargs["board"] == 3:
                self.LbLog.AppendItems("SEND TO Board 3 >> "+ str(kwargs["line"]))
                self.LbLog.SetSelection(int(self.LbLog.GetCount()) - 1)

    # -- PROCES INIT ON DIFFERENT THREAD / PROCES --
    def GenerateProces(self, mode, func, para, **kwargs):
        if mode == 1:  # Multiprocessing
            return (multiprocessing.Process(target=func, args=para))
        elif mode == 2:  # Threading args
            return (threading.Thread(target=func, args=para))
        elif mode == 4: # Threading kwargs
            para2 = kwargs["kwarg"]
            para3 = kwargs['kwarg2']
            return (threading.Thread(target=func, args=para, kwargs={para2:para3}))
        elif mode == 3:
            te = threading.Thread(target=func, args=para)
            te.daemon = True
            te.start()

    def ClosingApp(self, event):
        if self.__close_callback__:
            self.__close_callback__()

    def CFormatSuhu(self, suhu):
        self.BackLenght_Suhu = 2
        self.Splitter_Suhu = '.'
        try:
            realsuhu = suhu
            suhu = str(suhu).split(self.Splitter_Suhu)
            if len(suhu) != 2:
                raise Exception
        except Exception as e:
            suhu = None
            return (suhu)
        else:
            if len(suhu[1]) > self.BackLenght_Suhu:
                suhu1 = suhu[1][0:self.BackLenght_Suhu]
            elif len(suhu[1]) < self.BackLenght_Suhu:
                suhu1 = str('0' * self.BackLenght_Suhu)
            else:
                return (realsuhu)

        result = str(suhu[0]) + str(suhu1)
        return (result)

    def CPingIp(self, host):

        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Ping command count option as function of OS
        param = '-n' if system_name().lower() == 'windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        # Pinging
        return system_call(command) == 0


