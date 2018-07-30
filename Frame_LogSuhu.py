# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class Frm_SaveLogSuhu
###########################################################################

class Frm_SaveLogSuhu(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Save Log Suhu to a file", pos=wx.DefaultPosition,
                          size=wx.Size(509, 144), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)


        gSizer1 = wx.GridSizer(1, 1, 0, 0)

        self.Pnl_Savelog = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Pnl_Savelog.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        fgSizer1 = wx.FlexGridSizer(3, 1, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Jdl_Savelog = wx.StaticText(self.Pnl_Savelog, wx.ID_ANY, u"Save Log File", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.Jdl_Savelog.Wrap(-1)
        self.Jdl_Savelog.SetFont(wx.Font(12, 70, 90, 92, False, "Arial"))

        fgSizer1.Add(self.Jdl_Savelog, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_Savelog = wx.StaticText(self.Pnl_Savelog, wx.ID_ANY, u"Save your file", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        self.Lbl_Savelog.Wrap(-1)
        fgSizer2.Add(self.Lbl_Savelog, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Fp_Savelog = wx.FilePickerCtrl(self.Pnl_Savelog, wx.ID_ANY, wx.EmptyString, u"Save your file to specified location and name", u"Excel Files(*.xls)|*.xls|Excel-2003(*.xlsx)|*.xlsx|", wx.DefaultPosition, wx.Size( 400,-1 ), wx.FLP_OVERWRITE_PROMPT|wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL)
        fgSizer2.Add(self.Fp_Savelog, 0, wx.ALL, 5)

        fgSizer1.Add(fgSizer2, 1, wx.EXPAND, 5)

        fgSizer222 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer222.SetFlexibleDirection(wx.BOTH)
        fgSizer222.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Cmd_SaveLogDone = wx.Button(self.Pnl_Savelog, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer222.Add(self.Cmd_SaveLogDone, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_SaveLogCancel = wx.Button(self.Pnl_Savelog, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer222.Add(self.Cmd_SaveLogCancel, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer1.Add(fgSizer222, 1, wx.EXPAND, 5)

        self.Pnl_Savelog.SetSizer(fgSizer1)
        self.Pnl_Savelog.Layout()
        fgSizer1.Fit(self.Pnl_Savelog)
        gSizer1.Add(self.Pnl_Savelog, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)
        self.Show()

        # Connect Events`
        self.Cmd_SaveLogDone.Bind(wx.EVT_BUTTON, lambda x:self.SaveToExcels(self.Fp_Savelog.GetPath()))
        self.Cmd_SaveLogCancel.Bind(wx.EVT_BUTTON, lambda x:self.Continues())


    # Virtual event handlers, overide them in your derived class
    def SaveToExcels(self, destination):
        self.MFSaveToExcel(self.CurrentFileSuhu, destination)
        self.SaveLogSuhuActive = True
        self.Hide()

    def Continues(self):
        self.Hide()
        print ' DONE '
        self.SaveLogSuhuActive = True



