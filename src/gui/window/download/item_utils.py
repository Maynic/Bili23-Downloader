import wx
import os

from utils.common.style.icon_v4 import Icon, IconID
from utils.common.model.data_type import DownloadTaskInfo
from utils.common.enums import ParseType, DownloadStatus
from utils.common.map import video_quality_map, video_codec_map, audio_quality_map, extra_map, get_mapping_key_by_value
from utils.common.formatter.formatter import FormatUtils
from utils.common.formatter.file_name_v2 import FileNameFormatter
from utils.common.thread import Thread
from utils.common.exception import GlobalExceptionInfo
from utils.common.model.callback import Callback, DownloaderCallback
from utils.common.io.directory import Directory

from utils.module.pic.cover import Cover
from utils.module.downloader_v3 import Downloader
from utils.module.ffmpeg_v2 import FFmpeg

from utils.parse.download import DownloadParser
from utils.parse.extra.extra_v3 import ExtraParser

from gui.window.download.item_panel_v4 import DownloadTaskItemPanel

class Utils:
    class UI:
        def __init__(self, parent: wx.Window):
            self.parent: DownloadTaskItemPanel = parent

        def show_cover(self, cover_url: str):
            def worker():
                self.parent.cover_bmp.SetBitmap(bitmap)
            
            size = self.parent.cover_bmp.GetSize()

            image = Cover.crop_cover(Cover.get_cover_raw_contents(cover_url))

            bitmap = Cover.get_scaled_bitmap_from_image(image, size)

            wx.CallAfter(worker)

        def set_title(self, title: str):
            self.parent.title_lab.SetLabel(title)
            self.parent.title_lab.SetToolTip(title)

        def set_progress(self, progress: int):
            self.parent.progress_bar.SetValue(progress)
            self.parent.progress_bar.SetToolTip(f"{progress}%")

        def set_quality_label(self, label: str):
            self.parent.video_quality_lab.SetLabel(label)

        def set_codec_label(self, label: str):
            self.parent.video_codec_lab.SetLabel(label)

        def set_size_label(self, label: str):
            self.parent.video_size_lab.SetLabel(label)

        def set_speed_label(self, label: str, error: bool = False):
            self.parent.speed_lab.SetLabel(label)
            self.parent.speed_lab.SetForegroundColour("red" if error else self.parent.speed_lab.get_default_color())
            self.parent.speed_lab.SetCursor(wx.Cursor(wx.CURSOR_HAND if error else wx.CURSOR_DEFAULT))

        def set_pause_btn(self, icon_id: IconID, tooltip: str, enable = True):
            self.parent.pause_btn.SetBitmap(Icon.get_icon_bitmap(icon_id))

            self.parent.pause_btn.SetToolTip(tooltip)
            self.parent.pause_btn.Enable(enable)

        def update(self):
            self.parent.Layout()

    class Info:
        def __init__(self, task_info: DownloadTaskInfo):
            self.task_info = task_info

        def get_quality_label(self):
            match ParseType(self.task_info.download_type):
                case ParseType.Video | ParseType.Bangumi | ParseType.Cheese:
                    if "video" in self.task_info.download_option:
                        return get_mapping_key_by_value(video_quality_map, self.task_info.video_quality_id, "--")
                    else:
                        return "音频"

                case ParseType.Extra:
                    return " ".join([value for key, value in extra_map.items() if self.task_info.extra_option.get(key)])
                
                case _:
                    return "未知"
                
        def get_codec_label(self):
            match ParseType(self.task_info.download_type):
                case ParseType.Video | ParseType.Bangumi | ParseType.Cheese:
                    if "video" in self.task_info.download_option:
                        return get_mapping_key_by_value(video_codec_map, self.task_info.video_codec_id, "--")
                    else:
                        return get_mapping_key_by_value(audio_quality_map, self.task_info.audio_quality_id, "--")
                
                case _:
                    return ""

        def get_size_label(self):
            if self.task_info.progress == 100:
                return FormatUtils.format_size(self.task_info.total_file_size)
            
            elif self.task_info.total_file_size:
                return f"{FormatUtils.format_size(self.task_info.total_downloaded_size)}/{FormatUtils.format_size(self.task_info.total_file_size)}"
            
            else:
                return "--"
        
        def get_merging_label(self):
            if "video" in self.task_info.download_option:
                return "正在合并视频..."
            else:
                return "正在转换音频..."
            
        def get_merge_error_label(self):
            reason = "合并视频" if "video" in self.task_info.download_option else "转换音频"

            return f"{reason}失败，点击查看详情"

    def __init__(self, parent: wx.Window, task_info: DownloadTaskInfo):
        self.parent: DownloadTaskItemPanel = parent
        self.task_info = task_info

        self.ui = self.UI(parent)
        self.info = self.Info(task_info)

    def show_task_info(self):
        self.ui.set_title(self.task_info.title)
        self.ui.set_progress(self.task_info.progress)

        self.ui.set_quality_label(self.info.get_quality_label())
        self.ui.set_codec_label(self.info.get_codec_label())
        self.ui.set_size_label(self.info.get_size_label())

        self.set_download_status(DownloadStatus(self.task_info.status))

        self.ui.update()

    def show_cover(self):
        self.ui.show_cover(f"{self.task_info.cover_url}@.jpeg")

    def destroy_panel(self, remove_file: bool = False, user_action: bool = False):
        if hasattr(self, "downloader"):
            self.downloader.stop_download(shutdown = remove_file)

        if remove_file:
            self.task_info.remove_file()

        self.clear_temp_files()

        self.parent.Destroy()

        self.parent.download_window.update_title(self.task_info.source, user_action)
        self.parent.download_window.remove_item(self.task_info.source)

        if user_action:
            self.parent.download_window.load_next_task(self.task_info.source)

    def move_panel(self):
        def worker():
            self.destroy_panel(remove_file = False)

            self.parent.download_window.right_panel.move_to_completed_page(self.task_info)

        wx.CallAfter(worker)

    def start_download(self):
        match ParseType(self.task_info.download_type):
            case ParseType.Video | ParseType.Bangumi | ParseType.Cheese:
                self.set_download_status(DownloadStatus.Downloading)

                Thread(target = self.start_video_download_thread).start()

            case ParseType.Extra:
                self.set_download_status(DownloadStatus.Generating)

                Thread(target = self.start_extra_download_thread).start()

    def start_video_download_thread(self):
        if not hasattr(self, "downloader"):
            self.downloader = Downloader(self.task_info, self.get_downloader_callback())

        if not hasattr(self, "download_parser"):
            self.download_parser = DownloadParser(self.task_info, self.onDownloadError)

        downloader_info = self.download_parser.get_download_url()

        self.task_info.download_path = FileNameFormatter.get_download_path(self.task_info)
        self.task_info.file_name = FileNameFormatter.format_file_basename(self.task_info)

        self.downloader.set_downloader_info(downloader_info)

        self.downloader.start_download()

    def start_extra_download_thread(self):
        ExtraParser.download(self.task_info, self.get_extra_callback())

    def pause_download(self, set_waiting_status: bool = False):
        self.set_download_status(DownloadStatus.Waiting if set_waiting_status else DownloadStatus.Pause)
        
        if hasattr(self, "downloader"):
            self.downloader.stop_download()

    def resume_download(self):
        if self.task_info.status != DownloadStatus.Downloading.value:
            if self.task_info.progress == 100:
                self.onDownloadVideoComplete()
            else:
                self.start_download()

    def merge_video(self, set_status: bool = True):
        def worker():
            FFmpeg.Utils.merge(self.task_info, self.get_merge_callback())

        if set_status:
            self.set_download_status(DownloadStatus.Merging)

        Thread(target = worker).start()

    def rename_file(self):
        FFmpeg.Utils.rename_files(self.task_info)

        self.onMergeSuccess()

    def onDownloadStart(self):
        def worker():
            self.parent.show_info = True

            self.show_task_info()

        if not self.parent.panel_destroy and not self.parent.show_info:
            wx.CallAfter(worker)

    def onDownloading(self, speed_label: str):
        def worker():
            self.ui.set_progress(self.task_info.progress)

            self.ui.set_speed_label(speed_label)
            self.ui.set_size_label(self.info.get_size_label())

            self.ui.update()

        if not self.parent.panel_destroy:
            wx.CallAfter(worker)

    def onDownloadVideoComplete(self):
        def worker():
            self.ui.set_size_label(self.info.get_size_label())

            self.ui.update()

        if self.task_info.further_processing:
            self.set_download_status(DownloadStatus.Merging)

            self.parent.download_window.start_next_task()

            if self.task_info.ffmpeg_merge:
                self.merge_video(set_status = False)
            else:
                self.rename_file()

            wx.CallAfter(worker)

    def onDownloadError(self):
        self.task_info.error_info = GlobalExceptionInfo.info

        self.set_download_status(DownloadStatus.DownloadError)

        self.parent.download_window.start_next_task()
    
    def onMergeSuccess(self):
        def worker():
            self.move_panel()

        self.set_download_status(DownloadStatus.Complete)

        wx.CallAfter(worker)

    def onMergeError(self):
        self.task_info.error_info = GlobalExceptionInfo.info
        
        self.set_download_status(DownloadStatus.MergeError)

    def onDownloadExtraSuccess(self):
        self.task_info.progress = 100

        self.task_info.update()

        self.onMergeSuccess()

    def clear_temp_files(self):
        match ParseType(self.task_info.download_type):
            case ParseType.Video | ParseType.Bangumi | ParseType.Cheese:
                if self.task_info.total_file_size:
                    FFmpeg.Utils.clear_temp_files(self.task_info)

    def open_file_location(self):
        path = os.path.join(self.task_info.download_path, self.get_full_file_name())

        Directory.open_file_location(path)

    def set_download_status(self, status: DownloadStatus):
        def worker():
            self.update_pause_btn(status)

            self.task_info.update()

        self.task_info.status = status.value

        wx.CallAfter(worker)

    def update_pause_btn(self, status: int):
        match DownloadStatus(status):
            case DownloadStatus.Waiting:
                self.ui.set_pause_btn(IconID.Play, "开始下载")
                self.ui.set_speed_label("等待下载...")

            case DownloadStatus.Downloading:
                self.ui.set_pause_btn(IconID.Pause, "暂停下载")
                self.ui.set_speed_label("正在获取下载链接...")

            case DownloadStatus.Generating:
                self.ui.set_pause_btn(IconID.Pause, "", False)
                self.ui.set_speed_label("正在生成中...")

            case DownloadStatus.Pause:
                self.ui.set_pause_btn(IconID.Play, "继续下载")
                self.ui.set_speed_label("暂停中...")

            case DownloadStatus.Merging:
                self.ui.set_pause_btn(IconID.Pause, "", False)
                self.ui.set_speed_label(self.info.get_merging_label())

            case DownloadStatus.Complete:
                self.ui.set_pause_btn(IconID.Folder, "打开文件所在位置")
                self.ui.set_speed_label("下载完成")

            case DownloadStatus.MergeError:
                self.ui.set_pause_btn(IconID.Retry, "重试")
                self.ui.set_speed_label(self.info.get_merge_error_label(), error = True)

            case DownloadStatus.DownloadError:
                self.ui.set_pause_btn(IconID.Retry, "重试")
                self.ui.set_speed_label("下载失败，点击查看详情", error = True)

        self.ui.update()

    def get_downloader_callback(self):
        class callback(DownloaderCallback):
            @staticmethod
            def onStart():
                self.onDownloadStart()

            @staticmethod
            def onDownloading(speed: str):
                self.onDownloading(speed)

            @staticmethod
            def onComplete():
                self.onDownloadVideoComplete()

            @staticmethod
            def onError():
                self.onDownloadError()

        return callback

    def get_extra_callback(self):
        class callback(Callback):
            @staticmethod
            def onSuccess(*process):
                self.onDownloadExtraSuccess()

            @staticmethod
            def onError(*process):
                self.onDownloadError()

        return callback

    def get_merge_callback(self):
        class callback(Callback):
            @staticmethod
            def onSuccess(*process):
                self.onMergeSuccess()

            @staticmethod
            def onError(*process):
                self.onMergeError()

        return callback
    
    def get_full_file_name(self):
        return FileNameFormatter.check_file_name_length(f"{self.task_info.file_name}.{self.task_info.output_type}")
    