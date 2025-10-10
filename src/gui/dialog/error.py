import wx
import gettext

from utils.config import Config
from utils.common.exception import GlobalExceptionInfo
from utils.common.datetime_util import DateTime

from gui.component.window.dialog import Dialog
from gui.component.staticbitmap.staticbitmap import StaticBitmap

_ = gettext.gettext

class ErrorInfoDialog(Dialog):
    def __init__(self, parent, exception_info = GlobalExceptionInfo.info):
        self.exception_info: dict = exception_info

        Dialog.__init__(self, parent, _("错误日志"))

        self.init_UI()

        self.CenterOnParent()

        wx.Bell()

    def init_UI(self):
        err_icon = StaticBitmap(self, bmp = wx.ArtProvider().GetBitmap(wx.ART_ERROR, size = self.FromDIP((28, 28))), size = self.FromDIP((28, 28)))

        time_lab = wx.StaticText(self, -1, _("记录时间：%s") % DateTime.time_str_from_timestamp(self.exception_info.get("timestamp")))
        error_type = wx.StaticText(self, -1, _("异常类型：%s") % self.exception_info.get("exception_name"))
        error_id_lab = wx.StaticText(self, -1, _("错误码：%s") % self.exception_info.get("code"))
        message_lab = wx.StaticText(self, -1, _("描述：%s") % self.exception_info.get("message"), size = self.FromDIP((300, 16)), style = wx.ST_ELLIPSIZE_END)

        box_sizer = wx.FlexGridSizer(2, 2, 0, 75)
        box_sizer.Add(time_lab, 0, wx.ALL, self.FromDIP(6))
        box_sizer.Add(error_type, 0, wx.ALL, self.FromDIP(6))
        box_sizer.Add(error_id_lab, 0, wx.ALL & (~wx.TOP), self.FromDIP(6))
        box_sizer.Add(message_lab, 0, wx.ALL & (~wx.TOP), self.FromDIP(6))

        top_hbox = wx.BoxSizer(wx.HORIZONTAL)
        top_hbox.Add(err_icon, 0, wx.ALL | wx.ALIGN_CENTER, self.FromDIP(6))
        top_hbox.Add(box_sizer, 0, wx.ALL | wx.EXPAND, self.FromDIP(6))

        top_border = wx.StaticLine(self, -1, style = wx.HORIZONTAL)

        font: wx.Font = self.GetFont()
        font.SetFractionalPointSize(int(font.GetFractionalPointSize() + 1))

        self.log_box = wx.TextCtrl(self, -1, str(self.exception_info.get("stack_trace")), size = self.FromDIP((620, 250)), style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.log_box.SetFont(font)

        self.close_btn = wx.Button(self, wx.ID_CANCEL, _("关闭"), size = self.get_scaled_size((80, 28)))

        bottom_border = wx.StaticLine(self, -1, style = wx.HORIZONTAL)

        bottom_hbox = wx.BoxSizer(wx.HORIZONTAL)
        bottom_hbox.AddStretchSpacer()
        bottom_hbox.Add(self.close_btn, 0, wx.ALL & (~wx.LEFT), self.FromDIP(6))

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(top_hbox, 0, wx.EXPAND)
        vbox.Add(top_border, 0, wx.EXPAND)
        vbox.Add(self.log_box, 0, wx.EXPAND)
        vbox.Add(bottom_border, 0, wx.EXPAND)
        vbox.Add(bottom_hbox, 0, wx.EXPAND)

        self.SetSizerAndFit(vbox)

        self.set_dark_mode()

    def set_dark_mode(self):
        if not Config.Sys.dark_mode:
            self.SetBackgroundColour("white")
            self.log_box.SetBackgroundColour("white")