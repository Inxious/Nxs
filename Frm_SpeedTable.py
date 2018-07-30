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


###########################################################################
## Class Frm_SpeedTable
###########################################################################

class Frm_SpeedTable(wx.Frame):
    def __init__(self, parent):
        #if self.XNow
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(354, 368), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        gSizer1 = wx.GridSizer(0, 1, 0, 0)

        self.Pnl_ST = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.Pnl_ST.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

        fgSizer1 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.Jdl_ST = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"Speed Table", wx.DefaultPosition, wx.DefaultSize, 0)
        self.Jdl_ST.Wrap(-1)
        self.Jdl_ST.SetFont(wx.Font(16, 70, 90, 92, False, "Arial"))

        fgSizer1.Add(self.Jdl_ST, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.m_staticText1 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"X", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        gbSizer1.Add(self.m_staticText1, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Txt_ST_SpX = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_SpX, wx.GBPosition(1, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_ST_AccX = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_AccX, wx.GBPosition(1, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText11 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"Speed", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        gbSizer1.Add(self.m_staticText11, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText12 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"Acceleration", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText12.Wrap(-1)
        gbSizer1.Add(self.m_staticText12, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText111 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"Motor", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText111.Wrap(-1)
        gbSizer1.Add(self.m_staticText111, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText2 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"Y", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        gbSizer1.Add(self.m_staticText2, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Txt_ST_SpY = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_SpY, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_ST_AccY = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_AccY, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText3 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"Z", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        gbSizer1.Add(self.m_staticText3, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Txt_ST_SpZ = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_SpZ, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_ST_AccZ = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_AccZ, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText4 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"A", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gbSizer1.Add(self.m_staticText4, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Txt_ST_SpA = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_SpA, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_ST_AccA = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_AccA, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText5 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"B", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        gbSizer1.Add(self.m_staticText5, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Txt_ST_SpB = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_SpB, wx.GBPosition(5, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_ST_AccB = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_AccB, wx.GBPosition(5, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText6 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"C", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText6.Wrap(-1)
        gbSizer1.Add(self.m_staticText6, wx.GBPosition(6, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Txt_ST_SpC = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_SpC, wx.GBPosition(6, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_ST_AccC = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_AccC, wx.GBPosition(6, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.m_staticText7 = wx.StaticText(self.Pnl_ST, wx.ID_ANY, u"R", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText7.Wrap(-1)
        gbSizer1.Add(self.m_staticText7, wx.GBPosition(7, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Txt_ST_SpR = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_SpR, wx.GBPosition(7, 1), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Txt_ST_AccR = wx.TextCtrl(self.Pnl_ST, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Txt_ST_AccR, wx.GBPosition(7, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Cmd_ST_Set = wx.Button(self.Pnl_ST, wx.ID_ANY, u"SET", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Cmd_ST_Set, wx.GBPosition(8, 1), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.Cmd_ST_Defaukt = wx.Button(self.Pnl_ST, wx.ID_ANY, u"DEFAULT", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Cmd_ST_Defaukt, wx.GBPosition(8, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.Cmd_ST_Exit = wx.Button(self.Pnl_ST, wx.ID_ANY, u"EXIT", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.Cmd_ST_Exit, wx.GBPosition(8, 2), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        fgSizer1.Add(gbSizer1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 10)

        self.Pnl_ST.SetSizer(fgSizer1)
        self.Pnl_ST.Layout()
        fgSizer1.Fit(self.Pnl_ST)
        gSizer1.Add(self.Pnl_ST, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        idlist = {'X': 6, 'Y': 4, 'Z': 1, 'A': 3, 'B': 2, 'C': 5, 'R': 17}
        for id in idlist:
            spd = self.GETNows(4, idlist[id])
            if (spd not in(0,'',None)) == True:
                if id == 'X':
                    self.Txt_ST_SpX.SetValue(spd)
                elif id == 'Y':
                    self.Txt_ST_SpY.SetValue(spd)
                elif id == 'Z':
                    self.Txt_ST_SpZ.SetValue(spd)
                elif id == 'A':
                    self.Txt_ST_SpA.SetValue(spd)
                elif id == 'B':
                    self.Txt_ST_SpB.SetValue(spd)
                elif id == 'C':
                    self.Txt_ST_SpC.SetValue(spd)
                elif id == 'R':
                    self.Txt_ST_SpR.SetValue(spd)

            acc = self.GETNows(5, idlist[id])
            if (acc not in(0,'',None)) == True:
                if id == 'X':
                    self.Txt_ST_AccX.SetValue(acc)
                elif id == 'Y':
                    self.Txt_ST_AccY.SetValue(acc)
                elif id == 'Z':
                    self.Txt_ST_AccZ.SetValue(acc)
                elif id == 'A':
                    self.Txt_ST_AccA.SetValue(acc)
                elif id == 'B':
                    self.Txt_ST_AccB.SetValue(acc)
                elif id == 'C':
                    self.Txt_ST_AccC.SetValue(acc)
                elif id == 'R':
                    self.Txt_ST_AccR.SetValue(acc)

        self.Show()

        # Connect Events
        self.Cmd_ST_Set.Bind(wx.EVT_BUTTON, lambda x:self.ST_FrameAct(1))
        self.Cmd_ST_Defaukt.Bind(wx.EVT_BUTTON, lambda x:self.ST_FrameAct(2))
        self.Cmd_ST_Exit.Bind(wx.EVT_BUTTON, lambda x:self.ST_FrameAct(3))

    def ST_FrameAct(self,mode):
        if mode == 1:

            accs1 = {}
            accs1.update({'X':self.Txt_ST_SpX.GetValue()})
            accs1.update({'Y':self.Txt_ST_SpY.GetValue()})
            accs1.update({'Z':self.Txt_ST_SpZ.GetValue()})
            accs1.update({'A':self.Txt_ST_SpA.GetValue()})
            accs1.update({'B':self.Txt_ST_SpB.GetValue()})
            accs1.update({'C':self.Txt_ST_SpC.GetValue()})
            accs1.update({'R':self.Txt_ST_SpR.GetValue()})

            accs = {}
            accs.update({'X':self.Txt_ST_AccX.GetValue()})
            accs.update({'Y':self.Txt_ST_AccY.GetValue()})
            accs.update({'Z':self.Txt_ST_AccZ.GetValue()})
            accs.update({'A':self.Txt_ST_AccA.GetValue()})
            accs.update({'B':self.Txt_ST_AccB.GetValue()})
            accs.update({'C':self.Txt_ST_AccC.GetValue()})
            accs.update({'R':self.Txt_ST_AccR.GetValue()})

            acc = {'X':6,'Y':4,'Z':1,'A':3,'B':2,'C':5,'R':17}
            for i in acc:
                if accs1[i] == "":
                    pass
                else:
                    data = self.ser1.write('NEXUS=' + i + '_MAX_SPEED#~' + i + '=' + str(accs1[i]) + '~$' + '\r\n')
                    self.LbLog.AppendItems("COMMAND >> " + str(data))
                    self.Nows(2, acc[i], values=accs1[i])
                    self.Nows(4, acc[i], values=accs1[i])

                if accs[i] == "":
                    pass
                else:
                    data1 =self.ser1.write('NEXUS=' + i + '_ACCELERATION#~' + i + '=' + str(accs[i]) + '~$' + '\r\n')
                    self.LbLog.AppendItems("COMMAND >> " + str(data1))
                    self.Nows(3, acc[i], values=accs[i])
                    self.Nows(5, acc[i], values=accs[i])

                if accs1[i] != "" and accs[i] != "":
                    self.SpeedToConfig(i, accs1[i], accs[i])

                #FLUSH OUTPUT
                self.ser1.flushOutput()

        elif mode == 2:
            acc = ['X', 'Y', 'Z', 'A', 'C', 'R']
            scc = [20 , 15, 13, 13, 10, 1]
            for i in acc:
                data = 'NEXUS=' + i + '_MAX_SPEED#~' + i + '=' + str(scc[i]) + '~$'
                self.ser1.write(data + '\r\n')
                data1 = 'NEXUS=' + i + '_ACCELERATION#~' + i + '=' + str(scc[i] - 1) + '~$'
                self.ser1.write( data1 + '\r\n')

                self.LbLog.AppendItems("COMMAND >> " + str(data))
                self.LbLog.AppendItems("COMMAND >> " + str(data1))
        elif mode == 3:
            self.Hide()

    def SpeedToConfig(self, motor, speed, accel):



        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.txt'))

        if motor == 'X':
            with open('config.txt', 'w') as configfile:
                config.set('Motor Configuration', 'X_Speed', str(speed))
                config.write(configfile)
                config.set('Motor Configuration', 'X_Accel', str(accel))
                config.write(configfile)

        if motor == 'Y':
            with open('config.txt', 'w') as configfile:
                config.set('Motor Configuration', 'Y_Speed', str(speed))
                config.write(configfile)
                config.set('Motor Configuration', 'Y_Accel', str(accel))
                config.write(configfile)

        if motor == 'Z':
            with open('config.txt', 'w') as configfile:
                config.set('Motor Configuration', 'Z_Speed', str(speed))
                config.write(configfile)
                config.set('Motor Configuration', 'Z_Accel', str(accel))
                config.write(configfile)

        if motor == 'A':
            with open('config.txt', 'w') as configfile:
                config.set('Motor Configuration', 'A_Speed', str(speed))
                config.write(configfile)
                config.set('Motor Configuration', 'A_Accel', str(accel))
                config.write(configfile)

        if motor == 'B':
            with open('config.txt', 'w') as configfile:
                config.set('Motor Configuration', 'B_Speed', str(speed))
                config.write(configfile)
                config.set('Motor Configuration', 'B_Accel', str(accel))
                config.write(configfile)

        if motor == 'C':
            with open('config.txt', 'w') as configfile:
                config.set('Motor Configuration', 'C_Speed', str(speed))
                config.write(configfile)
                config.set('Motor Configuration', 'C_Accel', str(accel))
                config.write(configfile)

        if motor == 'R':
            with open('config.txt', 'w') as configfile:
                config.set('Motor Configuration', 'R_Speed', str(speed))
                config.write(configfile)
                config.set('Motor Configuration', 'R_Accel', str(accel))
                config.write(configfile)


