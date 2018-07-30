#==================== MAIN FORM ==================#

import wx
import wx.dataview as DV
import  ConfigParser
import Frame_SaveToText
import xlsxwriter

#subFrame
#import TransFrame as TF


class MainFrame( wx.Frame ):

    def __init__(self,parent):
        self.Frames(parent,"NEXUS")

        # IMPORT SETTING
        # LOAD DATABASE SETTING FROM CONFIG.txt
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        try:
            self.Standby_Start = bool(config.get('Heater Configuration', 'standby'))
            print self.Standby_Start
        except Exception:
            self.Standby_Start = False

        try:
            self.MaxLimitTemp = config.get('Heater Configuration', 'max_value')
        except Exception:
            self.MaxLimitTemp = 38
        else:
            self.MaxLimitTemp = config.get('Heater Configuration', 'max_value')

        try:
            self.MinLimitTemp = config.get('Heater Configuration', 'min_value')
        except Exception:
            self.MaxLimitTemp = 36
        else:
            self.MinLimitTemp = config.get('Heater Configuration', 'min_value')

        try:
            int(self.Serial_Mode)
        except Exception as e:
            print e
        else:
            if int(self.Serial_Mode) == 1: # AUTO CONNECT
                self.CAutoConnect(1)
            elif int(self.Serial_Mode) == 2: # JUST SET THE VALUE
                self.CAutoConnect(2)






        #Anti INFINITY
        self.Vals = True
        self.Events()


    def Frames(self,parent,title):
        wx.Frame.__init__( self, parent, title = title,
                           size = wx.Size(900,680))

        #=== INSIDE ===#
        self.MenuBars()
        self.SetMenuBar( self.MenuBar )

        Grids = wx.FlexGridSizer( 2, 2, 0, 0 )
        Grids.SetFlexibleDirection( wx.BOTH )

        self.Panels1(self)
        Grids.Add( self.Pnl_MF_Ctrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        SubGrids = wx.FlexGridSizer( 2, 1, 0, 0 )
        SubGrids.SetFlexibleDirection( wx.BOTH )
        Grids.Add( SubGrids, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )

        self.Panels2(self)
        SubGrids.Add( self.Panel2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.Panels3(self)
        SubGrids.Add( self.Panel3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.StatBar = wx.StatusBar( self )
        self.SetStatusBar(self.StatBar)
        self.SetSizer( Grids )
        self.Layout()
        self.Centre( wx.BOTH )
        Grids.Fit( self )
        #==============#
        self.Show()

    def MenuBars(self):
        #======================================
        self.MenuBar = wx.MenuBar( 0 )
        self.Menu1 = wx.Menu()

        self.SubMenu3_1 = wx.MenuItem(self.Menu1, wx.ID_ANY, u"Speed Setting", wx.EmptyString, wx.ITEM_NORMAL)
        self.Menu1.Append(self.SubMenu3_1)

        self.MenuBar.Append( self.Menu1, u"Settings" )

        #======================================
        self.Menu2 = wx.Menu()

        self.SubMenu2= wx.MenuItem(self.Menu2, wx.ID_ANY, u"Manual Command", wx.EmptyString, wx.ITEM_NORMAL)
        self.Menu2.Append(self.SubMenu2)

        self.SubMenu_Stream = wx.MenuItem(self.Menu2, wx.ID_ANY, u"Stream Window", wx.EmptyString, wx.ITEM_NORMAL)
        self.Menu2.Append(self.SubMenu_Stream)

        self.MenuBar.Append(self.Menu2, u"App")


    def Panels1(self,parent):
        self.Pnl_MF_Ctrl = wx.Panel(parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(510, 620),
                          style=wx.TAB_TRAVERSAL)

        MainSizer = wx.FlexGridSizer(3, 1, 0, 0)
        MainSizer.SetFlexibleDirection(wx.BOTH)
        MainSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.SubPanlelProces(self.Pnl_MF_Ctrl)
        MainSizer.Add(self.Pnl_MF_Prc, 1, wx.EXPAND | wx.ALL, 5)
        self.FrameData(1)

        self.SubPanelConfig(self.Pnl_MF_Ctrl)
        MainSizer.Add(self.Pnl_MF_Cfg, 1, wx.EXPAND | wx.ALL, 5)

        self.PanelSuhu(self.Pnl_MF_Ctrl)
        MainSizer.Add(self.Pnl_MF_Temperature, 1, wx.EXPAND | wx.ALL, 10)

        self.Pnl_MF_Ctrl.SetSizer(MainSizer)
        self.Pnl_MF_Ctrl.Layout()
        #==============#

    def Panels2(self,parent):
        self.Panel2 = wx.Panel( parent , size = wx.Size(350,200) )
        self.Panel2.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        #=== INNER FUNCTION ===#

        def Container(parent,slot): #KONEKSI
            self.SubPanel = wx.Panel( parent , size = wx.Size(350,150) )

            Grids = wx.FlexGridSizer( 4, 3, 0, 0 )
            Grids.SetFlexibleDirection( wx.BOTH )

            self.LblPort = wx.StaticText(self.SubPanel , label = "Port            = ")
            Grids.Add( self.LblPort, 0, wx.ALL|wx.ALIGN_CENTER, 5 )
            if slot == 1:
                CmbPortChoices = self.PortList
                self.CmbPort1 = wx.ComboBox( self.SubPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120,30), CmbPortChoices, 0 )
                Grids.Add( self.CmbPort1, 0, wx.ALL|wx.ALIGN_CENTER, 5 )


                self.CmdConn1 = wx.Button(self.SubPanel , label = "CONNECT" , size = wx.Size(90,30))
                Grids.Add( self.CmdConn1, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            elif slot == 2:
                CmbPortChoices = self.PortList
                self.CmbPort2 = wx.ComboBox( self.SubPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120,30), CmbPortChoices, 0 )
                Grids.Add( self.CmbPort2, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.CmdConn2 = wx.Button(self.SubPanel , label = "CONNECT" , size = wx.Size(90,30))
                Grids.Add( self.CmdConn2, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            elif slot == 3:
                CmbPortChoices = self.PortList
                self.CmbPort3 = wx.ComboBox( self.SubPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120,30), CmbPortChoices, 0 )
                Grids.Add( self.CmbPort3, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.CmdConn3 = wx.Button(self.SubPanel , label = "CONNECT" , size = wx.Size(90,30))
                Grids.Add( self.CmdConn3, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            self.LblBRate = wx.StaticText(self.SubPanel , label = "BaudRate   = ")
            Grids.Add( self.LblBRate, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            if slot == 1:
                CmbBRateChoices = ['9600', '115200']
                self.CmbBRate1 = wx.ComboBox( self.SubPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120,30), CmbBRateChoices, 0 )
                Grids.Add( self.CmbBRate1, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.CmdDisConn1 = wx.Button(self.SubPanel , label = "DISCONNECT" , size = wx.Size(90,30))
                Grids.Add( self.CmdDisConn1, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            if slot == 2:
                CmbBRateChoices = ['9600', '115200']
                self.CmbBRate2 = wx.ComboBox( self.SubPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120,30), CmbBRateChoices, 0 )
                Grids.Add( self.CmbBRate2, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.CmdDisConn2 = wx.Button(self.SubPanel , label = "DISCONNECT" , size = wx.Size(90,30))
                Grids.Add( self.CmdDisConn2, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            if slot == 3:
                CmbBRateChoices = ['9600', '115200']
                self.CmbBRate3 = wx.ComboBox( self.SubPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(120,30), CmbBRateChoices, 0 )
                Grids.Add( self.CmbBRate3, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.CmdDisConn3 = wx.Button(self.SubPanel , label = "DISCONNECT" , size = wx.Size(90,30))
                Grids.Add( self.CmdDisConn3, 0, wx.ALL|wx.ALIGN_CENTER, 5 )



            #======== LABEL ======================================================================================

            self.LblComNows = wx.StaticText(self.SubPanel , label = " COM Port ")
            Grids.Add( self.LblComNows, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            self.LblStats = wx.StaticText(self.SubPanel , label = " STATUS ")
            Grids.Add( self.LblStats, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            if slot == 1:

                Grids.Add(0, 0, 0)

                self.LblComNow1 = wx.StaticText(self.SubPanel , label = " - ")
                Grids.Add( self.LblComNow1, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.LblStat1 = wx.StaticText(self.SubPanel , label = " - ")
                Grids.Add( self.LblStat1, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            if slot == 2:

                Grids.Add(0, 0, 0)

                self.LblComNow2 = wx.StaticText(self.SubPanel , label = " - ")
                Grids.Add( self.LblComNow2, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.LblStat2 = wx.StaticText(self.SubPanel , label = " - ")
                Grids.Add( self.LblStat2, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

            if slot == 3:

                Grids.Add(0, 0, 0)

                self.LblComNow3 = wx.StaticText(self.SubPanel , label = " - ")
                Grids.Add( self.LblComNow3, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

                self.LblStat3 = wx.StaticText(self.SubPanel , label = " - ")
                Grids.Add( self.LblStat3, 0, wx.ALL|wx.ALIGN_CENTER, 5 )



            self.SubPanel.SetSizer( Grids )
            self.SubPanel.Centre( wx.BOTH )
            Grids.Fit( self.SubPanel )

        #======================#

        #=== PANEL ====#
        Grids = wx.FlexGridSizer( 4, 1, 0, 0 )
        Grids.SetFlexibleDirection( wx.BOTH )

        self.Pnl_MF_Ttl_Con = wx.Panel(self.Panel2, wx.ID_ANY, wx.DefaultPosition, wx.Size(340, -1),
                                      wx.TAB_TRAVERSAL)
        self.Pnl_MF_Ttl_Con.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.Lbl_MF_Ttl_Con = wx.StaticText(self.Pnl_MF_Ttl_Con, wx.ID_ANY, u"CONNECTION", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.Lbl_MF_Ttl_Con.Wrap(-1)
        self.Lbl_MF_Ttl_Con.SetFont(wx.Font(9, 74, 90, 92, False, "Arial Black"))

        bSizer7.Add(self.Lbl_MF_Ttl_Con, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_MF_Ttl_Con.SetSizer(bSizer7)
        self.Pnl_MF_Ttl_Con.Layout()
        bSizer7.Fit(self.Pnl_MF_Ttl_Con)
        Grids.Add(self.Pnl_MF_Ttl_Con, 1, wx.EXPAND | wx.ALL, 5)

        #-- NOTEBOOK --#
        self.NbConn = wx.Notebook( self.Panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        #-PAGE 1
        Container(self.NbConn,1)
        self.NbConn.AddPage( self.SubPanel, u"BOARD 1", True )

        #-PAGE 2
        Container(self.NbConn,2)
        self.NbConn.AddPage( self.SubPanel, u"HEATER", False )

        # -PAGE 2
        Container(self.NbConn, 3)
        self.NbConn.AddPage(self.SubPanel, u"CAMERA", False)

        Grids.Add( self.NbConn, 0, wx.EXPAND |wx.ALL|wx.ALIGN_CENTER, 5 )
        #--------------#

        self.Panel2.SetSizer( Grids )
        self.Panel2.Centre( wx.BOTH )
        Grids.Fit( self.Panel2 )
        #==============#

    def Panels3(self,parent):
        self.Panel3 = wx.Panel( parent , size = wx.Size(350,410) )
        self.Panel3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        #=== PANEL ====#
        Grids = wx.FlexGridSizer( 2, 1, 0, 0 )
        Grids.SetFlexibleDirection( wx.BOTH )
        Grids.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        SubGrids = wx.FlexGridSizer( 2, 1, 0, 0 )
        SubGrids.SetFlexibleDirection( wx.BOTH )
        SubGrids.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.Pnl_MF_Ttl_Log = wx.Panel(self.Panel3, wx.ID_ANY, wx.DefaultPosition, wx.Size(490, -1),
                                      wx.TAB_TRAVERSAL)
        self.Pnl_MF_Ttl_Log.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.Lbl_MF_Ttl_Log = wx.StaticText(self.Pnl_MF_Ttl_Log, wx.ID_ANY, u"LOG COMMAND", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.Lbl_MF_Ttl_Log.Wrap(-1)
        self.Lbl_MF_Ttl_Log.SetFont(wx.Font(9, 74, 90, 92, False, "Arial Black"))

        bSizer7.Add(self.Lbl_MF_Ttl_Log, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_MF_Ttl_Log.SetSizer(bSizer7)
        self.Pnl_MF_Ttl_Log.Layout()
        bSizer7.Fit(self.Pnl_MF_Ttl_Log)
        SubGrids.Add(self.Pnl_MF_Ttl_Log, 1, wx.EXPAND | wx.ALL, 5)

        LbLogChoices = []
        self.LbLog = wx.ListBox( self.Panel3, wx.ID_ANY, wx.DefaultPosition, wx.Size(330,250), LbLogChoices, 0 )
        SubGrids.Add( self.LbLog, 0, wx.ALL|wx.ALIGN_CENTER, 5 )


        Grids.Add( SubGrids, 1, wx.EXPAND, 5 )

        SubGrids2 = wx.FlexGridSizer( 1, 2, 0, 0 )
        SubGrids2.SetFlexibleDirection( wx.BOTH )
        SubGrids2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.Cmd_LB_Clear = wx.Button( self.Panel3, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
        SubGrids2.Add( self.Cmd_LB_Clear, 0, wx.ALL|wx.ALIGN_CENTER, 5 )

        self.CmdSave = wx.Button( self.Panel3, wx.ID_ANY, u"Save To Txt", wx.DefaultPosition, wx.DefaultSize, 0 )
        SubGrids2.Add( self.CmdSave, 0, wx.ALL|wx.ALIGN_CENTER, 5 )


        Grids.Add( SubGrids2, 1, wx.EXPAND, 5 )


        Grids.Fit( self.Panel3 )
        self.Panel3.SetSizer( Grids )
        self.Panel3.Centre( wx.BOTH )
        #==============#

    def SubPanlelProces(self, parent):

        self.Pnl_MF_Prc = wx.Panel( parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 73),
                          style=wx.TAB_TRAVERSAL)

        self.Pnl_MF_Prc.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        fgSizer9 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer9.SetFlexibleDirection(wx.BOTH)
        fgSizer9.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.Pnl_MF_Ttl_PL = wx.Panel(self.Pnl_MF_Prc, wx.ID_ANY, wx.DefaultPosition, wx.Size(490, -1), wx.TAB_TRAVERSAL)
        self.Pnl_MF_Ttl_PL.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer8 = wx.BoxSizer(wx.VERTICAL)

        self.Lbl_MF_PL_Ttl = wx.StaticText(self.Pnl_MF_Ttl_PL, wx.ID_ANY, u"PROCES LIST", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.Lbl_MF_PL_Ttl.Wrap(-1)
        self.Lbl_MF_PL_Ttl.SetFont(wx.Font(9, 74, 90, 92, False, "Arial Black"))

        bSizer8.Add(self.Lbl_MF_PL_Ttl, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_MF_Ttl_PL.SetSizer(bSizer8)
        self.Pnl_MF_Ttl_PL.Layout()
        bSizer7.Add(self.Pnl_MF_Ttl_PL, 1, wx.EXPAND | wx.ALL, 5)

        fgSizer9.Add(bSizer7, 1, wx.EXPAND, 5)

        gbSizer4 = wx.GridBagSizer(0, 0)
        gbSizer4.SetFlexibleDirection(wx.BOTH)
        gbSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_MF_PL_Prc = wx.StaticText(self.Pnl_MF_Prc, wx.ID_ANY, u"Proces", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_MF_PL_Prc.Wrap(-1)
        gbSizer4.Add(self.Lbl_MF_PL_Prc, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        Cmb_MF_PrcChoices = []
        self.Cmb_MF_Prc = wx.ComboBox(self.Pnl_MF_Prc, wx.ID_ANY, u"-- Choose --", wx.DefaultPosition, wx.Size(230, -1),
                                      Cmb_MF_PrcChoices, 0)
        gbSizer4.Add(self.Cmb_MF_Prc, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Cmd_MF_Prc_Detail = wx.Button(self.Pnl_MF_Prc, wx.ID_ANY, u"Detail", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer4.Add(self.Cmd_MF_Prc_Detail, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Cmd_MF_Prc_Refresh = wx.Button(self.Pnl_MF_Prc, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer4.Add(self.Cmd_MF_Prc_Refresh, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer9.Add(gbSizer4, 1, wx.EXPAND, 5)

        self.Pnl_MF_Prc.SetSizer(fgSizer9)
        self.Pnl_MF_Prc.Layout()

    def SubPanelConfig(self, parent):

        self.Pnl_MF_Cfg = wx.Panel( parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 258),
                          style=wx.TAB_TRAVERSAL)

        self.Pnl_MF_Cfg.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        MainSizer = wx.FlexGridSizer(1, 2, 0, 0)
        MainSizer.SetFlexibleDirection(wx.BOTH)
        MainSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer8 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer8.SetFlexibleDirection(wx.BOTH)
        fgSizer8.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Pnl_MF_Ttl_CL = wx.Panel(self.Pnl_MF_Cfg, wx.ID_ANY, wx.DefaultPosition, wx.Size(490,-1), wx.TAB_TRAVERSAL)
        self.Pnl_MF_Ttl_CL.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.Lbl_MF_Ttl_CL = wx.StaticText(self.Pnl_MF_Ttl_CL, wx.ID_ANY, u"CONFIG LIST", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.Lbl_MF_Ttl_CL.Wrap(-1)
        self.Lbl_MF_Ttl_CL.SetFont(wx.Font(9, 74, 90, 92, False, "Arial Black"))

        bSizer7.Add(self.Lbl_MF_Ttl_CL, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_MF_Ttl_CL.SetSizer(bSizer7)
        self.Pnl_MF_Ttl_CL.Layout()
        bSizer7.Fit(self.Pnl_MF_Ttl_CL)
        fgSizer8.Add(self.Pnl_MF_Ttl_CL, 1, wx.EXPAND | wx.ALL, 5)

        fgSizer9 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer9.SetFlexibleDirection(wx.BOTH)
        fgSizer9.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Dv_MF_MovementList = wx.dataview.DataViewListCtrl(self.Pnl_MF_Cfg, wx.ID_ANY, wx.DefaultPosition, wx.Size(373, 200),0)
        fgSizer9.Add(self.Dv_MF_MovementList, 0, wx.ALL, 5)

        SubSizer = wx.BoxSizer(wx.VERTICAL)

        #self.Cmd_MF_Details = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"See Details", wx.DefaultPosition, wx.DefaultSize, 0)
        #SubSizer.Add(self.Cmd_MF_Details, 0, wx.ALL, 5)

        self.Cmd_MF_Run = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"RUN ALL", wx.DefaultPosition, wx.DefaultSize, 0)
        SubSizer.Add(self.Cmd_MF_Run, 0, wx.ALL|wx.EXPAND, 5)

        #self.Cmd_MF_RunSelect = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"Run Selected", wx.DefaultPosition, wx.DefaultSize, 0)
        #SubSizer.Add(self.Cmd_MF_RunSelect, 0, wx.ALL, 5)

        self.Cmd_MF_RunChkd = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"RUN CHECKED", wx.DefaultPosition, wx.DefaultSize, 0)
        SubSizer.Add(self.Cmd_MF_RunChkd, 0, wx.ALL|wx.EXPAND, 5)

        self.Cmd_MF_Clear = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"CLEAR", wx.DefaultPosition, wx.DefaultSize, 0)
        SubSizer.Add(self.Cmd_MF_Clear, 0, wx.ALL|wx.EXPAND, 5)

        self.Cmd_MF_All = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"LIST ALL", wx.DefaultPosition, wx.DefaultSize, 0)
        SubSizer.Add(self.Cmd_MF_All, 0, wx.ALL|wx.EXPAND, 5)

        #======================= ADD By Reza V2.3.6

        self.Cmd_MF_ChkAll = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"CHECK ALL", wx.DefaultPosition, wx.DefaultSize, 0)
        SubSizer.Add(self.Cmd_MF_ChkAll, 0, wx.ALL | wx.EXPAND, 5)

        self.Cmd_MF_UnChkAll = wx.Button(self.Pnl_MF_Cfg, wx.ID_ANY, u"UNCHECK ALL", wx.DefaultPosition, wx.DefaultSize, 0)
        SubSizer.Add(self.Cmd_MF_UnChkAll, 0, wx.ALL | wx.EXPAND, 5)


        #============================================


        fgSizer9.Add(SubSizer, 1, wx.EXPAND, 5)

        fgSizer8.Add(fgSizer9, 1, wx.EXPAND, 5)

        MainSizer.Add(fgSizer8, 1, wx.EXPAND, 5)

        self.Pnl_MF_Cfg.SetSizer(MainSizer)
        self.Pnl_MF_Cfg.Layout()

        #======== TABLE SETTING ===============
        self.Dv_MF_MovementList.AppendToggleColumn("Run", 1, width=50)
        self.Dv_MF_MovementList.AppendTextColumn("Config Name", 2, width=197)
        self.Dv_MF_MovementList.AppendTextColumn("Status", 3, width=120)

        #======================================

    def PanelSuhu(self, parent):

        self.Pnl_MF_Temperature = wx.Panel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Pnl_MF_Temperature.SetMinSize(wx.Size(500, -1))

        fgSizer16 = wx.FlexGridSizer(3, 1, 0, 0)
        fgSizer16.SetFlexibleDirection(wx.BOTH)
        fgSizer16.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer16.SetMinSize(wx.Size(500, -1))
        self.Pnl_MF_Temp_Judul = wx.Panel(self.Pnl_MF_Temperature, wx.ID_ANY, wx.DefaultPosition, wx.Size(500, -1),
                                          wx.TAB_TRAVERSAL)
        self.Pnl_MF_Temp_Judul.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        bSizer10.SetMinSize(wx.Size(250, -1))
        self.Txt_MF_TempJudul = wx.StaticText(self.Pnl_MF_Temp_Judul, wx.ID_ANY, u"TEMPERATURE", wx.DefaultPosition,
                                              wx.DefaultSize, 0)
        self.Txt_MF_TempJudul.Wrap(-1)
        self.Txt_MF_TempJudul.SetFont(wx.Font(9, 74, 90, 92, False, "Arial Black"))
        self.Txt_MF_TempJudul.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer10.Add(self.Txt_MF_TempJudul, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_MF_Temp_Judul.SetSizer(bSizer10)
        self.Pnl_MF_Temp_Judul.Layout()
        fgSizer16.Add(self.Pnl_MF_Temp_Judul, 1,
                      wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)

        fgSizer18 = wx.FlexGridSizer(1, 2, 0, 0)
        fgSizer18.SetFlexibleDirection(wx.BOTH)
        fgSizer18.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer18.SetMinSize(wx.Size(500, -1))
        fgSizer11 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer11.SetFlexibleDirection(wx.BOTH)
        fgSizer11.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Pnl_MF_MainSubTemp = wx.Panel(self.Pnl_MF_Temperature, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1),
                                           wx.TAB_TRAVERSAL)
        gSizer8 = wx.GridSizer(1, 1, 0, 0)

        gSizer8.SetMinSize(wx.Size(250, -1))
        self.Pnl_MF_FrameTemp = wx.Panel(self.Pnl_MF_MainSubTemp, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1),
                                         wx.TAB_TRAVERSAL)
        self.Pnl_MF_FrameTemp.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        fgSizer12 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer12.SetFlexibleDirection(wx.BOTH)
        fgSizer12.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Pnl_MF_Sub1Temp = wx.Panel(self.Pnl_MF_FrameTemp, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TAB_TRAVERSAL)
        self.Pnl_MF_Sub1Temp.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT))

        gSizer9 = wx.GridSizer(1, 1, 0, 0)

        gSizer9.SetMinSize(wx.Size(240, -1))
        self.Lbl_MF_Temp_Value = wx.StaticText(self.Pnl_MF_Sub1Temp, wx.ID_ANY, u"-", wx.DefaultPosition,
                                               wx.Size(150, 100), wx.ALIGN_CENTRE)
        self.Lbl_MF_Temp_Value.Wrap(-1)
        self.Lbl_MF_Temp_Value.SetFont(wx.Font(48, 72, 90, 92, False, "Times New Roman"))
        self.Lbl_MF_Temp_Value.SetForegroundColour(wx.Colour(255, 255, 0))

        gSizer9.Add(self.Lbl_MF_Temp_Value, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Pnl_MF_Sub1Temp.SetSizer(gSizer9)
        self.Pnl_MF_Sub1Temp.Layout()
        gSizer9.Fit(self.Pnl_MF_Sub1Temp)
        fgSizer12.Add(self.Pnl_MF_Sub1Temp, 1, wx.EXPAND | wx.ALL, 5)

        self.Pnl_MF_Sub2Temp = wx.Panel(self.Pnl_MF_FrameTemp, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                        wx.TAB_TRAVERSAL)
        self.Pnl_MF_Sub2Temp.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTIONTEXT))

        gSizer11 = wx.GridSizer(1, 1, 0, 0)

        gSizer11.SetMinSize(wx.Size(240, -1))
        self.Lbl_MF_Temp_Type = wx.StaticText(self.Pnl_MF_Sub2Temp, wx.ID_ANY, u"CELCIUS", wx.DefaultPosition,
                                              wx.DefaultSize, wx.ALIGN_CENTRE)
        self.Lbl_MF_Temp_Type.Wrap(-1)
        self.Lbl_MF_Temp_Type.SetFont(wx.Font(24, 72, 90, 92, False, "Times New Roman"))
        self.Lbl_MF_Temp_Type.SetForegroundColour(wx.Colour(255, 255, 0))

        gSizer11.Add(self.Lbl_MF_Temp_Type, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Pnl_MF_Sub2Temp.SetSizer(gSizer11)
        self.Pnl_MF_Sub2Temp.Layout()
        gSizer11.Fit(self.Pnl_MF_Sub2Temp)
        fgSizer12.Add(self.Pnl_MF_Sub2Temp, 1, wx.EXPAND | wx.ALL, 5)

        self.Pnl_MF_FrameTemp.SetSizer(fgSizer12)
        self.Pnl_MF_FrameTemp.Layout()
        gSizer8.Add(self.Pnl_MF_FrameTemp, 1, wx.EXPAND | wx.ALL, 0)

        self.Pnl_MF_MainSubTemp.SetSizer(gSizer8)
        self.Pnl_MF_MainSubTemp.Layout()
        fgSizer11.Add(self.Pnl_MF_MainSubTemp, 1,
                      wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        fgSizer18.Add(fgSizer11, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer14 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer14.SetFlexibleDirection(wx.BOTH)
        fgSizer14.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Pnl_MF_Timer = wx.Panel(self.Pnl_MF_Temperature, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1),
                                     wx.TAB_TRAVERSAL)
        fgSizer15 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer15.SetFlexibleDirection(wx.BOTH)
        fgSizer15.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        fgSizer15.SetMinSize(wx.Size(250, -1))
        self.Pnl_MF_Timer_Lbl = wx.Panel(self.Pnl_MF_Timer, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1),
                                         wx.TAB_TRAVERSAL)
        self.Pnl_MF_Timer_Lbl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer11 = wx.BoxSizer(wx.VERTICAL)

        self.Lbl_MF_TimerTemp = wx.StaticText(self.Pnl_MF_Timer_Lbl, wx.ID_ANY, u"LIMIT", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.Lbl_MF_TimerTemp.Wrap(-1)
        self.Lbl_MF_TimerTemp.SetFont(wx.Font(9, 74, 90, 92, False, "Arial"))

        bSizer11.Add(self.Lbl_MF_TimerTemp, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_MF_Timer_Lbl.SetSizer(bSizer11)
        self.Pnl_MF_Timer_Lbl.Layout()
        fgSizer15.Add(self.Pnl_MF_Timer_Lbl, 1, wx.EXPAND | wx.ALL, 0)

        self.Pnl_MF_Timer_Value = wx.Panel(self.Pnl_MF_Timer, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, 70),
                                           wx.TAB_TRAVERSAL)
        gSizer15 = wx.GridSizer(1, 1, 0, 0)

        gSizer15.SetMinSize(wx.Size(250, -1))
        gbSizer5 = wx.GridBagSizer(0, 0)
        gbSizer5.SetFlexibleDirection(wx.BOTH)
        gbSizer5.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Lbl_MF_Temp_Time_Value = wx.StaticText(self.Pnl_MF_Timer_Value, wx.ID_ANY, u"MAX", wx.DefaultPosition,
                                                    wx.DefaultSize, 0)
        self.Lbl_MF_Temp_Time_Value.Wrap(-1)
        gbSizer5.Add(self.Lbl_MF_Temp_Time_Value, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Lbl_MF_Temp_Time_Remaining = wx.StaticText(self.Pnl_MF_Timer_Value, wx.ID_ANY, u"MIN",
                                                        wx.DefaultPosition, wx.DefaultSize, 0)
        self.Lbl_MF_Temp_Time_Remaining.Wrap(-1)
        gbSizer5.Add(self.Lbl_MF_Temp_Time_Remaining, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_Max_Temp = wx.TextCtrl(self.Pnl_MF_Timer_Value, wx.ID_ANY, str(self.MaxLimitTemp), wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        gbSizer5.Add(self.Txt_Max_Temp, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Txt_Min_Temp = wx.TextCtrl(self.Pnl_MF_Timer_Value, wx.ID_ANY, str(self.MinLimitTemp), wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        gbSizer5.Add(self.Txt_Min_Temp, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Cmd_SET_Temp = wx.Button(self.Pnl_MF_Timer_Value, wx.ID_ANY,u'SET', wx.DefaultPosition,
                                      wx.Size(40, 40), 0)
        gbSizer5.Add(self.Cmd_SET_Temp, wx.GBPosition(0, 2), wx.GBSpan(2, 1), wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)

        gSizer15.Add(gbSizer5, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Pnl_MF_Timer_Value.SetSizer(gSizer15)
        self.Pnl_MF_Timer_Value.Layout()
        fgSizer15.Add(self.Pnl_MF_Timer_Value, 1, wx.EXPAND | wx.ALL, 0)

        self.Pnl_MF_Timer.SetSizer(fgSizer15)
        self.Pnl_MF_Timer.Layout()
        fgSizer14.Add(self.Pnl_MF_Timer, 1, wx.EXPAND | wx.ALL, 5)

        self.Pnl_MF_Status = wx.Panel(self.Pnl_MF_Temperature, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                      wx.TAB_TRAVERSAL)
        fgSizer19 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer19.SetFlexibleDirection(wx.BOTH)
        fgSizer19.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Pnl_MF_Status_Lbl = wx.Panel(self.Pnl_MF_Status, wx.ID_ANY, wx.DefaultPosition, wx.Size(250, -1),
                                          wx.TAB_TRAVERSAL)
        self.Pnl_MF_Status_Lbl.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        bSizer13 = wx.BoxSizer(wx.VERTICAL)

        bSizer13.SetMinSize(wx.Size(250, -1))
        self.m_staticText44 = wx.StaticText(self.Pnl_MF_Status_Lbl, wx.ID_ANY, u"STATUS", wx.DefaultPosition,
                                            wx.DefaultSize, 0)
        self.m_staticText44.Wrap(-1)
        self.m_staticText44.SetFont(wx.Font(9, 74, 90, 92, False, "Arial"))

        bSizer13.Add(self.m_staticText44, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Pnl_MF_Status_Lbl.SetSizer(bSizer13)
        self.Pnl_MF_Status_Lbl.Layout()
        fgSizer19.Add(self.Pnl_MF_Status_Lbl, 1, wx.EXPAND | wx.ALL, 0)

        self.Pnl_MF_Status_Value = wx.Panel(self.Pnl_MF_Status, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.TAB_TRAVERSAL)
        gSizer16 = wx.GridSizer(1, 1, 0, 0)

        fgSizer20 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer20.SetFlexibleDirection(wx.BOTH)
        fgSizer20.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Pnl_MF_Status_Sub = wx.Panel(self.Pnl_MF_Status_Value, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                          wx.TAB_TRAVERSAL)
        self.Pnl_MF_Status_Sub.SetMinSize(wx.Size(250, -1))

        bSizer14 = wx.BoxSizer(wx.VERTICAL)

        bSizer14.SetMinSize(wx.Size(250, -1))
        self.Lbl_MF_Temp_Status = wx.StaticText(self.Pnl_MF_Status_Sub, wx.ID_ANY, u"-", wx.DefaultPosition,
                                                wx.DefaultSize, 0)
        self.Lbl_MF_Temp_Status.Wrap(-1)
        self.Lbl_MF_Temp_Status.SetFont(wx.Font(12, 74, 90, 92, False, "Calibri"))

        bSizer14.Add(self.Lbl_MF_Temp_Status, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.Pnl_MF_Status_Sub.SetSizer(bSizer14)
        self.Pnl_MF_Status_Sub.Layout()
        bSizer14.Fit(self.Pnl_MF_Status_Sub)
        fgSizer20.Add(self.Pnl_MF_Status_Sub, 1, wx.EXPAND | wx.ALL, 0)

        gSizer16.Add(fgSizer20, 1, wx.EXPAND, 5)

        self.Pnl_MF_Status_Value.SetSizer(gSizer16)
        self.Pnl_MF_Status_Value.Layout()
        gSizer16.Fit(self.Pnl_MF_Status_Value)
        fgSizer19.Add(self.Pnl_MF_Status_Value, 1, wx.EXPAND | wx.ALL, 5)

        self.Pnl_MF_Status.SetSizer(fgSizer19)
        self.Pnl_MF_Status.Layout()
        fgSizer19.Fit(self.Pnl_MF_Status)
        fgSizer14.Add(self.Pnl_MF_Status, 1, wx.EXPAND | wx.ALL, 5)

        fgSizer18.Add(fgSizer14, 1, wx.EXPAND, 5)

        fgSizer16.Add(fgSizer18, 1, wx.EXPAND, 5)

        self.Pnl_MF_Temp_Button_Control = wx.Panel(self.Pnl_MF_Temperature, wx.ID_ANY, wx.DefaultPosition,
                                                   wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Pnl_MF_Temp_Button_Control.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_INACTIVECAPTION))

        gSizer17 = wx.GridSizer(1, 4, 0, 0)

        self.Cmd_MF_Temp_ON = wx.Button(self.Pnl_MF_Temp_Button_Control, wx.ID_ANY, u"ON", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        gSizer17.Add(self.Cmd_MF_Temp_ON, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_MF_Temp_OFF = wx.Button(self.Pnl_MF_Temp_Button_Control, wx.ID_ANY, u"OFF", wx.DefaultPosition,
                                         wx.DefaultSize, 0)
        gSizer17.Add(self.Cmd_MF_Temp_OFF, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_MF_Temp_Standby = wx.Button(self.Pnl_MF_Temp_Button_Control, wx.ID_ANY, u"STANDBY", wx.DefaultPosition,
                                        wx.DefaultSize, 0)
        gSizer17.Add(self.Cmd_MF_Temp_Standby, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        #ADD BY REZA=
        self.Cmd_MF_SeeLogSuhu = wx.Button(self.Pnl_MF_Temp_Button_Control, wx.ID_ANY, u"Log Suhu", wx.DefaultPosition,
                                             wx.DefaultSize, 0)
        gSizer17.Add(self.Cmd_MF_SeeLogSuhu, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        #============


        self.Pnl_MF_Temp_Button_Control.SetSizer(gSizer17)
        self.Pnl_MF_Temp_Button_Control.Layout()
        gSizer17.Fit(self.Pnl_MF_Temp_Button_Control)
        fgSizer16.Add(self.Pnl_MF_Temp_Button_Control, 1, wx.EXPAND | wx.ALL, 0)

        self.Pnl_MF_Temperature.SetSizer(fgSizer16)
        self.Pnl_MF_Temperature.Layout()
        fgSizer16.Fit(self.Pnl_MF_Temperature)

    #def Warning Box

    def Events(self):
        #PANEL 1


        self.Cmd_MF_RunChkd.Bind( wx.EVT_BUTTON, lambda x:self.FrameAction(1, row = self.Dv_MF_MovementList.GetItemCount(),
                                                                    col = self.Dv_MF_MovementList.GetColumnCount()))
        self.Cmd_MF_Run.Bind( wx.EVT_BUTTON, lambda x:self.FrameAction(101, row = self.Dv_MF_MovementList.GetItemCount(),
                                                                    col = self.Dv_MF_MovementList.GetColumnCount()))
        self.Cmd_MF_All.Bind( wx.EVT_BUTTON, lambda x:self.FrameData(2, ))
        self.Cmd_MF_Clear.Bind( wx.EVT_BUTTON, lambda x:self.FrameAction(2, ))
        self.Cmd_SET_Temp.Bind( wx.EVT_BUTTON, lambda x:self.FrameAction(8, ))
        self.Cmd_MF_SeeLogSuhu.Bind(wx.EVT_BUTTON, lambda x:self.MFOpenLog())

        self.Bind(wx.EVT_MENU, lambda x: self.FrameLoad(1), id=self.SubMenu2.GetId())
        self.Bind(wx.EVT_MENU, lambda x: self.FrameLoad(5), id=self.SubMenu_Stream.GetId())
        self.Bind(wx.EVT_MENU, lambda x: self.FrameLoad(2), id=self.SubMenu3_1.GetId())

        self.Cmd_MF_Temp_Standby.Bind( wx.EVT_BUTTON , lambda x:self.ActionPasser("Frame","Temperature StandBy",))
        self.Bind(wx.dataview.EVT_DATAVIEW_ITEM_VALUE_CHANGED,
                  lambda x:self.FrameAction(3, selected = self.Dv_MF_MovementList.GetSelectedRow()), id = wx.ID_ANY )

        #ComboBoX Proses
        self.Cmb_MF_Prc.Bind(wx.EVT_COMBOBOX, lambda x:self.FrameData(3, name = self.Cmb_MF_Prc.GetValue()))

        self.Cmd_MF_Temp_ON.Bind(wx.EVT_BUTTON, lambda x: self.ActionPasser("Frame","Temperature ON",))
        self.Cmd_MF_Temp_OFF.Bind(wx.EVT_BUTTON, lambda x: self.ActionPasser("Frame","Temperature OFF",))
        self.Cmd_MF_Prc_Refresh.Bind(wx.EVT_BUTTON, lambda x: self.FrameData(1,))

        #PANEL 2
        self.CmdConn1.Bind(wx.EVT_BUTTON,
                           lambda x: self.SerialConn(1, self.CmbPort1.GetValue(), self.CmbBRate1.GetValue(), 0))
        self.CmdConn2.Bind(wx.EVT_BUTTON,
                           lambda x: self.SerialConn(2, self.CmbPort2.GetValue(), self.CmbBRate2.GetValue(), 0))
        self.CmdConn3.Bind(wx.EVT_BUTTON,
                           lambda x: self.SerialConn(3, self.CmbPort3.GetValue(), self.CmbBRate3.GetValue(), 0))

        self.CmdDisConn1.Bind(wx.EVT_BUTTON, lambda x: self.SerialDisconn(1))
        self.CmdDisConn2.Bind(wx.EVT_BUTTON, lambda x: self.SerialDisconn(2))
        self.CmdDisConn3.Bind(wx.EVT_BUTTON, lambda x: self.SerialDisconn(3))

        #PANEL 3
        self.Cmd_LB_Clear.Bind(wx.EVT_BUTTON, lambda x:self.FrameAction(4,))
        self.CmdSave.Bind(wx.EVT_BUTTON, lambda x:self.FrameAction(9,))

        #ADD RezaFR V2.3.6 MFCheckUnCheck(self, mode)
        self.Cmd_MF_ChkAll.Bind(wx.EVT_BUTTON,lambda x: self.MFCheckUnCheck(1))
        self.Cmd_MF_UnChkAll.Bind(wx.EVT_BUTTON, lambda x: self.MFCheckUnCheck(2))

    def ActionPasser(self, type, mode, **kwargs):
            if self.Event_Status == "ON":
                #func to call massage warning box
                #if Answer == "CONTINUE":
                #   print("Proces Overwrited")
                #  pass
                #elif Answer == "CANCEL":
                #  print("Proces Canceled")
                #  return
                pass

            if type == "Proces":
                if mode == "Proces Running":
                    # == Wait Running Proces Warning
                    if self.Proces_Step == "Running":
                        self.MessagesBox("Ordinary", "Warning : Proces Conflict!", "Ada Proces Yang Masih Berjalan\n" +
                                         "Mohon Tunggu Agar Proses Selesai\n")
                    else:
                    #if True:
                        self.Proces_Data = kwargs["Data"]
                        self.Event_Types = "Proces"
                        self.Event_Status = "ON"

            elif type == "Frame":
                if mode == "Temperature ON":
                    self.Event_Types = "Action"
                    self.Event_Name = "Temperature"
                    self.Event_Temperature = "ON"
                    self.Event_Status = "ON"

                elif mode == "Temperature OFF":
                    self.Event_Types = "Action"
                    self.Event_Name = "Temperature"
                    self.Event_Temperature = "OFF"
                    self.Event_Status = "ON"

                elif mode == "Temperature StandBy":
                    self.Event_Types = "Action"
                    self.Event_Name = "Temperature"
                    if self.Cmd_MF_Temp_Standby.GetLabel() == "STANDBY":
                        self.RoboHEAT(0)
                        self.suhus = "off"
                        self.Event_Temperature = "StandBy"
                    if self.Cmd_MF_Temp_Standby.GetLabel() == "STOP":
                        self.Event_Temperature = "Stop"
                    self.Event_Status = "ON"

                elif mode == "Temperature StandBy Off":
                    self.Event_Types = "Action"
                    self.Event_Name = "Temperature"
                    self.Event_Temperature = "Stop"
                    self.Event_Status = "ON"


    def FrameAction(self, mode, **kwargs):

        #-- Recording Data TO Array
        if mode == 1:
            self.MFDisable()
            self.Is_All = False
            hasil = []
            for row in range(kwargs["row"]):
                allitem = []
                for col in range(kwargs["col"]):
                    if col == 0:
                        data = self.Dv_MF_MovementList.GetToggleValue(row, col)
                    else:
                        data = self.Dv_MF_MovementList.GetValue(row, col)
                        data = data.encode()
                    allitem.append(data)

                hasil.append(allitem)



            Empty = True
            print "========================================================"
            for value in hasil:
                if (True in value) == True or ("True" in value) == True:
                    print value
                    Empty = False
            print "========================================================"
            print Empty
            if Empty == True:
                self.MessagesBox("Ordinary", "Warning : None Has Selected!", "Belum Ada Gerakan Yang Dipilih")
                self.MFEnable()
            elif Empty == False:
                self.ActionPasser("Proces", "Proces Running", Data=hasil)

        # -- Recording Data TO Array
        if mode == 101:
            self.MFDisable()
            self.Is_All = True
            hasil = []
            for row in range(kwargs["row"]):
                allitem = []
                for col in range(kwargs["col"]):
                    if col == 0:
                        data = self.Dv_MF_MovementList.GetToggleValue(row, col)
                    else:
                        data = self.Dv_MF_MovementList.GetValue(row, col)
                        data = data.encode()
                    allitem.append(data)

                hasil.append(allitem)

            Empty = True
            print "========================================================"
            for value in hasil:
                if (True in value) == True or ("True" in value) == True:
                    print value
                    Empty = False
            print "========================================================"
            print Empty
            if Empty == True:
                self.MessagesBox("Ordinary", "Warning : None Has Selected!", "Belum Ada Gerakan Yang Dipilih")
                self.MFEnable()
            elif Empty == False:
                self.ActionPasser("Proces", "Proces Running", Data=hasil)

        #Not Used ... Looping Config
        elif mode == 11:
            hasil = []

            for i in range(300):
                for row in range(kwargs["row"]):
                    allitem = []
                    for col in range(kwargs["col"]):
                        if col == 0:
                            data = self.Dv_MF_MovementList.GetToggleValue(row, col)
                        else:
                            data = self.Dv_MF_MovementList.GetValue(row, col)
                            data = data.encode()
                        allitem.append(data)

                    hasil.append(allitem)

                self.LbLog.AppendItems(str(i))

            while i != 299:
                pass

            Empty = True
            print "========================================================"
            for value in hasil:
                if (True in value) == True or ("True" in value) == True:
                    print value
                    Empty = False
            print "========================================================"
            print Empty
            if Empty == True:
                self.MessagesBox("Ordinary", "Warning : None Has Selected!", "Belum Ada Gerakan Yang Dipilih")
                self.MFEnable()
            elif Empty == False:
                self.ActionPasser("Proces", "Proces Running", Data=hasil)

        #-- Clear All Items ON DataView
        elif mode == 2:
            self.Dv_MF_MovementList.DeleteAllItems()

        #-- If Enter Clicked Change Value To True And Selected
        elif mode == 3:
            if self.Vals == False:
                self.Vals = True
                return

            value = self.Dv_MF_MovementList.GetToggleValue(kwargs["selected"], 0)
            print value

            if value == True:
                hasil = "SELECTED"
            elif value == False:
                hasil = "PENDING"

            self.Vals = False
            self.Dv_MF_MovementList.SetValue(hasil, kwargs["selected"], 2)
            #anti infinity loop

        #-- Delete All Items ON ListBox
        elif mode == 4:
            self.Cmb_MF_Prc.SetValue('')
            self.LbLog.Clear()
            self.GUID_Proces = self.MDiagnostikNexus(2)
            self.ID_Proces = ''
            self.Cmb_MF_Prc.SetValue('')

        #-- Refresh Items On Combo Box Proces
        elif mode == 5:
            self.Cmb_MF_Prc.Clear()
            self.FrameData(1)

        elif mode == 6:
            if kwargs['portser'] == 1:
                a = self.CmbPort1.GetValue()
                self.CmbPort1.Clear()
                self.CmbPort1.SetValue(a)

            elif kwargs['portser'] == 2:
                a = self.CmbPort2.GetValue()
                self.CmbPort2.Clear()
                self.CmbPort2.SetValue(a)

            elif kwargs['portser'] == 3:
                a = self.CmbPort3.GetValue()
                self.CmbPort3.Clear()
                self.CmbPort3.SetValue(a)

            for i in kwargs['serial']:
                if kwargs['portser'] == 1:
                    self.CmbPort1.Append(i)
                elif kwargs['portser'] == 2:
                    self.CmbPort2.Append(i)
                elif kwargs['portser'] == 3:
                    self.CmbPort3.Append(i)

        elif mode == 7:
            self.FrameLoad(1)

        elif mode == 8:
            self.MaxLimitTemp = float(self.Txt_Max_Temp.GetValue())
            print self.MaxLimitTemp
            self.MinLimitTemp = float(self.Txt_Min_Temp.GetValue())
            print self.MinLimitTemp

        elif mode == 9:
            Frame_SaveToText.Nexus_SaveToText(None,self.LbLog.GetItems())



    def FrameData(self, mode, **kwargs):
        if mode == 1: #Proces Listing
            self.Cmb_MF_Prc.Clear()
            sSQL = (" EXEC SP_Nxs_GetProses 1, ?")
            Values = ["NONE"]
            data = self.GETData(2, SQL=sSQL, value=Values)
            data = [x[0] for x in data]
            for i in data:
                self.Cmb_MF_Prc.AppendItems(i)

        elif mode == 2: #All Listing
            self.Dv_MF_MovementList.DeleteAllItems()
            sSQL = (" EXEC SP_Nxs_GetConfiguration 3, ?")
            Values = ["NONE"]
            data = self.GETData(2, SQL=sSQL, value=Values)
            data = [x[0] for x in data]
            for i in data:
                hasil = []
                hasil.extend([False,i,"PENDING"])
                self.Dv_MF_MovementList.AppendItem(hasil)

            #Reset Cmb Process
            self.ID_Proces = ''
            self.GUID_Proces = self.MDiagnostikNexus(2)
            self.Cmb_MF_Prc.SetValue('')

        elif mode == 3: #Selected Listing
            if kwargs['name'] == '' or len(kwargs['name']) == 0:
                return

            sSQL = (" EXEC SP_Nxs_ControlFrame_Data 1, ?")
            Values = [kwargs["name"]]
            data = self.GETData(2, SQL=sSQL, value = Values)
            data = [x[0] for x in data]
            self.Dv_MF_MovementList.DeleteAllItems()
            for i in data:
                hasil = []
                hasil.extend([True,i,"SELECTED"])
                self.Dv_MF_MovementList.AppendItem(hasil)

            #SET THE CURRENT SELECTED PROCESS
            sSQL = (" EXEC SP_Nxs_ControlFrame_Data 2, ?")
            Values = [kwargs["name"]]
            data = self.GETData(2, SQL=sSQL, value=Values)
            data = [x[0] for x in data]
            if type(data) == list:
                data = data[0]
            if data not in (None,''):
                self.GUID_Proces = self.MDiagnostikNexus(2)
                self.ID_Proces = data
            else:
                self.GUID_Proces = self.MDiagnostikNexus(2)
                self.ID_Proces = ''

    def MFCheckUnCheck(self, mode):

        hasil = []
        for row in range(self.Dv_MF_MovementList.GetItemCount()):
            allitem = []
            for col in range(self.Dv_MF_MovementList.GetColumnCount()):
                if col == 0:
                    data = self.Dv_MF_MovementList.GetToggleValue(row, col)
                else:
                    data = self.Dv_MF_MovementList.GetValue(row, col)
                    data = data.encode()
                allitem.append(data)

            hasil.append(allitem)

        #Check
        if mode == 1:
            self.Dv_MF_MovementList.DeleteAllItems()
            for itemrow in hasil:
                itemrow[0] = True
                self.Dv_MF_MovementList.AppendItem(itemrow)

        #Uncheck
        elif mode == 2:
            self.Dv_MF_MovementList.DeleteAllItems()
            for itemrow in hasil:
                itemrow[0] = False
                self.Dv_MF_MovementList.AppendItem(itemrow)



    def MFDisable(self):
        self.Cmd_MF_All.Disable()
        self.Cmd_MF_Run.Disable()
        self.Cmd_MF_RunChkd.Disable()

    def MFEnable(self):
        self.Cmd_MF_All.Enable()
        self.Cmd_MF_Run.Enable()
        self.Cmd_MF_RunChkd.Enable()

    def MFCreateFile(self,filename):
        name = str(r'.\LogSuhu\%s' %(str(filename)+'.txt'))
        name = name.replace(':','+')
        newfiles = open(name, 'a+')
        return(name)

    def MFAppendConfig(self, pathfileused, data):
        #DATA MUST FORMAT {TITLE:{ATTR1:contain,ATTR2:contain}}

        try:
            complete_path = str(pathfileused)
            fileconfig = ConfigParser.ConfigParser()
            fileconfig.readfp(open(complete_path, 'r'))
            data.keys()
        except Exception as e:
            print (e)
            return (None)

        for keys in data.keys():
            title = keys
            isi = data[str(title)]
            #Add to Config
            fileconfig.add_section(title)

            try:
                data.keys()
            except Exception as e:
                print (e)
                pass
            else:
                for items in isi.keys():
                    isititle = str(items)
                    isicontain = str(isi[items])

                    #Add Config Contain
                    fileconfig.set(title, isititle, isicontain)

        #Save To Confile txt [This is Temporary]
        with open(complete_path, 'a+') as filetoappend:
            fileconfig.write(filetoappend)


    def MFSaveToExcel(self, pathfilesource, pathfiledestination):
        try:
            complete_path = str(pathfilesource)
            fileconfig = ConfigParser.ConfigParser()
            fileconfig.readfp(open(complete_path))
        except Exception as e:
            print (e)
            return (None)

        #Create File
        workbook = xlsxwriter.Workbook(pathfiledestination)
        worksheet = workbook.add_worksheet()


        #Write Header
        #-- time
        worksheet.write(0, 0, str(self.CurTime()))
        # -- header
        worksheet.write(1, 0, 'Suhu')
        worksheet.write(1, 1, 'Waktu')
        worksheet.write(1, 2, 'Status Heater')

        #start from 2:0
        row = 2

        plused = False
        for sectionslis in fileconfig.sections():
            suhu =  fileconfig.get(str(sectionslis), 'Suhu')
            waktu = fileconfig.get(str(sectionslis), 'Waktu')
            status = fileconfig.get(str(sectionslis), 'StatusHeater')

            worksheet.write(row, 0, str(suhu))
            worksheet.write(row, 1, str(waktu))
            worksheet.write(row, 2, str(status))

            row += 1
            plused = True

        #close
        workbook.close()

    def MFOpenLog(self):
        self.FrameLoad(6)

    

        
