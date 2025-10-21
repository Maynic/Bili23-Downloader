import wx
import sys
import wx.adv

from utils.common.style.icon_v4 import Icon, IconID
from utils.config import Config

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self):
        wx.adv.TaskBarIcon.__init__(self)

        self.SetIcon(wx.BitmapBundle.FromBitmap(Icon.get_icon_bitmap(IconID.App_Default)), Config.APP.name)

        self.init_id()

        self.Bind_EVT()

    def CreatePopupMenu(self):
        menu = wx.Menu()

        main_menuitem = wx.MenuItem(menu, self.ID_MAIN_MENU, "主界面(&M)")
        download_menuitem = wx.MenuItem(menu, self.ID_DOWNLOAD_MENU, "下载管理(&D)")
        exit_menuitem = wx.MenuItem(menu, self.ID_EXIT_MENU, "退出(&X)")

        menu.Append(main_menuitem)
        menu.Append(download_menuitem)
        menu.AppendSeparator()
        menu.Append(exit_menuitem)

        return menu
    
    def init_id(self):
        self.ID_MAIN_MENU = wx.NewIdRef()
        self.ID_DOWNLOAD_MENU = wx.NewIdRef()
        self.ID_EXIT_MENU = wx.NewIdRef()

    def Bind_EVT(self):
        self.Bind(wx.EVT_MENU, self.onMenuEVT)

    def onMenuEVT(self, event: wx.MenuEvent):
        main_window = wx.FindWindowByName("main")

        match event.GetId():
            case self.ID_MAIN_MENU:
                self.switch_window(main_window)

            case self.ID_DOWNLOAD_MENU:
                self.switch_window(main_window.download_window)

            case self.ID_EXIT_MENU:
                sys.exit()
    
    def switch_window(self, frame: wx.Frame):
        if frame.IsIconized():
            frame.Iconize(False)
        
        elif not frame.IsShown():
            frame.Show()
            frame.CenterOnParent()

        frame.Raise()
