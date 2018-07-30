

import wx
import wx.dataview as DV
import Model as M

class FrameTrans( wx.Frame ):

    def __init__(self,parent):
        self.Frames(parent,"DATA Transaksi")

    def Frames(self,parent,title):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = title,
                          pos = wx.DefaultPosition, size = wx.Size( 750,440 ) )

        Grids = wx.FlexGridSizer( 0, 2, 0, 0 )
        Grids.SetFlexibleDirection( wx.BOTH )
        Grids.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.Panels1(self)
        Grids.Add( self.Panel1, 1, wx.EXPAND |wx.ALL, 0 )	

        self.SetSizer( Grids )
        self.Layout()

        self.DataLoad()
        self.Show()

    def Panels1(self,parent):
        self.Panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        Grids = wx.FlexGridSizer( 3, 1, 0, 0 )
        Grids.SetFlexibleDirection( wx.BOTH )
        Grids.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
        self.LblJudul = wx.StaticText( self.Panel1, wx.ID_ANY, u"TABLE TRANSAKSI", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.LblJudul.Wrap( -1 )
        self.LblJudul.SetFont( wx.Font( 22, 74, 90, 92, False, "Calibri" ) )
		
        Grids.Add( self.LblJudul, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
        self.TblKoor = DV.DataViewListCtrl( self.Panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size(740,300), 0 )
        Grids.Add( self.TblKoor, 1, wx.ALL|wx.EXPAND, 10 )
		
        SubGrids = wx.FlexGridSizer( 1, 3, 0, 0 )
        SubGrids.SetFlexibleDirection( wx.BOTH )
        SubGrids.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
        self.CmdADD = wx.Button( self.Panel1, wx.ID_ANY, u"ADD", wx.DefaultPosition, wx.DefaultSize, 0 )
        SubGrids.Add( self.CmdADD, 0, wx.ALL, 5 )
		
        self.CmdEDIT = wx.Button( self.Panel1, wx.ID_ANY, u"EDIT", wx.DefaultPosition, wx.DefaultSize, 0 )
        SubGrids.Add( self.CmdEDIT, 0, wx.ALL, 5 )
		
        self.CmdDEL = wx.Button( self.Panel1, wx.ID_ANY, u"DELETE", wx.DefaultPosition, wx.DefaultSize, 0 )
        SubGrids.Add( self.CmdDEL, 0, wx.ALL, 5 )
			
        Grids.Add( SubGrids, 1, wx.EXPAND, 5 )
		
		
        self.Panel1.SetSizer( Grids )
        self.Panel1.Layout()
        Grids.Fit( self.Panel1 )

    def DataLoad(self):
        data = M.Model()
        data = data.TableGet(1,)
        datas = data
        self.TblKoor.AppendTextColumn("ID")
        self.TblKoor.AppendTextColumn("List Motor")
        self.TblKoor.AppendTextColumn("Name")
        self.TblKoor.AppendTextColumn("Start")
        self.TblKoor.AppendTextColumn("End")
        self.TblKoor.AppendTextColumn("Orientasi")
        
        for i in range(len(datas[0])):
            self.TblKoor.AppendItem([str(datas[0][i]),
                                     str(datas[1][i]),
                                     str(datas[2][i]),
                                     str(datas[3][i]),
                                     str(datas[4][i]),
                                     str(datas[5][i])])
