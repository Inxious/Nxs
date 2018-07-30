# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import ConfigParser
import time


###########################################################################
## Class Frm_Cam
###########################################################################

class Frm_Cam(wx.Frame):
    def __init__(self, parent):

        # IMPORT SETTING
        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.Hi = config.get('OneImage Configuration', 'BigValCoordinate')
        self.Lo = config.get('OneImage Configuration', 'LowValCoordinate')

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(336, 315), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        gSizer1 = wx.GridSizer(1, 1, 0, 0)

        self.Pnl_Cam = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1, -1), wx.TAB_TRAVERSAL)
        self.Pnl_Cam.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))

        fgSizer1 = wx.FlexGridSizer(3, 1, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_Jdl_Cam = wx.StaticText(self.Pnl_Cam, wx.ID_ANY, u"MANUAL ROTATE PROCEDURE", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.Lbl_Jdl_Cam.SetFont(wx.Font(16, 74, 90, 92, False, "Calibri"))
        self.Lbl_Jdl_Cam.SetBackgroundColour(wx.Colour(255, 255, 128))
        self.Lbl_Jdl_Cam.Wrap(-1)
        fgSizer1.Add(self.Lbl_Jdl_Cam, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer2 = wx.FlexGridSizer(3, 1, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_Info_Cam = wx.StaticText(self.Pnl_Cam, wx.ID_ANY, u"*Please see the camera view on the other screen \n"
                                                                   u"*Use RIGHT ARROW TO PLUS  \n"
                                                                   u"*Use LEFT ARROW TO MINUS  \n",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Info_Cam.Wrap(-1)
        fgSizer2.Add(self.Lbl_Info_Cam, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gSizer6 = wx.GridSizer(0, 2, 0, 0)

        self.Cmd_Cam_UpSet = wx.Button(self.Pnl_Cam, wx.ID_ANY, u"SET UPPER VALUE", wx.DefaultPosition, wx.DefaultSize,
                                       0)
        gSizer6.Add(self.Cmd_Cam_UpSet, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_Cam_LoSet = wx.Button(self.Pnl_Cam, wx.ID_ANY, u"SET LOWER VALUE", wx.DefaultPosition, wx.DefaultSize,
                                       0)
        gSizer6.Add(self.Cmd_Cam_LoSet, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer2.Add(gSizer6, 1, wx.EXPAND, 5)

        fgSizer3 = wx.FlexGridSizer(0, 3, 0, 0)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        gbSizer2 = wx.GridBagSizer(0, 0)
        gbSizer2.SetFlexibleDirection(wx.BOTH)
        gbSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_Cam_Plus = wx.StaticText(self.Pnl_Cam, wx.ID_ANY, u"PLUS", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Cam_Plus.Wrap(-1)
        gbSizer2.Add(self.Lbl_Cam_Plus, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_Cam_Plus = wx.Button(self.Pnl_Cam, wx.ID_ANY, u"+", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.Cmd_Cam_Plus, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        fgSizer3.Add(gbSizer2, 1, wx.EXPAND, 5)

        gbSizer4 = wx.GridBagSizer(0, 0)
        gbSizer4.SetFlexibleDirection(wx.BOTH)
        gbSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_Val_Used = wx.StaticText(self.Pnl_Cam, wx.ID_ANY, u"Value Used", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Val_Used.Wrap(-1)
        gbSizer4.Add(self.Lbl_Val_Used, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        Cmb_Cam_ValueChoicess = ['10','100','1000']
        self.Cmb_Cam_Value = wx.ComboBox(parent=self.Pnl_Cam, id=wx.ID_ANY, value=u"-- Value --", pos=wx.DefaultPosition, size=wx.Size(100,30), choices=Cmb_Cam_ValueChoicess)
        gbSizer4.Add(self.Cmb_Cam_Value, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        fgSizer3.Add(gbSizer4, 1, wx.EXPAND, 5)

        gbSizer5 = wx.GridBagSizer(0, 0)
        gbSizer5.SetFlexibleDirection(wx.BOTH)
        gbSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_Cam_Min = wx.StaticText(self.Pnl_Cam, wx.ID_ANY, u"MINUS", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Cam_Min.Wrap(-1)
        gbSizer5.Add(self.Lbl_Cam_Min, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_Cam_Min = wx.Button(self.Pnl_Cam, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer5.Add(self.Cmd_Cam_Min, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        fgSizer3.Add(gbSizer5, 1, wx.EXPAND, 5)

        fgSizer2.Add(fgSizer3, 1, wx.EXPAND, 5)

        fgSizer1.Add(fgSizer2, 1, wx.EXPAND, 5)

        gSizer3 = wx.GridSizer(1, 2, 0, 0)

        self.Cmd_Cam_Confirm = wx.Button(self.Pnl_Cam, wx.ID_ANY, u"Confirm", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.Cmd_Cam_Confirm, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_Cam_Exit = wx.Button(self.Pnl_Cam, wx.ID_ANY, u"EXIT", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer3.Add(self.Cmd_Cam_Exit, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer1.Add(gSizer3, 1, wx.EXPAND, 5)

        self.Pnl_Cam.SetSizer(fgSizer1)
        self.Pnl_Cam.Layout()
        fgSizer1.Fit(self.Pnl_Cam)
        gSizer1.Add(self.Pnl_Cam, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        #self.SetWindowStyle(wx.STAY_ON_TOP)

        self.Show()

        # Connect Events
        self.Cmd_Cam_UpSet.Bind(wx.EVT_BUTTON, lambda x:self.CamPulseGO(3))
        self.Cmd_Cam_LoSet.Bind(wx.EVT_BUTTON, lambda x:self.CamPulseGO(4))
        self.Cmd_Cam_Plus.Bind(wx.EVT_BUTTON, lambda x:self.CamPulseGO(1))
        self.Cmd_Cam_Min.Bind(wx.EVT_BUTTON,  lambda x:self.CamPulseGO(2))
        self.Cmd_Cam_Confirm.Bind(wx.EVT_BUTTON, lambda x:self.CamFrameAct(1))
        self.Cmd_Cam_Exit.Bind(wx.EVT_BUTTON, lambda x:self.CamFrameAct(2))




    def CamPulseGO (self, mode):

        if mode == 1:
            Pulse = (float(self.RNow) - float(self.Cmb_Cam_Value.GetValue()))
            self.RoboGO(17, values=Pulse, home=0, ex="NONE", serial=1)
            self.ReadAINO(1, 1, "MOTOR_R")
            if self.ViewType == 'User':
                if self.StreamType == 'Image':
                    self.CameraRead(3)
                    time.sleep(1)
                    self.GoOpenImage(self.ImageStream)

            self.Cmd_Cam_Min.SetFocus()

        elif mode == 2:
            Pulse = (float(self.RNow) + float(self.Cmb_Cam_Value.GetValue()))
            self.RoboGO(17, values=Pulse, home=0, ex="NONE", serial=1)
            self.ReadAINO(1, 1, "MOTOR_R")
            if self.ViewType == 'User':
                if self.StreamType == 'Image':
                    self.CameraRead(3)
                    time.sleep(1)
                    self.GoOpenImage(self.ImageStream)

            self.Cmd_Cam_Plus.SetFocus()

        elif mode == 3: #UPPER
            self.RoboGO(1, values=float(self.Hi), home=0, ex="NONE", serial=1)
            self.ReadAINO(1, 1, "MOTOR_Z")
            if self.ViewType == 'User':
                if self.StreamType == 'Image':
                    self.CameraRead(3)
                    time.sleep(1)
                    self.GoOpenImage(self.ImageStream)

        elif mode == 4: #LOWER
            self.RoboGO(1, values=float(self.Lo), home=0, ex="NONE", serial=1)
            self.ReadAINO(1, 1, "MOTOR_Z")
            if self.ViewType == 'User':
                if self.StreamType == 'Image':
                    self.CameraRead(3)
                    time.sleep(1)
                    self.GoOpenImage(self.ImageStream)


    def CamFrameAct (self, mode):
        if mode == 1:
            self.Cam_Procedure_Status = "CONFIRMED"
            self.ser3.write("END" + '\r\n')
            self.Volume_Setting = 'END'
            self.Camera_Procedure = False
            self.Ending_Procedure = True
            self.Hide()
            #if self.ViewType != 'Rasberry':
            #    self.OneImageCloseFrame()

        elif mode == 2:
            #if self.ViewType != 'Rasberry':
                #self.OneImageCloseFrame()
            self.Hide()






