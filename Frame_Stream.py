# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.html
import ConfigParser


###########################################################################
## Class Frame_Stream
###########################################################################

class Frame_Stream(wx.Frame):
    def __init__(self, parent):

        #GET DATA FROM CONFIG FILE
        # IMPORT SETTING
        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.X_TrueSpeed = config.get('Stream Camera Configuration', 'Link')
        #self.Y_TrueSpeed = config.get('Stream Camera Configuration', 'Y_Speed')
        #self.Z_TrueSpeed = config.get('Stream Camera Configuration', 'Z_Speed')

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(624, 478), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        fgSizer1 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer1.SetMinSize(wx.Size(400, 300))
        bSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        self.Jdl_Strm_Cam = wx.StaticText(self, wx.ID_ANY, u"STREAMING CAMERA", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Jdl_Strm_Cam.Wrap(-1)
        bSizer1.Add(self.Jdl_Strm_Cam, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.Lbl_Strm_Link = wx.StaticText(self, wx.ID_ANY, u"Link", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Strm_Link.Wrap(-1)
        bSizer1.Add(self.Lbl_Strm_Link, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Txt_Strm_Link = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.Txt_Strm_Link, 0, wx.ALL | wx.EXPAND, 5)

        self.Cmd_Strm_GO = wx.Button(self, wx.ID_ANY, u"GO", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.Cmd_Strm_GO, 0, wx.ALL, 5)

        self.Cmd_Strm_EXIT = wx.Button(self, wx.ID_ANY, u"EXIT", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.Cmd_Strm_EXIT, 0, wx.ALL, 5)

        fgSizer1.Add(bSizer1, 1, wx.EXPAND, 5)

        self.MyBrowser = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.html.HW_SCROLLBAR_AUTO)
        self.MyBrowser.SetMinSize(wx.Size(600, 400))

        fgSizer1.Add(self.MyBrowser, 0, wx.ALL, 5)

        self.SetSizer(fgSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_ACTIVATE, self.LoadLink)
        self.Cmd_Strm_GO.Bind(wx.EVT_BUTTON, self.GoLink)
        self.Cmd_Strm_EXIT.Bind(wx.EVT_BUTTON, self.Exit)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def LoadLink(self, event):
        event.Skip()

    def GoLink(self, event):
        event.Skip()

    def Exit(self, event):
        event.Skip()


