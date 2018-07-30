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
## Class Nexus_SaveToText
###########################################################################

class Nexus_SaveToText(wx.Frame):
    def __init__(self, parent ,data):
        self.data = data
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(472, 205), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        fgSizer8 = wx.FlexGridSizer(4, 1, 0, 0)
        fgSizer8.SetFlexibleDirection(wx.BOTH)
        fgSizer8.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Txt_Save_Jdl = wx.StaticText(self, wx.ID_ANY, u"Save Log To Text", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Txt_Save_Jdl.Wrap(-1)
        self.Txt_Save_Jdl.SetFont(wx.Font(14, 74, 90, 92, False, "Arial"))

        fgSizer8.Add(self.Txt_Save_Jdl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_SelectAFolder = wx.StaticText(self, wx.ID_ANY, u"Select A Folder", wx.DefaultPosition, wx.DefaultSize,
                                               0)
        self.Lbl_SelectAFolder.Wrap(-1)
        gbSizer1.Add(self.Lbl_SelectAFolder, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Dir_Folder = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                           wx.Size(350, -1), wx.DIRP_DEFAULT_STYLE)
        gbSizer1.Add(self.Dir_Folder, wx.GBPosition(0, 1), wx.GBSpan(1, 2), wx.ALL, 5)

        self.Lbl_WriteFileName = wx.StaticText(self, wx.ID_ANY, u"The Name of File", wx.DefaultPosition, wx.DefaultSize,
                                               0)
        self.Lbl_WriteFileName.Wrap(-1)
        gbSizer1.Add(self.Lbl_WriteFileName, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_Filename = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(200, -1), 0)
        gbSizer1.Add(self.Txt_Filename, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Lbl_Ext_Save = wx.StaticText(self, wx.ID_ANY, u"* .txt", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Ext_Save.Wrap(-1)
        gbSizer1.Add(self.Lbl_Ext_Save, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer8.Add(gbSizer1, 1, wx.EXPAND, 5)

        fgSizer9 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer9.SetFlexibleDirection(wx.BOTH)
        fgSizer9.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Cmd_SaveOk = wx.Button(self, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer9.Add(self.Cmd_SaveOk, 0, wx.ALL, 5)

        self.Cmd_DoneOk = wx.Button(self, wx.ID_ANY, u"Done", wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer9.Add(self.Cmd_DoneOk, 0, wx.ALL, 5)

        fgSizer8.Add(fgSizer9, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Lbl_Save_Status = wx.StaticText(self, wx.ID_ANY, u"-", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_Save_Status.Wrap(-1)
        self.Lbl_Save_Status.SetFont(wx.Font(16, 74, 90, 90, False, "Arial"))

        fgSizer8.Add(self.Lbl_Save_Status, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(fgSizer8)
        self.Layout()

        self.Centre(wx.BOTH)
        self.Show()

        # Connect Events
        self.Cmd_SaveOk.Bind(wx.EVT_BUTTON, lambda x:self.GoSave())
        self.Cmd_DoneOk.Bind(wx.EVT_BUTTON, lambda x:self.GoDone())

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def GoSave(self):
        if self.Txt_Filename.GetValue() != '':
            try:
                f = open(str(self.Dir_Folder.GetPath())+str(self.Txt_Filename.GetValue())+".txt", "w+")
            except Exception as e:
                print (e)
                self.Lbl_Save_Status.SetLabel("Save Failed!")
            else:
                f.close()
                if len(self.data) != 0:
                    with open(str(self.Dir_Folder.GetPath())+str(self.Txt_Filename.GetValue())+".txt", "w+") as text_file:
                        for item in self.data:
                            text_file.write(str(item))

                    self.Lbl_Save_Status.SetLabel("Save Success!")
                else:
                    self.Lbl_Save_Status.SetLabel("No Data!")

    def GoDone(self):
        self.Close()


