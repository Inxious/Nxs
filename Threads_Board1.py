
import time

#Threads For Board 1

class ThreadsB1():
    def  __init__(self):
        print 'THREAD 1 JALAN'

        while True:

            if self.Board1_Connection == "ON":


                if self.Board1_Reading == "ON":
                    self.Board1_Reading_Data = ""
                    self.Board1_Reading_Result = "STARTED"

                    print '1'

                    time_pass  = 0
                    #self.ser1.flushInput()
                    #self.ser1.flushOutput()

                    # DELAY
                    try:
                        times = float(self.Board1_Delay)
                    except Exception as e:
                        times = 0.1
                    else:
                        times = float(self.Board1_Delay)

                    # TO
                    try:
                        timesout = float(self.Board1_TO)
                    except Exception as e:
                        timesout = 180
                    else:
                        timesout = float(self.Board1_TO)

                    print '1'

                    while self.Board1_Reading_Flag not in self.Board1_Reading_Data:


                        if int(time_pass) > float(timesout):
                            break
                            print("PROSES TIMEOUT")
                            self.Board1_Reading_Result = "FAILED"

                        data = str(self.ser1.readline())


                        if data:
                            self.LogView(1, board = 1, line = data)

                        self.Board1_Reading_Data += (data)

                        time.sleep(float(times))
                        time_pass += float(times)

                    if (self.Board1_Reading_Flag in self.Board1_Reading_Data) == True:
                        self.Board1_Reading_Result = "SUCCESS"

                    if self.Board1_Reading_Result == "FAILED":
                        self.Board1_Reading_Result = "FAILED"
                        self.Proces_Step = "Unfinished"
                        self.timedone = self.CurTime()
                        self.Board1_Reading = "OFF"
                        #self.ser2.flushInput()
                        #self.ser2.flushOutput()

                    elif self.Board1_Reading_Result == "SUCCESS":
                        self.Board1_Motor = "NONE"
                        self.Board1_Reading_Result = "SUCESS"
                        self.timedone = self.CurTime()
                        self.Proces_Step = "Finished"
                        self.Board1_Reading = "OFF"
                        #self.ser1.flushInput()
                        #self.ser1.flushOutput()

                    if self.UNO_Boards == 1:
                        self.Proces_Step = "Finished"
                        self.UNO_Readings = "ENDED"
                        #self.ser1.flushInput()
                        #self.ser1.flushOutput()

                    elif self.DUAL_Boards == 1:
                        self.Proces_Step = "Finished"
                        self.DUAL_Readings = "ENDED"
                        #self.ser1.flushInput()
                        #self.ser1.flushOutput()









