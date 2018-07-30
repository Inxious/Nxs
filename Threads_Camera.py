
import time

#Threads For Board 2

class Camera():
    def  __init__(self):

        while True:

            if self.Camera_Connection == "ON":


                if self.Camera_Reading == "ON":
                    self.Camera_Readed_Status = ""

                    print ('READING')

                    self.Camera_Reading_Data = ""
                    self.Camera_Reading_Result = "STARTED"

                    #ToDo : READ 2
                    #self.ser3.write("READ" + "\r\n")
                    #Readings = True

                    #IF USING 2 READ
                    if self.Camera_Crop == 'UPPER':
                        senddata = "VOLUME_UP"
                        Readings = True
                    elif self.Camera_Crop == 'LOWER':
                        senddata = "VOLUME_DOWN"
                        Readings = True
                    else:
                        senddata = "READ"
                        Readings = True

                    #WRITE
                    try:
                        self.ser3.write(str(senddata) + "\n")
                        self.LogView(2, board=3, line=senddata)
                    except Exception as e:
                        print e
                        ser_reload = True
                    else:
                        ser_reload = False
                    finally:
                        if ser_reload == True:
                            #self.ReConnectSerial()
                            self.CSerialRecon(3)
                            Readings = True

                    hasildata = ''
                    trial = 20
                    trial_count = 0
                    while Readings:
                        #time.sleep(1)

                        if trial_count == trial:
                            Readings = False

                        try:
                            data = str(self.ser3.readline())
                        except Exception as e:
                            print e
                            ser_reload = True
                        else:
                            ser_reload = False
                        finally:
                            if ser_reload == True:
                                self.CSerialRecon(3)
                                Readings = True

                        #Filter Readline Data Result
                        filered_data = ''
                        for string in data:
                            if string in ['',None,' ']:
                                pass
                            else:
                                filered_data += str(string)




                        if data == "" or len(data) == 0 or data == None or ser_reload == True:
                            ser_reload = False
                            pass
                        else:
                            hasildata += str(data)

                        if ('\n' in data) == True and len(data) > 3:
                            Readings = False

                        trial_count += 1

                    if len(data.split("[+]")) != 3:
                        data = "FAILED[+]FAILED[+]FAILED"
                    else:
                        hasilfilter = []
                        for item in data.split("[+]"):
                            for string in item:
                                if string in ['F','A','I','L','E','D']:
                                    item = 'FAILED'
                                    break
                            hasilfilter.append(str(item))
                        if len(hasilfilter) != 3:
                            data = "FAILED[+]FAILED[+]FAILED"
                        else:
                            data = str(hasilfilter[0]) + '[+]' + str(hasilfilter[1]) + '[+]' + str(hasilfilter[2])

                        self.LogView(1, board=3, line=data)


                    self.Camera_Readed_Value = self.CameraCompare(1,data.split("[+]"))
                    print 'HASILLLLLS'
                    print self.Camera_Readed_Value
                    print data
                    print self.Camera_Readed_Value
                    print 'HASILLLLLS'
                    self.Array_of_Truth = self.CameraCompare(2,data.split("[+]"))
                    print self.Array_of_Truth

                    if self.Camera_Readed_Value != "FAILED":
                        self.Camera_Readed_Status = "SUCCES"
                    else:
                        self.Camera_Readed_Status = "FAILED"

                    self.Camera_Reading_Result = "SUCESS"
                    self.Camera_Reading = "OFF"









