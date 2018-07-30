import time
import serialscan

#THREAD FOR PASSING VAR FOR EACH BOARDTHREADS

class ThreadsPasser():
    def __init__(self):
        self.Proces_Step = "Started"
        print "THREAD EVENT RUNNING"
        
        #Infinity Loop Until App Exit
        while True:

            if self.Event_Status == "ON":
                if self.Event_Types == "Proces":
                    #== Running Proces
                    self.Proces_Step = "Running"
                    print "======++++++=======+++++"
                    print "START"
                    print "======++++++=======+++++"
                    for datalist in self.Proces_Data:
                        #-- Running the proceslist
                        if not self.Proces_Step == "Unfinished":

                            #Only Run Checked Value
                            if datalist[0] == True:
                                self.TableGet(1, act=datalist[1])

                            #-- Adding current proceslist if it was failed before it ends
                            if self.Proces_Step == "Unfinished":
                                self.Proces_UnfinishedList.append(datalist[1])

                        #-- Adding rest of proceslist that is unfinished
                        if self.Proces_Step == "Unfinished":
                            self.MessagesBox("Ordinary", "Warning : Proces Failed!",
                                             "Ada Proses Yang Gagal !" +
                                             "Proses Akan Berhenti !")
                            self.Proces_UnfinishedList.append(datalist[1])
                        print "======++++++=======+++++"
                        print "FINISH HIM"
                        print "======++++++=======+++++"

                    #== When Proces Ends
                    print "======++++++=======+++++"
                    print "FATALITY"
                    print "======++++++=======+++++"
                    self.Event_Types = "NONE"
                    self.Is_All = False
                    self.MFEnable()
                    if self.Proces_Step == "Running":
                        self.Proces_Step = "Ends"
                    self.Event_Status = "OFF"

                elif self.Event_Types == "Action":

                    #-- If Event Was Serial Connection
                    if self.Event_Name == "Connection":
                        if self.Connection_Mode == "Connect":
                            self.SerialConn(self.Serial_Board, self.Serial_COM_PORT, self.Serial_BRATE, self.Serial_Timeout)
                        elif self.Connection_Mode == "Dissconn":
                            self.SerialDisConn(self.Connection_Board)

                    #-- if Event Was Temperature Based
                    elif self.Event_Name == "Temperature":
                        if self.Event_Temperature == "ON":
                            self.RoboHEAT(1)
                        elif self.Event_Temperature == "OFF":
                            self.RoboHEAT(0)
                        elif self.Event_Temperature == "StandBy":
                            self.StandbyTemp = True
                            self.LimitTemp = 37
                            self.TimerTemp = 0
                            self.suhus = "off"
                            self.Cmd_MF_Temp_Standby.SetLabel("STOP")
                        elif self.Event_Temperature == "Stop":
                            self.StandbyTemp = False
                            self.suhus = "off"
                            self.RoboHEAT(0)
                            self.Cmd_MF_Temp_Standby.SetLabel("STANDBY")

                    # == When Action Ends
                    self.Event_Types = "NONE"
                    self.Is_All = False
                    self.MFEnable()
                    self.Event_Status = "OFF"


