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
## Class Frame_Images
###########################################################################

class Frame_Images(wx.Frame):
    def __init__(self, parent):

        #GET DATA FROM CONFIG FILE
        # IMPORT SETTING
        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        self.StreamType = config.get('Stream Camera Configuration', 'Type')
        if self.StreamType == '' or len(self.StreamType) == 0:
            pass
        elif self.StreamType == 'Link':
            self.LinkStream = config.get('Stream Camera Configuration', 'Link')
        elif self.StreamType == 'Image':
            self.ImageStream = config.get('Stream Camera Configuration', 'Image')

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(730, 665), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        fgSizer2 = wx.FlexGridSizer(4, 1, 0, 0)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer2.SetMinSize(wx.Size(600, -1))
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer2.SetMinSize(wx.Size(600, -1))
        self.Lbl_Link = wx.StaticText(self, wx.ID_ANY, u"Link", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Link.Wrap(-1)
        bSizer2.Add(self.Lbl_Link, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Txt_Link = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(450, -1), 0)
        bSizer2.Add(self.Txt_Link, 0, wx.ALL | wx.EXPAND, 5)

        self.Cmd_GoLink = wx.Button(self, wx.ID_ANY, u"Go", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.Cmd_GoLink, 0, wx.ALL, 5)

        self.Cmd_RefreshPg = wx.Button(self, wx.ID_ANY, u"Refresh Page", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer2.Add(self.Cmd_RefreshPg, 0, wx.ALL, 5)


        fgSizer2.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.Jdl_Img = wx.StaticText(self, wx.ID_ANY, u"Browse Image", wx.Point(3, 3), wx.DefaultSize, 0)
        self.Jdl_Img.Wrap(-1)
        bSizer3.Add(self.Jdl_Img, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Dir_Img = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition,
                                         wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        bSizer3.Add(self.Dir_Img, 0, wx.ALL | wx.EXPAND, 5)

        fgSizer2.Add(bSizer3, 1, wx.EXPAND, 5)

        self.MyBrowser2 = wx.html.HtmlWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                             wx.html.HW_SCROLLBAR_AUTO)
        self.MyBrowser2.SetMinSize(wx.Size(700, 550))

        fgSizer2.Add(self.MyBrowser2, 0, wx.ALL, 5)

        self.SetSizer(fgSizer2)
        self.Layout()

        self.Centre(wx.BOTH)


        #Constant
        self.start_image = '.\images\Start_Image.png'

        # Connect Events
        self.Bind(wx.EVT_ACTIVATE, lambda x: self.LoadStarterImage() )
        self.Cmd_GoLink.Bind(wx.EVT_BUTTON, lambda x: self.GoLink(self.Txt_Link.GetValue()))
        self.Cmd_RefreshPg.Bind(wx.EVT_BUTTON, lambda x: self.LoadStarterImage())

        self.Dir_Img.Bind(wx.EVT_FILEPICKER_CHANGED, lambda x: self.GoOpenImage(self.Dir_Img.GetPath()))

        self.Show()


    # Virtual event handlers, overide them in your derived class
    def LoadStarterImage(self):
        if self.StreamType != "" or len(self.StreamType) != 0:
            if self.StreamType == 'Link' and self.LinkStream != '':
                self.GoLink(self.LinkStream)
            elif self.StreamType == 'Image' and self.ImageStream != '':
                self.GoOpenImage(self.ImageStream)
            else:
                self.MyBrowser2.SetPage(self.GenerateHTML(1, self.start_image))
        else:
            self.MyBrowser2.SetPage(self.GenerateHTML(1,self.start_image))

    def GoLink(self, linkpage):
        print linkpage
        if linkpage in ('',None):
            return
        self.MyBrowser2.LoadPage(linkpage)

    def GoOpenImage(self , linkpage):
        print linkpage
        self.MyBrowser2.SetFocus()
        try:
            self.MyBrowser2.SetPage(self.GenerateHTML(1, linkpage))
            self.Txt_Link.SetValue(str(linkpage))
        except Exception as e:
            print (e)

    def OneImageCloseFrame(self):
        self.Hide()

