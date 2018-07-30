import pyodbc
import wx
import time
import ConfigParser
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import pub
from msvcrt import getch


class Model(object):

    def __init__(self):

        #LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.Trusted = config.get('Database Configuration', 'Trusted')
        print self.Trusted
        self.Driver = config.get('Database Configuration', 'Driver')
        self.Server = config.get('Database Configuration', 'Server')
        self.Database = config.get('Database Configuration', 'Database')
        self.Uid = config.get('Database Configuration', 'Uid')
        self.Pwd = config.get('Database Configuration', 'Pwd')

        if self.Trusted == "yes":
            self.DBConnect(2,self.Driver,self.Server,self.Database)
        elif self.Trusted == "no":
            self.DBConnect(1,self.Driver, self.Server, self.Database, uid=self.Uid, pwd=self.Pwd)

    def sleep(self,times):
        time.sleep(1)


    def DBConnect(self,mode,driver,server,database,**kwargs):
        if mode == 1:
            try:
                self.Conn = pyodbc.connect(r"Driver={"+str(driver)+"};"+
                                           r"Server="+str(server)+";"+
                                           r"Database="+str(database)+";"+
                                           r"uid="+str(kwargs["uid"])+";"+
                                           r"pwd="+str(kwargs["pwd"]))
            except Exception:
                try:
                    self.Conn = pyodbc.connect(r"Driver={"+str(driver)+"};"+
                                               r"Server="+str(server)+";"+
                                               r"Database="+str(database)+";"+
                                               r"uid="+str(kwargs["uid"])+";"+
                                               r"pwd="+str(kwargs["pwd"]))
                except Exception:
                    print("KONEKSI GAGAL")
        elif mode == 2:
            try:
                self.Conn = pyodbc.connect(r"Driver={"+str(driver)+"};"+
                                           r"Server="+str(server)+";"+
                                           r"Database="+str(database)+";"+
                                           r"Trusted_Connection=yes")
            except Exception:
                try:
                    self.Conn = pyodbc.connect(r"Driver={"+str(driver)+"};"+
                                               r"Server="+str(server)+";"+
                                               r"Database="+str(database)+";"+
                                               r"Trusted_Connection=yes")
                except Exception:
                    print("KONEKSI GAGAL")

        self.oConn = self.Conn.cursor()


    def Transaction(self, date):

        sSQL = ("SELECT * "+
                "FROM M_TransHeader "+
                "WHERE ") #ON PROGRESS
        try:
            self.oConn.execute(sSQL)
            self.Conn.commit()
        except Exception:
            print ("QUERY GAGAL")

    def TableGet(self,mode,**kwargs):

        if mode == 1: #CONFIG
            sSQL = (''' EXEC SP_Nxs_GetConfiguration 1, ?''' )


            Value = [str(kwargs["act"])]
            print Value
            data = self.oConn.execute(sSQL,Value)
            data = data.fetchall()
            self.Config_Data = []
            self.Config_Data.append([ x[0] for x in data ])#HeaderID
            self.Config_Data.append([ x[1] for x in data ])#list
            self.Config_Data.append([ x[2] for x in data ])#motor
            self.Config_Data.append([ x[3] for x in data ])#sumbu
            self.Config_Data.append([ x[4] for x in data ])#time
            self.Config_Data.append([ x[5] for x in data ])#speed
            self.Config_Data.append([ x[6] for x in data ])#Orientasi
            self.Config_Data.append([ x[7] for x in data ])#SideBySide
            self.Config_Data.append([ x[8] for x in data ])#koor
            self.Config_Data.append([x[9] for x in data])  # detail ID
            self.PrepareMovement(1, self.Config_Data, str(kwargs["act"]))

        elif mode == 2:  # SETTING PIPETE
            sSQL = (''' EXEC SP_Nxs_GetSetRotation ?''')

            Value = [str(kwargs["rotatemode"])]
            print Value
            data = self.oConn.execute(sSQL, Value)
            data = data.fetchall()
            self.Config_Data = []
            self.Config_Data.append([x[0] for x in data])  # HeaderID
            self.Config_Data.append([x[1] for x in data])  # list
            self.Config_Data.append([x[2] for x in data])  # motor
            self.Config_Data.append([x[3] for x in data])  # sumbu
            self.Config_Data.append([x[4] for x in data])  # time
            self.Config_Data.append([x[5] for x in data])  # speed
            self.Config_Data.append([x[6] for x in data])  # Orientasi
            self.Config_Data.append([x[7] for x in data])  # SideBySide
            self.Config_Data.append([x[8] for x in data])  # koor
            self.Config_Data.append([x[10] for x in data])  # detail ID
            config = [x[9] for x in data]
            config = config[0]
            self.PrepareMovement(1, self.Config_Data, config)

    def PrepareMovement(self, mode, data, types ):
        #IF IT WAS ONLY CONFIG
        if mode == 1:
            # // GUID MOTOR [ FOR M_LOG ]
            guid_config = self.MDiagnostikNexus(2)
            self.ID_Config = data[0][0]
            self.ListingMotors(data, len(data[1]), types, guid_config = guid_config)

        #IF IT WAS WHOLE PROCES
        elif mode == 2:
            self.ListingConfig(data, len(data[1]), types)


    def ListingConfig(self, data, lenght, actionname):
        for lis in range(lenght):
            config = data[2][lis]
            sSQL = (""" EXEC  SP_Nxs_GetConfiguration 2, ? """)
            Values = [int(config)]
            aksi = self.oConn.execute(sSQL,Values)
            aksi = aksi.fetchall()
            hasil = aksi[0]
            hasil2 = hasil[0]
            hasil2 = hasil2.encode()

            self.TableGet(1, act = hasil2)
            
    def ListingMotors(self, data, lenght, config , **kwargs):

        self.firstorient = data[5][0]
        self.firstsumbu = data[3][0]
        self.lastsumbu = ""
        self.moves = ""

        # GUID PROCESS
        guid_config = kwargs['guid_config']

        #LISTING MOTOR IN ARRAY
        #----------------------
        for lis in range(lenght):

            sumbu = data[3][lis]
            #koor = data[7][lis]
            koor = data[8][lis]
            orientasi = data[6][lis]
            motorname = data[2][lis]
            speedid = data[5][lis]
            time = data[4][lis]
            detail_id = data[9][lis]

            # // GUID MOTOR [ FOR M_LOG ]
            guid_motor = self.MDiagnostikNexus(2)


            MotorID = self.GetMotor(12, motorname)
            serial = self.GetBoard(3,self.GetMotor(3,MotorID))

            #SETTING SPEED IF SPEEDLIST NOT NONE
            if self.SpeedChanged == True:
                print 'speed rollback'

                self.SpeedBefore = self.GETNows(4,self.MotorIDBefore)
                self.AccelBefore = self.GETNows(5,self.MotorIDBefore)

                print '--- roll ---'
                print self.SpeedBefore
                print self.AccelBefore
                print '--- roll ---'

                if (self.SpeedBefore in (None,"")) == True or (self.AccelBefore in (None,"")) == True:
                    pass
                else:
                    self.RoboSPEED(self.MotorIDBefore, self.SpeedBefore, serial=self.SerBefore)
                    self.RoboACCEL(self.MotorIDBefore, self.AccelBefore, serial=self.SerBefore)
                    self.SpeedChanged = False

            if speedid != None or (bool(speedid) != 0) != False:
                print 'change speed ' + str(speedid)
                if (int(speedid) in ([i+1 for i in range(20)])) == True:
                    speed = self.GetSpeedSet(1,speedid)
                    accel = self.GetSpeedSet(2,speedid)

                    if speed == None or accel == None:
                        pass
                    else:
                        if speed > 20:
                            speed = 20
                        if accel > 20:
                            accel = speed - 1

                    SpeedNows = self.GETNows(1, MotorID)
                    AccelNows = self.GETNows(3, MotorID)

                    ser = serial
                    if speed != SpeedNows:
                        self.RoboSPEED(MotorID,speed,serial=ser)
                        if accel != AccelNows:
                            if accel > speed:
                                accel = int(speed) - 1
                                self.RoboACCEL(MotorID,accel,serial=ser)
                        else:
                            if accel > speed:
                                accel = int(speed) - 1
                                self.RoboACCEL(MotorID, accel, serial=ser)

                        self.RoboWAIT(1)
                        self.MotorIDBefore = MotorID
                        self.SerBefore = ser
                        self.SpeedChanged = True


            if lis >= 1:
                #BEDA SUMBU
                self.laststart = self.sumbustart
                if sumbu != self.lastsumbu:
                    self.sumbustart = self.CurTime()
                    self.LogRecord( sumbu, (lis+1), motorname, orientasi, config, 1, guid_proses = self.GUID_Proces, guid_motor = self.GUID_Motor, guid_config = self.GUID_Config )
                    self.lastsumbu = sumbu


                if True:
                    #Wait Proses
                    #-----------------------------------------------
                    if self.moves == "UNO":
                        if self.Not_Moving == False:
                            if self.Home_Moving == True:
                                modes = 2
                            else:
                                modes = 1
                            self.ReadAINO(modes,self.lastserial,self.lastmotor)
                            self.UNO_Readings = "STARTED"

                            while not self.UNO_Readings == "ENDED":
                                pass
                        else:
                            self.timesoon = self.CurTime()
                            self.timedone = self.CurTime()
                    #-----------------------------------------------

                    #Save Proces
                    #------------------------------------------------
                        self.LogRecord( self.lastsumbu, self.lastlist ,
                                        self.lastmotor, self.lastorientasi,
                                        self.lastconfig, 2,id_proses = self.ID_Proces, id_config = self.ID_Config,id_configdetail = self.ID_ConfigDetail,
                                        id_motor = self.ID_Motor, guid_proses = self.GUID_Proces, guid_motor = self.GUID_Motor, guid_config = self.GUID_Config )
                    #------------------------------------------------


                    #Motor_R moving
                    # ROTATING MOVEMENT
                    if motorname == "MOTOR_R":
                        # if self.Rotataing == True:
                        #self.timesoon = self.CurTime()
                        volumes = self.GetKoor(3, koor, motorname)
                        self.Koordinat_IS = float(volumes)
                        self.RoboVolumes(volumes)
                        #self.timedone = self.CurTime()
                        #self.laststart = self.sumbustart
                        self.Proc_once = 0
                        self.Camera_Procedure = False

                        # DATA FOR Record
                        self.sumbu_rotate = self.firstsumbu
                        self.laststart_rotate = self.sumbustart
                        self.timesoon_rotate = self.self.CurTime()
                        self.motor_rotate = motorname

                        self.ProcedureStart = True
                        self.ID_Motor = MotorID
                        self.ID_ConfigDetail = detail_id
                        self.Ending_Procedure = False
                        #self.sumbu_rotate = sumbu

                        while self.ProcedureStart == True:
                            if self.Camera_Procedure == True and self.Proc_once == 0:
                                #Load OneImage Frame
                                wx.CallAfter(pub.sendMessage, 'ImageFrame', mode=3)

                                #Load ManualFrane
                                wx.CallAfter(pub.sendMessage, 'ManualLoad', mode=3)

                                #for running just once
                                self.Proc_once += 1

                                #Wait Proces Manual Camera while Confirm Button not Pressed on Frame ManualCamera
                                print '--- -- waiting confirm -- ---'
                                while self.Camera_Procedure == True:
                                    #KEYPRESS FUNCTION
                                    #key = ord(getch())
                                    #if key == 75:  # LEFT
                                    #    self.CamPulseGO(2)
                                    #elif key == 77:  # RIGHT
                                    #    self.CamPulseGO(1)
                                    pass
                                print '--- -- Done confirm -- ---'

                                self.Volume_Setting = "END"
                                self.Ending_Procedure = False

                        #Save Record
                        self.LogRecord(self.sumbu_rotate, 0, 0, 0, config, 0, guid_proses=self.GUID_Proces,
                                       guid_motor=self.GUID_Motor, guid_config=self.GUID_Config)
                        self.LogRecord(self.sumbu_rotate, lis + 1,
                                       self.motor_rotate, 'R', config, 2, id_proses=self.ID_Proces, id_config=self.ID_Config,
                                       id_configdetail=self.ID_ConfigDetail,
                                       id_motor=self.ID_Motor, guid_proses=self.GUID_Proces, guid_motor=self.GUID_Motor,
                                       guid_config=self.GUID_Config)

                        self.Rotating = False
                        self.Proces_Step = "Finished"
                        print "======++++++=======+++++"
                        print "FINISHED"
                        print "======++++++=======+++++"
                        self.Not_Moving = True
                        pass



                    #New Proses
                    #-------------------------------------------------
                    self.moves = "UNO"
                    self.UNO_Boards = serial

                    self.timesoon = self.CurTime()

                    if self.GenerateMOVE( motorname, koor, serial, time ) == "DONE":
                        self.timesoon = self.CurTime()
                        self.timedone = self.CurTime()
                        self.Not_Moving = True
                    #elif self.GenerateMOVE( motorname, koor, serial, time ) == "NONE":
                    #    self.Not_Moving = True
                    else:
                        self.Not_Moving = False

                    #-------------------------------------------------

            else:
                self.sumbustart = self.CurTime()
                self.lastsumbu = self.firstsumbu
                self.moves = "UNO"
                self.UNO_Boards = serial
                self.ID_Motor = MotorID


                #ROTATING MOVEMENT
                if motorname == "MOTOR_R":
                    #self.timesoon = self.CurTime()
                    volumes = self.GetKoor(3, koor, motorname)
                    self.Koordinat_IS = float(volumes)
                    self.RoboVolumes(volumes)
                    #self.timedone = self.CurTime()
                    #self.laststart = self.sumbustart
                    self.Proc_once = 0
                    self.Camera_Procedure = False
                    self.ProcedureStart = True

                    # DATA FOR Record
                    self.sumbu_rotate = self.firstsumbu
                    self.laststart_rotate = self.sumbustart
                    self.timesoon_rotate = self.CurTime()
                    self.motor_rotate = motorname

                    self.ID_Motor = MotorID
                    self.ID_ConfigDetail = detail_id
                    self.Ending_Procedure = False


                    while self.ProcedureStart == True:
                        if self.Camera_Procedure == True and self.Proc_once == 0:
                            # Load OneImage Frame
                            wx.CallAfter(pub.sendMessage,  'ImageFrame', mode=3)
                            print ('OPEN IMAGE FRAME')

                            # Load ManualFrane
                            wx.CallAfter(pub.sendMessage, 'ManualLoad', mode=3)
                            print ('OPEN MANUAL')

                            # for running just once
                            self.Proc_once += 1

                            # Wait Proces Manual Camera while Confirm Button not Pressed on Frame ManualCamera
                            print '--- -- waiting confirm -- ---'
                            while self.Camera_Procedure == True:
                                # KEYPRESS FUNCTION
                                #key = ord(getch())
                                #if key == 75:  # LEFT
                                #    self.CamPulseGO(2)
                                #elif key == 77:  # RIGHT
                                #    self.CamPulseGO(1)
                                #print 'STANDBY'
                                pass
                            print '--- -- Done confirm -- ---'

                            self.Volume_Setting = "END"
                            self.Ending_Procedure = False

                    self.timedone = self.CurTime()

                    #SAVE Record
                    self.LogRecord(self.sumbu_rotate, 0, 0, 0, config, 0, guid_proses=self.GUID_Proces,
                                   guid_motor=self.GUID_Motor, guid_config=self.GUID_Config)
                    self.LogRecord(self.sumbu_rotate, lis + 1,
                                   self.motor_rotate, 'R', config, 2, id_proses=self.ID_Proces,
                                   id_config=self.ID_Config, id_configdetail=self.ID_ConfigDetail,
                                   id_motor=self.ID_Motor, guid_proses=self.GUID_Proces,
                                   guid_motor=self.GUID_Motor, guid_config=self.GUID_Config)

                    self.Rotating = False
                    self.Proces_Step = "Finished"
                    self.Not_Moving = True
                    pass

                else:
                    if self.GenerateMOVE( motorname , koor, serial, time) == "DONE":
                        self.timesoon = self.CurTime()
                        self.timedone = self.CurTime()
                        self.Not_Moving = True
                    #elif self.GenerateMOVE(motorname, koor, serial, time) == "NONE":
                    #    self.Not_Moving = True
                    else:
                        self.Not_Moving = False

                    self.LogRecord( self.firstsumbu, 0, 0, 0, config, 0 ,guid_proses = self.GUID_Proces, guid_motor = self.GUID_Motor, guid_config = self.GUID_Config)

            self.lastconfig = config
            self.lastlist = lis + 1
            self.lastserial = serial
            self.lastmotor = motorname
            self.lastorientasi = orientasi
            self.ID_Motor = MotorID
            self.GUID_Motor = guid_motor
            self.GUID_Config = guid_config
            self.lastdetailid = detail_id
            self.ID_ConfigDetail = detail_id


            #IF IT WAS THE LAST MOVE
            #-----------------------------------------------------
            if (lis+1) == lenght and motorname != "MOTOR_R":
                self.laststart = self.sumbustart
                self.moves = "UNO"
                self.UNO_Boards = ""
                #Wait Proses

                if True:
                    if self.Home_Moving  == True:
                        modes = 2
                    else:
                        modes = 1
                    if self.Not_Moving == False:
                        print serial
                        self.UNO_Boards = serial
                        self.ReadAINO(modes, serial, motorname)
                        self.UNO_Readings = "STARTED"

                        while not self.UNO_Readings == "ENDED":
                            pass
                    else:
                        self.timesoon = self.CurTime()
                        self.timedone = self.CurTime()

                self.LogRecord( self.lastsumbu, self.lastlist ,
                                self.lastmotor, self.lastorientasi,
                                self.lastconfig, 2 ,id_proses = self.ID_Proces, id_config = self.ID_Config,id_configdetail = self.ID_ConfigDetail,
                                        id_motor = self.ID_Motor, guid_proses = self.GUID_Proces, guid_motor = self.GUID_Motor, guid_config = self.GUID_Config)
            # -----------------------------------------------------

    def GenerateMOVE(self, motorname, koorid, serial, times):

        MotorID = self.GetMotor(12, motorname) # Get ID
        if koorid == None or bool(koorid) == False:
            Koordinat = times
        else:
            Koordinat = self.GetKoor(1, koorid, motorname) # Get Coordinate Value

        Nama = self.GetKoor(2, koorid, motorname) # Get Coordinate Name

        blow_home = False
        heat_home = False
        #TO CHECK IF THE MOTOR WAS ON OFF
        if ("BLOW" in motorname) == True:
            if int(Koordinat) == 0:
                blow_home = True
            elif int(Koordinat) == 1:
                blow_home = False
            is_ex = "BLOW"
        elif ("HEAT" in motorname) == True:
            if int(Koordinat) == 0:
                heat_home = True
            elif int(Koordinat) == 1:
                heat_home = False
            is_ex = "HEAT"
        else:
            is_ex = "NONE"

        #  IF IS PAUSE MOVEMENT
        if ("PAUSE" in motorname) == True:
            self.lastcommand = '-'
            self.lastflag = self.GetMotor(7, MotorID)
            self.TimersStatus = 'None'

            wx.CallAfter(pub.sendMessage, 'TimerLoad', mode=1 ,ex=Koordinat)
            self.Not_Moving = True
            self.Home_Moving = False

            while self.TimersStatus != 'DONE':
                time.sleep(1)
                self.Ontimer()
                pass

            #self.RoboWAIT(Koordinat)

            self.Not_Moving = True
            self.Koordinat_IS = 0
            return ("DONE")

        # IF THE MOVEMENT WAS HOME ACTION
        if ("HOME" in Nama) == True or blow_home == True or heat_home == True:
            self.RoboGO(MotorID, values=Koordinat, home=1, ex=is_ex , serial=serial)
            self.Home_Moving = True
            self.Koordinat_IS = 0

            print 'ss'
            print serial
            print 'ss'

            return ("HOME")


        Koordinat = int(Koordinat)

        #self.AntiBacklash(1, Koordinat, self.XNow, "X", 500)
        self.Home_Moving = False
        if self.RoboGO(MotorID, values=Koordinat, home=0, ex=is_ex, serial=serial) == "DONE":  # ToDo : SET RoboGO To Word
            self.Koordinat_IS = Koordinat
            return ("DONE")
        
        self.Koordinat_IS = Koordinat

    def LogRecord(self, sumbu, lis, motor, orientasi, config, mode , **kwargs):
        #SAVE HEADER ON M_TransHeader
        def Header(sumbu,start,orientasi,config):
            sSQL = """ EXEC SP_Nxs_Record_TransactionHeader 1,?,?,?,? """
            Values = [str(sumbu), start, str(orientasi), str(config)]
            try:
                self.oConn.execute(sSQL,Values)
                self.Conn.commit()
            except pyodbc.ProgrammingError:
                print("INSERT HEADER FAILED , Check your Query !")

        #SAVE DETAIL ON M_TransDetail
        def Detail(mode,idh,lis,motor,start,end,orientasi):
            if mode == 0:
                noCount = " SET NOCOUNT ON; "
                sSQL = """ EXEC SP_Nxs_Record_TransactionDetail 1,?,?,?,?,?,?,? """
                Values = [int(idh), int(lis), str(motor), start, end, str(orientasi),int(self.Koordinat_IS)]

            print sSQL , Values
            try:
                data = self.oConn.execute(noCount + sSQL,Values)
                self.Conn.commit()
            except pyodbc.ProgrammingError:
                print("INSERT DETAIL FAILED , Check your Query !")

            #SAVE ON M_LOG ALSO , REMARK IF NOT NEEDED
            #===================================================================================================================
            try:
                kwargs['guid_motor']
                kwargs['guid_config']
            except Exception as e:
                print e
            else:
                # ================== SAVING ON TABLE LOG Version 1
                #SAVE SEND
                self.MDiagnostikNexus(1, GUID_Prc=kwargs['guid_config'].encode(), GUID_Motor=kwargs['guid_motor'].encode(),
                                      Prc_Name=str(config),
                                      DetailID=int(self.lastdetailid), Command=self.lastcommand, Time=self.timesoon, Type='SEND')
                #SAVE RECEIVE
                self.MDiagnostikNexus(1, GUID_Prc = kwargs['guid_config'].encode() , GUID_Motor=kwargs['guid_motor'].encode(), Prc_Name=str(config),
                                      DetailID=int(self.lastdetailid),Command=self.lastflag,Time=self.timedone,Type='RECEIVE')
                #==================================================

                # ================== SAVING ON TABLE LOG Version 2
                try:
                    kwargs['guid_proses']
                    print kwargs['id_proses']
                    print kwargs['id_config']
                    print kwargs['id_configdetail']
                except Exception as e:
                    print e
                else:
                    #filter
                    if kwargs['id_proses'] == '':
                        prosesid = kwargs['id_proses'] = None
                    else:
                        prosesid = int(kwargs['id_proses'])
                    # ================== SAVING ON TABLE LOG Version 1
                    # SAVE SEND
                    self.MDiagnostikNexus2(1, GUID_Prc=kwargs['guid_proses'].encode(),GUID_Cfg=kwargs['guid_config'].encode(),
                                          GUID_Motor=kwargs['guid_motor'].encode(), ProcessID= prosesid, ConfigID=int(kwargs['id_config']),ConfigDetailID=int(kwargs['id_configdetail']),
                                          MotorID=int(kwargs['id_motor']), Command=self.lastcommand, Time=self.timesoon,
                                          Type='SEND')
                    # SAVE RECEIVE
                    self.MDiagnostikNexus2(1, GUID_Prc=kwargs['guid_proses'].encode(),GUID_Cfg=kwargs['guid_config'].encode(),
                                          GUID_Motor=kwargs['guid_motor'].encode(), ProcessID= prosesid, ConfigID=int(kwargs['id_config']),ConfigDetailID=int(kwargs['id_configdetail']),
                                          MotorID=int(kwargs['id_motor']), Command=self.lastflag, Time=self.timedone,
                                          Type='RECEIVE')
                    # ==================================================




            #===================================================================================================================

        # GET RECENT HEADER ID FROM M_TransHeader
        # ID USED FOR INSERTING DETAIL ON M_TransDetail
        if mode == 2 or mode == 3: 
            sSQL = """ EXEC SP_Nxs_GetTransaction ?, ?, ?"""
            Values = [1,str(self.laststart),motor]
            self.Conn.commit()
            print Values
            idh = self.oConn.execute(sSQL.encode(),Values)
            idh = idh.fetchall()
            maxs = len(idh)
            idh = idh[maxs-1]
            idh = idh[0]

            
            
        if mode == 0:

            Header(sumbu,self.sumbustart,self.firstorient,config)
        elif mode == 1:

            Header(sumbu,self.sumbustart,orientasi,config)
        elif mode == 2:
            Detail( 0, idh, lis, motor, self.timesoon, self.timedone, orientasi  )
        #NOT USED DUE TO NOT USING DUAL MOVEMENT
        #elif mode == 3:
        #    Detail( 1, idh, lis, motor, self.dualsoon, self.dualdone, orientasi  )

        self.Conn.commit()

    def Offset(self, mode, motorid):
        if mode == 1:
            sSQL = (r"EXEC SP_Nxs_GetMotorData ?, ?")
            Values = [1,motorid]
            data = self.oConn.execute(sSQL,Values)
            data = data.fetchall()
            data = data[0]
            self.Conn.commit()
            return(data[0])
            
    def MoveCommand(self, motorid):
        sSQL = "EXEC SP_Nxs_GetCommand ? , ?"
        Values = [1, int(motorid)]
        data = self.oConn.execute(sSQL, Values)
        data = [ x[0] for x in data.fetchall()]
        data = data[0]
        print data
        self.Conn.commit()
        return (data)

    def HomeCommand(self, motorid):
        sSQL = "EXEC SP_Nxs_GetCommand ? , ?"
        Values = [2, int(motorid)]
        data = self.oConn.execute(sSQL, Values)
        data = [ x[0] for x in data.fetchall()]
        data = data[0]
        self.Conn.commit()
        return (data)

    def SpeedCommand(self, motorid):
        sSQL = "EXEC SP_Nxs_GetCommand ? , ?"
        Values = [3, int(motorid)]
        data = self.oConn.execute(sSQL, Values)
        data = [ x[0] for x in data.fetchall()]
        data = data[0]
        self.Conn.commit()
        return (data)

    def AccelCommand(self, motorid):
        sSQL = "EXEC SP_Nxs_GetCommand ? , ?"
        Values = [4, int(motorid)]
        data = self.oConn.execute(sSQL, Values)
        data = [ x[0] for x in data.fetchall()]
        data = data[0]
        self.Conn.commit()
        return (data)

    def GetBoard(self, mode, boardid):
        # SEE THE SP FOR DETAL OF MODE
        sSQL = "EXEC SP_Nxs_GetBoard ? , ?"
        Values = [mode, int(boardid)]
        data = self.oConn.execute(sSQL, Values)
        data = [x[0] for x in data.fetchall()]
        data = data[0]
        self.Conn.commit()
        return (data)

    def GetMotor(self, mode, motorid):
        # SEE THE SP FOR DETAL OF MODE
        print motorid
        sSQL = "EXEC SP_Nxs_GetMotorData ? , ?"
        Values = [mode, str(motorid)]
        print sSQL,Values
        data = self.oConn.execute(sSQL, Values)
        data = [x[0] for x in data.fetchall()]
        print data
        print "-----------------"
        print len(data)
        print "-----------------"
        data = data[0]
        self.Conn.commit()
        return (data)

    def GetSpeedSet(self, mode, speedid):
        #Get Speed
        #if mode == 1:
        # Get Accel
        #elif mode == 2:
        print speedid
        sSQL = "EXEC SP_Nxs_GetSpeedSet ? , ?"
        Values = [mode, str(speedid)]
        print sSQL, Values
        data = self.oConn.execute(sSQL, Values)
        data = [x[0] for x in data.fetchall()]
        print data
        data = data[0]
        self.Conn.commit()
        return (data)

    def GetKoor(self, mode, koorid, motorname):
        # SEE THE SP FOR DETAL OF MODE
        if koorid == None or bool(koorid) == False:
            return(0)
        sSQL = "EXEC SP_Nxs_GetKoor ? , ? , ?"
        Values = [mode, int(koorid), motorname]
        print sSQL,Values
        data = self.oConn.execute(sSQL, Values)
        data = [x[0] for x in data.fetchall()]
        data = data[0]
        self.Conn.commit()
        return (data)

    def GetMovement(self, mode):
        #GET LIST OF FISRTS VOLUME MPVEMENT
        if mode == 1:
            self.TableGet(2, rotatemode=1)

        #GET LIST OF SECOND VOLUME MOVEMENT
        elif mode == 2:
            self.TableGet(2, rotatemode=2)
        #GET SET START
        elif mode == 3:
            self.TableGet(2, rotatemode=3)
        #GET SET END
        elif mode == 4:
            self.TableGet(2, rotatemode=4)

    def GETData(self,mode,**kwargs):
        if mode == 1: #Simple
            sSQL = ("SELECT "+str(kwargs["kolom"])+" FROM "+str(kwargs["table"]))
            data = self.oConn.execute(sSQL)

        elif mode == 2: #SP EXECUTE
            sSQL = kwargs["SQL"]
            Values = kwargs["value"]
            data = self.oConn.execute(sSQL, Values)

        data = data.fetchall()
        self.Conn.commit()
        return (data)

    def MDiagnostikNexus(self, mode, **kwargs):
        sSQL = "EXEC SP_Nxs_Diagnostik ?, ?, ?, ?, ?, ?, ?, ?, ?"

        #Generate Default Values
        attr_len = 9
        Values = {}
        for i in range(attr_len):
            Values.update({(int(i)+1):''})

        if mode == 1:
            #SET The Parameters
            Values[1] = int(mode)

            try:
                kwargs['GUID_Prc']
            except Exception as e:
                print e
            else:
                Values[2] = kwargs['GUID_Prc']

            try:
                kwargs['GUID_Motor']
            except Exception as e:
                print e
            else:
                Values[3] = kwargs['GUID_Motor']

            try:
                kwargs['Prc_Name']
            except Exception as e:
                print e
            else:
                Values[4] = kwargs['Prc_Name']

            try:
                kwargs['DetailID']
            except Exception as e:
                print e
            else:
                Values[5] = kwargs['DetailID']

            try:
                kwargs['Command']
            except Exception as e:
                print e
            else:
                Values[6] = kwargs['Command']

            try:
                kwargs['Time']
            except Exception as e:
                print e
            else:
                Values[7] = kwargs['Time']

            try:
                kwargs['Type']
            except Exception as e:
                print e
            else:
                Values[8] = kwargs['Type']

        elif mode == 2:
            # SET The Parameters
            Values[1] = int(mode)
            pass

        elif mode == 3:
            # SET The Parameters
            Values[1] = int(mode)
            try:
                kwargs['GUID_Prc']
            except Exception as e:
                print e
            else:
                Values[9] = kwargs['GUID_Prc']


        #EXECUTE COMMAND
        try:
            print sSQL, [Values[keys] for keys in Values]
            data = self.oConn.execute(sSQL, [Values[keys] for keys in Values])
            if mode != 1:
                data = data.fetchall()
            self.Conn.commit()
        except Exception as e:
            print e
            if mode != 1:
                print("QUERY FAILED [" + str(mode) + "] , Check your Query !")
        else:
            if mode != 1:
                try:
                    data = [x[0] for x in data]
                except Exception as e:
                    print e
                else:
                    if len(data) == 1:
                        return data[0]
                    else:
                        return data
                    print 'L0L0L0L0 >>?? ' + str(data)
        self.Conn.commit()

    # ============ VERSION 2
    def MDiagnostikNexus2(self, mode, **kwargs):
        sSQL = "EXEC SP_Nxs_Diagnostik2 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?"

        # Generate Default Values
        attr_len = 12
        Values = {}
        for i in range(attr_len):
            Values.update({(int(i) + 1): ''})


        if mode == 1:
            # SET The Parameters
            Values[1] = int(mode)

            try:
                kwargs['GUID_Prc']
            except Exception as e:
                print e
            else:
                Values[2] = kwargs['GUID_Prc']

            try:
                kwargs['GUID_Cfg']
            except Exception as e:
                print e
            else:
                Values[3] = kwargs['GUID_Cfg']

            try:
                kwargs['GUID_Motor']
            except Exception as e:
                print e
            else:
                Values[4] = kwargs['GUID_Motor']

            try:
                kwargs['ProcessID']
            except Exception as e:
                print e
            else:
                Values[5] = kwargs['ProcessID']

            try:
                kwargs['ConfigID']
            except Exception as e:
                print e
            else:
                Values[6] = kwargs['ConfigID']

            try:
                kwargs['ConfigDetailID']
            except Exception as e:
                print e
            else:
                Values[7] = kwargs['ConfigDetailID']

            try:
                kwargs['MotorID']
            except Exception as e:
                print e
            else:
                Values[8] = kwargs['MotorID']


            try:
                kwargs['Command']
            except Exception as e:
                print e
            else:
                Values[9] = kwargs['Command']

            try:
                kwargs['Time']
            except Exception as e:
                print e
            else:
                Values[10] = kwargs['Time']

            try:
                kwargs['Type']
            except Exception as e:
                print e
            else:
                Values[11] = kwargs['Type']

        # EXECUTE COMMAND
        try:
            print sSQL, [Values[keys] for keys in Values]
            data = self.oConn.execute(sSQL, [Values[keys] for keys in Values])
            if mode != 1:
                data = data.fetchall()
            self.Conn.commit()
        except Exception as e:
            print e
            if mode != 1:
                print("QUERY FAILED [" + str(mode) + "] , Check your Query !")
        else:
            if mode != 1:
                try:
                    data = [x[0] for x in data]
                except Exception as e:
                    print e
                else:
                    if len(data) == 1:
                        return data[0]
                    else:
                        return data
                    print 'L0L0L0L0 >>?? ' + str(data)
        self.Conn.commit()
