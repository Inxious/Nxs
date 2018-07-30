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
## Class MyFrame1
###########################################################################

class Mnl_Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(518, 168), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        fgSizer1 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"MANUAL COMMANDS", wx.DefaultPosition, wx.Size(500, -1),
                                           wx.ALIGN_CENTRE)
        self.m_staticText1.Wrap(-1)
        fgSizer1.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_Mnl_Serial = wx.StaticText(self, wx.ID_ANY, u"Serial", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Mnl_Serial.Wrap(-1)
        gbSizer1.Add(self.Lbl_Mnl_Serial, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        Cmb_Mnl_SerialChoices = ['Board 1','Heater','Camera']
        self.Cmb_Mnl_Serial = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Cmb_Mnl_SerialChoices, 0)
        self.Cmb_Mnl_Serial.SetSelection(0)
        gbSizer1.Add(self.Cmb_Mnl_Serial, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Lbl_Mnl_Command = wx.StaticText(self, wx.ID_ANY, u"Command", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Mnl_Command.Wrap(-1)
        gbSizer1.Add(self.Lbl_Mnl_Command, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_Mnl_Ciommand = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(400, -1), 0)
        gbSizer1.Add(self.Txt_Mnl_Ciommand, wx.GBPosition(1, 1), wx.GBSpan(1, 2), wx.ALL, 5)

        self.Cmd_Mnl_Send = wx.Button(self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Cmd_Mnl_Send, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Cmd_Mnl_Reset = wx.Button(self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Cmd_Mnl_Reset, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        fgSizer1.Add(gbSizer1, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.SetSizer(fgSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

        # Connect Events
        Serials = {'Board 1':1,'Heater':2,'Camera':3}

        self.Cmd_Mnl_Send.Bind(wx.EVT_BUTTON, lambda x:self.ManualCmd(str(Serials[self.Cmb_Mnl_Serial.GetString(self.Cmb_Mnl_Serial.GetSelection())]),
                                                             self.Txt_Mnl_Ciommand.GetValue()))
        self.Cmd_Mnl_Reset.Bind(wx.EVT_BUTTON, lambda x:self.OnReset)

        self.Show()

    def __del__(self):
        pass


    # Virtual event handlers, overide them in your derived class

    def OnReset(self):
        self.Txt_Mnl_Ciommand.Clear()


