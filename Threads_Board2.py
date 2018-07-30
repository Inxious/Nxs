
import time
import datetime
import math

#Threads For Board 2

class ThreadsB2():

    def  __init__(self):

        starting = False
        self.AVG_Count = 0
        self.AVG_Total = 0
        self.suhus = ''
        self.SuhuReadCount = 1

        while True:

            if self.Board2_Connection == "ON":

                self.SaveLogSuhuActive = True

                if self.Board2_Reading == "ON":
                    self.StandbyTemp = False
                    data2 = ""
                    rightvalue = ["DONE", "HEATER", "ON", "OFF"]
                    while self.Ser2_Active == True:

                        #DELAY
                        try:
                            times = float(self.Board2_Delay)
                        except Exception as e:
                            times = 0.1
                        else:
                            times = float(self.Board2_Delay)

                        time.sleep(times)

                        if self.Ser2_Active == False:
                            break
                            return
                        data2 = self.ser2.readline()

                        #self.ser2.flushInput()
                        #self.ser2.flushOutput()

                        if data2 != "":
                            types = ""
                            for right in rightvalue:
                                # COMMAND READ
                                # ===================================================================
                                if (right in data2) == True:
                                    self.LbLog.AppendItems("Board 2 >> " + str(data2))
                                    self.LbLog.SetFirstItem(int(self.LbLog.GetCount() - 1))
                                    types = "string"
                                    break
                                else:
                                    #============== ADD BY REZA 7/12/18 V2.3.4 ======

                                    try:
                                        float(data2)
                                    except Exception as e:
                                        print e
                                        continue
                                    else:
                                        types = "number"

                                    #===============================================

                            # Continue if it was string
                            if types == "string":
                                continue
                            elif types == "number":
                                filtered = ''
                                for alfabet in str(data2):
                                    if alfabet != '' and alfabet != ' ':
                                        filtered += alfabet

                                if filtered == '' or len(filtered) == 0:
                                    continue
                                else:
                                    data2 = filtered

                            # SUHU READING
                            # ===================================================================
                            hasil = ""
                            for string in str(data2):
                                if string == "" or string == " ":
                                    pass
                                else:
                                    try:
                                        int(string)
                                    except Exception as e:
                                        if string in ('.',',','-'):
                                            hasil += string
                                    else:
                                        hasil += string

                            if hasil == "" or len(hasil) == 0:
                                continue
                            else:
                                #Save Log Suhu
                                if self.SaveLogSuhuActive == True:
                                    #data = {}
                                    waktulog = str(self.CurTime())
                                    statuslog = str(self.suhus)
                                    suhulog = str(float(hasil))
                                    if len(self.LogSuhuRt) >= 100:
                                        self.MFAppendConfig(self.CurrentFileSuhu, self.LogSuhuRt)
                                    else:
                                        self.LogSuhuRt.update({str(self.SuhuReadCount):{'Suhu':suhulog,'Waktu':waktulog,'StatusHeater':statuslog}})
                                    #self.MFAppendConfig(self.CurrentFileSuhu, data)
                                    self.SuhuReadCount += 1
                                try:
                                    float(hasil)
                                except Exception as e:
                                    continue
                                else:
                                    if float(hasil) < 0 or hasil[0] == '-':
                                        continue

                                    #GET LAST SUHU
                                    try:
                                        float(self.lastsuhubaca)
                                    except Exception as e:
                                        self.lastsuhubaca = float(hasil)
                                        formated_hasil = self.CFormatSuhu(hasil)
                                        if formated_hasil != None:
                                            self.Lbl_MF_Temp_Value.SetLabel(formated_hasil)
                                    else:
                                        #FOR DIFFER TOO HIGH
                                        formated_hasil = self.CFormatSuhu(hasil)
                                        if float(self.lastsuhubaca) > float(hasil):
                                            if (float(self.lastsuhubaca) - float(hasil)) > 10:
                                                hasil = self.lastsuhubaca
                                            else:
                                                if formated_hasil != None:
                                                    self.Lbl_MF_Temp_Value.SetLabel(formated_hasil)
                                        elif float(self.lastsuhubaca) < float(hasil):
                                            if (float(hasil) - float(self.lastsuhubaca)) > 10:
                                                hasil = self.lastsuhubaca
                                            else:
                                                if formated_hasil != None:
                                                    self.Lbl_MF_Temp_Value.SetLabel(formated_hasil)

                                    self.lastsuhubaca = float(hasil)

                                #self.ser2.flushInput()
                                #self.ser2.flushOutput()

                            # IF Standby Command is Activated
                            # ======================================================================
                            if self.StandbyTemp == True:
                                if self.AVG_Count == 0:
                                    starting = True
                                    starts = datetime.datetime.now()
                                    start_time = self.CurTime()

                                if hasil == "":
                                    pass
                                else:
                                    try:
                                        hasil = float(hasil)
                                    except Exception as e:
                                        pass
                                    else:
                                        #STANDBYING TEMP
                                        if float(hasil) >= int(self.MaxLimitTemp):
                                            if self.suhus == "off":
                                                pass
                                            else:
                                                # func turn off HEATER
                                                self.RoboHEAT(0)
                                                self.suhus = "off"

                                        elif float(hasil) <= int(self.MinLimitTemp):
                                            if self.suhus == "on":
                                                pass
                                            else:
                                                # func turn on HEATER
                                                self.RoboHEAT(1)
                                                self.suhus = "on"

                                        self.AVG_Count += 1
                                        self.AVG_Total += float(hasil)
                                        nows =  datetime.datetime.now()
                                        minute_differ = math.floor(((nows - starts).total_seconds() // 60 ))

                                        if  minute_differ >= 30:
                                            end_time = self.CurTime()
                                            hasil = self.AVG_Total / self.AVG_Count

                                            print ("=================================")
                                            print (" start  =   " + str(start_time))
                                            print (" rata rata = " + str(float(hasil)))
                                            print (" end    =   " + str(end_time))
                                            print ("=================================")

                                            start_time = self.CurTime()
                                            starts = datetime.datetime.now()
                                            self.AVG_Count = 0
                                            self.AVG_Total = 0

                            if self.StandbyTemp == False:
                                self.AVG_Count = 0
                                self.AVG_Total = 0