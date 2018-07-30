# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import time




###########################################################################
## Class MyFrame1
###########################################################################

class FrameTimer(wx.Frame):
    def __init__(self, parent, times):

        self.starttimer = 0
        self.curtimer = 0
        self.maxtimer = times
        self.TimersStatus = 'START'

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(440, 143), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        gSizer1 = wx.GridSizer(1, 1, 0, 0)

        self.Pnl_T1 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Pnl_T1.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.Pnl_T1.SetMinSize(wx.Size(400, -1))

        fgSizer1 = wx.FlexGridSizer(3, 1, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer1.SetMinSize(wx.Size(500, -1))
        self.Pnl_T2 = wx.Panel(self.Pnl_T1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Pnl_T2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))
        self.Pnl_T2.SetMinSize(wx.Size(400, -1))

        gSizer2 = wx.GridSizer(1, 1, 0, 0)

        gSizer2.SetMinSize(wx.Size(4500, -1))
        self.Jdl_Tmrs = wx.StaticText(self.Pnl_T2, wx.ID_ANY, u"Timer Countdown", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Jdl_Tmrs.Wrap(-1)
        self.Jdl_Tmrs.SetFont(wx.Font(12, 70, 90, 92, False, "Arial"))

        gSizer2.Add(self.Jdl_Tmrs, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_T2.SetSizer(gSizer2)
        self.Pnl_T2.Layout()
        gSizer2.Fit(self.Pnl_T2)
        fgSizer1.Add(self.Pnl_T2, 1, wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        gSizer3 = wx.GridSizer(1, 2, 0, 0)

        self.Lbl_MustTime = wx.StaticText(self.Pnl_T1, wx.ID_ANY, u"Time", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_MustTime.Wrap(-1)
        gSizer3.Add(self.Lbl_MustTime, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Txt_Timers = wx.TextCtrl(self.Pnl_T1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.Txt_Timers.SetMinSize(wx.Size(150, -1))

        gSizer3.Add(self.Txt_Timers, 0, wx.ALL, 5)

        fgSizer1.Add(gSizer3, 1, wx.EXPAND | wx.ALIGN_RIGHT, 5)

        self.Pb_Tmr = wx.Gauge(self.Pnl_T1, wx.ID_ANY, int(self.maxtimer), wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.Pb_Tmr.SetValue(0)
        self.Pb_Tmr.SetMinSize(wx.Size(400, 20))

        fgSizer1.Add(self.Pb_Tmr, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_T1.SetSizer(fgSizer1)
        self.Pnl_T1.Layout()
        fgSizer1.Fit(self.Pnl_T1)
        gSizer1.Add(self.Pnl_T1, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(gSizer1)
        self.Layout()
        #self.StopWatch = wx.Timer(self)
        #self.StopWatch.Start(1000)
        timesmax = time.strftime("%H:%M:%S", time.gmtime(int(self.maxtimer)))
        self.Txt_Timers.SetValue(timesmax)
        self.Lbl_MustTime.SetLabel('TIMER = ' + str(timesmax))

        self.Centre(wx.BOTH)


        # Connect Events
        #self.Bind(wx.EVT_TIMER, self.Ontimer, self.StopWatch)
        self.Show()

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def Ontimer(self):

        if self.curtimer >= self.maxtimer:
            self.curtimer = self.starttimer
            self.Hide()
            self.TimersStatus = 'DONE'
        else:
            self.curtimer += 1
            self.Pb_Tmr.SetValue(self.curtimer)
            times = time.strftime("%H:%M:%S", time.gmtime(int(self.maxtimer) - int(self.curtimer)))
            self.Txt_Timers.SetValue(times)


