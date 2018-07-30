

import MainFrame
import Frame_ManualCmd
import Frm_SpeedTable
import Frame_ManualCamera
import Frame_Timer
import Frame_OneImage

import time
import wx
import ConfigParser
import  wx.adv as adv
import Frame_LogSuhu

class View(MainFrame.MainFrame,Frame_ManualCmd.Mnl_Frame,Frm_SpeedTable.Frm_SpeedTable,Frame_ManualCamera.Frm_Cam,
           Frame_Timer.FrameTimer,Frame_OneImage.Frame_Images,Frame_LogSuhu.Frm_SaveLogSuhu):
    def __init__(self):

        # IMPORT SETTING
        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.ViewType = config.get('Camera Configuration', 'ViewType')

        MainFrame.MainFrame.__init__(self,None)
        #self.FrameLoad(3)


    def FrameLoad(self, mode , **kwargs):
        #MANUAL FRAME
        if mode == 1:
            Frame_ManualCmd.Mnl_Frame.__init__(self,None)
        elif mode == 2:
            Frm_SpeedTable. Frm_SpeedTable.__init__(self,None)
        elif mode == 3:
            if self.ViewType == 'Rasberry':
                self.ser3.write("VIEW" + '\r\n')
            elif self.ViewType == 'User':
                self.FrameLoad(5)
            else:
                self.FrameLoad(5)
            Frame_ManualCamera.Frm_Cam.__init__(self, None)

        elif mode == 4:
            print kwargs['time']
            Frame_Timer.FrameTimer.__init__(self, None, kwargs['time'])
        elif mode == 5:
            if self.StreamType == 'Stream':
                self.CCameraCommand(1)
            time.sleep(3)
            Frame_OneImage.Frame_Images.__init__(self,None)
        elif mode == 6:
            Frame_LogSuhu.Frm_SaveLogSuhu.__init__(self,None)
            self.SaveLogSuhuActive = False

    def FrameEx(self, mode, ex):
        if mode == 1:
            print ex
            Frame_Timer.FrameTimer.__init__(self, None, int(ex))
        elif mode == 2:
            # Show MessageBox
            self.MsgBox_Alert_Rotate = self.MessagesBox('ManualRotateAlert', 'Manual Camera Rotate Initiated',
                                                        'Manual Procedure Started . Please Press the "CONTINUE" button to Continue')
            self.option = 'NONE'
            klick = self.MsgBox_Alert_Rotate.ShowModal()

            if klick == wx.ID_OK or klick == wx.ID_CANCEL:
                self.option = 'DONE'

    def MessagesBox(self, mode, title, message):
        if mode == "Ordinary":
            wx.MessageBox(message,title)
        elif mode == "ManualRotateAlert":
            return(wx.MessageDialog(None, message, title, wx.OK | wx.CANCEL | wx.ICON_ERROR))

    def PlaySound(self, mode):
        #Beep
        if mode == 1:
            sound = adv.Sound('Sound\Beep.wav')
            if sound.IsOk():
                sound.Play(adv.SOUND_ASYNC)
            else:
                wx.MessageBox("Invalid sound file", "Error")
            time.sleep(3)

    def GenerateHTML(self, mode, image_source):
        #IMAGE VIEWER HTML
        if mode == 1:
            strings = '''   <!DOCTYPE html>
                            <html>
                            <head>
                                <title>	
                                    Nexus Image Viewer
                                </title>
                            </head> 
                            <body style="width:100%">
                                    
                                    <p align="center" , style="vertical-align: middle;">
                                    <center>
                                    <img style="margin: auto;" src="'''+ str(image_source) + '''" class="imgViewer">
                                    </center>
                                    </p>
                                    
                            </body>
                            </html>     '''
            return(strings)