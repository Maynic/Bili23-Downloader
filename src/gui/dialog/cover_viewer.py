import wx
import os
import gettext

from utils.module.pic.cover import Cover

from utils.common.style.color import Color

from gui.component.window.frame import Frame

_ = gettext.gettext

class CoverViewerDialog(Frame):
    def __init__(self, parent, cover_raw_contents: bytes, cover_url: str):
        self.cover_raw_contents = cover_raw_contents
        self.cover_url = cover_url

        Frame.__init__(self, parent, _("视频封面"))

        self.init_utils()

        self.init_UI()

        self.Bind_EVT()

        self.CenterOnParent()

    def init_UI(self):
        self.SetBackgroundColour(Color.get_panel_background_color())

        self.cover_bmp = wx.StaticBitmap(self, -1, bitmap = self.show_cover(self.FromDIP((800, 480))))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.AddStretchSpacer()
        hbox.Add(self.cover_bmp, 0, wx.EXPAND)
        hbox.AddStretchSpacer()

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.AddStretchSpacer()
        vbox.Add(hbox, 0, wx.EXPAND)
        vbox.AddStretchSpacer()

        self.SetSizerAndFit(vbox)

        self.init_menubar()
        self.init_statusbar()

    def init_menubar(self):
        menu_bar = wx.MenuBar()

        self.file_menu = wx.Menu()
        self.options_menu = wx.Menu()

        menu_bar.Append(self.file_menu, _("文件(&F)"))
        menu_bar.Append(self.options_menu, _("选项(&O)"))

        self.file_menu.Append(self.ID_SAVE, _("保存原图(&S)\tCtrl+S"))
        self.file_menu.AppendSeparator()
        self.file_menu.Append(self.ID_CLOSE, _("关闭(&X)\tAlt+F4"))

        self.options_menu.Append(self.ID_ORIGINAL_SIZE, _("显示原图(&R)"))
        self.options_menu.AppendSeparator()
        self.options_menu.Append(self.ID_FIT_SIZE, _("窗口适应图片尺寸(&A)"))

        self.SetMenuBar(menu_bar)

    def init_statusbar(self):
        width, height = Cover.get_cover_size(self.cover_raw_contents)

        self.status_bar: wx.StatusBar = self.CreateStatusBar()

        self.status_bar.SetFieldsCount(2)
        self.status_bar.SetStatusWidths([self.FromDIP(250), self.FromDIP(250)])

        self.status_bar.SetStatusText("Ready", 0)
        self.status_bar.SetStatusText(_("原图尺寸：%sx%s") % (width, height), 1)

    def Bind_EVT(self):
        self.Bind(wx.EVT_MENU, self.onSaveEVT, id = self.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.onExitEVT, id = self.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.onFitSizeEVT, id = self.ID_FIT_SIZE)
        self.Bind(wx.EVT_MENU, self.onOriginalSizeEVT, id = self.ID_ORIGINAL_SIZE)

        self.Bind(wx.EVT_SIZE, self.onResizeEVT)

    def init_utils(self):
        self.ID_SAVE = wx.NewIdRef()
        self.ID_CLOSE = wx.NewIdRef()
        self.ID_ORIGINAL_SIZE = wx.NewIdRef()
        self.ID_FIT_SIZE = wx.NewIdRef()

    def onSaveEVT(self, event):
        dlg = wx.FileDialog(self, _("保存封面"), os.getcwd(), wildcard = _("JPG 文件(*.jpg)|*.jpg|PNG 文件|*.png|WEBP 文件|*.webp|AVIF 文件|*.avif"), style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            save_path = dlg.GetPath()

            cover_raw_contents = Cover.download_cover(self.cover_url, dlg.GetFilterIndex())

            with open(save_path, "wb") as f:
                f.write(cover_raw_contents)

    def onExitEVT(self, event):
        self.Destroy()

    def onResizeEVT(self, event: wx.SizeEvent):
        scaled_cover: wx.Bitmap = self.show_cover(self.GetClientSize())

        width, height = scaled_cover.GetSize()

        self.cover_bmp.SetBitmap(scaled_cover)

        self.status_bar.SetStatusText(_("缩放尺寸：%sx%s") % (width, height), 0)

        event.Skip()

    def onFitSizeEVT(self, event):
        cover_width, cover_height = self.cover_bmp.GetSize()

        self.SetSize(cover_width, cover_height + (self.GetSize()[1] - self.GetClientSize()[1]))

    def onOriginalSizeEVT(self, event):
        self.cover_bmp.SetBitmap(Cover.get_image_obj(self.cover_raw_contents))

        self.onFitSizeEVT(event)

        self.CenterOnScreen()

    def show_cover(self, new_size: wx.Size):
        cover_size = Cover.get_scaled_size(self.cover_raw_contents, new_size)

        return Cover.get_scaled_bitmap(self.cover_raw_contents, cover_size)
