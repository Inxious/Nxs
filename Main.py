import Controller as C
import sys,os
import wx
from wx.lib.pubsub import  pub


class Main:

    def __init__(self,parent):
        C.Controller()

if __name__ == '__main__':
    Nexus = wx.App(False)

    Program = Main(None)

    Nexus.MainLoop()
