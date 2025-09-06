import os
import json
from typing import List, Dict

from utils.config import Config

from utils.common.enums import DownloadStatus
from utils.common.io.file import File

class DownloadTaskInfo:
    def __init__(self):
        # 最低支持版本
        self.min_version: int = 0

        # id，区分不同下载任务的唯一标识符
        self.id: int = 0
        # 序号
        self.number: int = 0
        # 补零序号
        self.zero_padding_number: str = ""
        # 列表中的序号
        self.list_number: int = 0
        # 时间戳
        self.timestamp: int = 0
        # 分P序号
        self.page: int = 0
        
        # Referer URL
        self.referer_url: str = ""
        # 视频封面链接
        self.cover_url: str = ""

        # 视频 bvid 和 cid 信息
        self.bvid: str = ""
        self.cid: int = 0
        self.aid: int = 0
        self.ep_id: int = 0
        self.season_id: int = 0
        self.media_id: int = 0

        # 视频标题
        self.title: str = ""
        # 剧集系列名称
        self.series_title: str = ""
        # 章节标题
        self.section_title: str = ""
        # 分节标题
        self.part_title: str = ""
        # 合集标题
        self.collection_title: str = ""
        # 互动视频标题
        self.interact_title: str = ""
        # parent_title
        self.parent_title: str = ""

        # 视频时长
        self.duration: int = 0

        # 下载目录
        self.download_base_path: str = ""
        # 完整下载目录
        self.download_path: str = ""
        # 下载文件名
        self.file_name: str = ""
        # 下载进度
        self.progress: int = 0
        # 总大小，单位字节
        self.total_file_size: int = 0
        # 已下载完成的总大小，单位字节
        self.total_downloaded_size: int = 0
        # 已下载完成的当前任务大小
        self.current_downloaded_size: int = 0
        # 下载状态
        self.status: int = DownloadStatus.Waiting.value

        # 媒体信息，0 表示未定义
        self.video_quality_id: int = 0
        self.audio_quality_id: int = 00
        self.video_codec_id: int = 0
        self.video_type: str = ""
        self.audio_type: str = ""
        self.output_type: str = ""

        # 下载项目标识
        self.download_items: list = []

        # 解析类型
        self.parse_type: int = 0
        # 下载类型
        self.download_type: int = 0
        # 视频流类型
        self.stream_type: int = 0
        # 下载选项
        self.download_option: List[int] = []
        # 是否调用 FFmpeg 合并
        self.ffmpeg_merge: bool = False
        # 下载完成后是否对文件进行进一步处理
        self.further_processing = False
        # flv 视频个数，仅 flv 流时有效
        self.flv_video_count: int = 0

        # 附加内容选项
        self.extra_option: dict = {}

        # 视频发布时间戳
        self.pubtimestamp: int = 0
        # 地区
        self.area: str = ""
        # 分区信息
        self.zone: str = ""
        # 子分区信息
        self.subzone: str = ""
        # UP 主名称
        self.up_name: str = ""
        # UP 主uid
        self.up_uid: int = 0
        # 标识
        self.badge: str = ""
        # 剧集编号
        self.episode_num: int = 0
        # 剧集类型
        self.bangumi_type: str = ""
        # 模板类型
        self.template_type: int = 0

        # 视频宽度
        self.video_width: int = 0
        self.video_height: int = 0

        # 源
        self.source: str = ""

        self.thread_info: dict = {}
        self.error_info: dict = {}

    def to_dict(self):
        return {
            "min_version": self.min_version,

            "id": self.id,
            "number": self.number,
            "zero_padding_number": self.zero_padding_number,
            "list_number": self.list_number,
            "timestamp": self.timestamp,
            "page": self.page,

            "referer_url": self.referer_url,
            "cover_url": self.cover_url,

            "bvid": self.bvid,
            "cid": self.cid,
            "aid": self.aid,
            "ep_id": self.ep_id,
            "season_id": self.season_id,
            "media_id": self.media_id,

            "title": self.title,
            "series_title": self.series_title,
            "section_title": self.section_title,
            "part_title": self.part_title,
            "collection_title": self.collection_title,
            "interact_title": self.interact_title,
            "parent_title": self.parent_title,

            "duration": self.duration,

            "download_base_path": self.download_base_path,
            "download_path": self.download_path,
            "file_name": self.file_name,
            "progress": self.progress,
            "total_file_size": self.total_file_size,
            "total_downloaded_size": self.total_downloaded_size,
            "current_downloaded_size": self.current_downloaded_size,
            "status": self.status,

            "video_quality_id": self.video_quality_id,
            "audio_quality_id": self.audio_quality_id,
            "video_codec_id": self.video_codec_id,
            "video_type": self.video_type,
            "audio_type": self.audio_type,
            "output_type": self.output_type,

            "download_items": self.download_items,
            
            "parse_type": self.parse_type,
            "download_type": self.download_type,
            "stream_type": self.stream_type,
            "download_option": self.download_option,
            "ffmpeg_merge": self.ffmpeg_merge,
            "further_processing": self.further_processing,
            "flv_video_count": self.flv_video_count,

            "extra_option": self.extra_option,

            "pubtimestamp": self.pubtimestamp,
            "area": self.area,
            "zone": self.zone,
            "subzone": self.subzone,
            "up_name": self.up_name,
            "up_uid": self.up_uid,
            "badge": self.badge,
            "episode_num": self.episode_num,
            "bangumi_type": self.bangumi_type,
            "template_type": self.template_type,

            "video_width": self.video_width,
            "video_height": self.video_height,

            "source": self.source,

            "thread_info": self.thread_info,
            "error_info": self.error_info
        }

    def load_from_dict(self, data: Dict):
        self.min_version = data.get("min_version", self.min_version)

        self.id = data.get("id", self.id)
        self.number = data.get("number", self.number)
        self.zero_padding_number = data.get("zero_padding_number", self.zero_padding_number)
        self.list_number = data.get("list_number", self.list_number)
        self.timestamp = data.get("timestamp", self.timestamp)
        self.page = data.get("page", self.page)

        self.referer_url = data.get("referer_url", self.referer_url)
        self.cover_url = data.get("cover_url", self.cover_url)

        self.bvid = data.get("bvid", self.bvid)
        self.cid = data.get("cid", self.cid)
        self.aid = data.get("aid", self.aid)
        self.ep_id = data.get("ep_id", self.ep_id)
        self.season_id = data.get("season_id", self.season_id)
        self.media_id = data.get("media_id", self.media_id)

        self.title = data.get("title", self.title)
        self.series_title = data.get("series_title", self.series_title)
        self.section_title = data.get("section_title", self.section_title)
        self.part_title = data.get("part_title", self.part_title)
        self.collection_title = data.get("collection_title", self.collection_title)
        self.interact_title = data.get("interact_title", self.interact_title)
        self.parent_title = data.get("parent_title", self.parent_title)

        self.duration = data.get("duration", self.duration)

        self.download_base_path = data.get("download_base_path", self.download_base_path)
        self.download_path = data.get("download_path", self.download_path)
        self.file_name = data.get("file_name", self.file_name)
        self.progress = data.get("progress", self.progress)
        self.total_file_size = data.get("total_file_size", self.total_file_size)
        self.total_downloaded_size = data.get("total_downloaded_size", self.total_downloaded_size)
        self.current_downloaded_size = data.get("current_downloaded_size", self.current_downloaded_size)
        self.status = data.get("status", self.status)

        self.video_quality_id = data.get("video_quality_id", self.video_quality_id)
        self.audio_quality_id = data.get("audio_quality_id", self.audio_quality_id)
        self.video_codec_id = data.get("video_codec_id", self.video_codec_id)
        self.video_type = data.get("video_type", self.video_type)
        self.audio_type = data.get("audio_type", self.audio_type)
        self.output_type = data.get("output_type", self.output_type)

        self.download_items = data.get("download_items", self.download_items)

        self.parse_type = data.get("parse_type", self.parse_type)
        self.download_type = data.get("download_type", self.download_type)
        self.stream_type = data.get("stream_type", self.stream_type)
        self.download_option = data.get("download_option", self.download_option)
        self.ffmpeg_merge = data.get("ffmpeg_merge", self.ffmpeg_merge)
        self.further_processing = data.get("further_processing", self.further_processing)
        self.flv_video_count = data.get("flv_video_count", self.flv_video_count)

        self.extra_option = data.get("extra_option", self.extra_option)
        
        self.pubtimestamp = data.get("pubtimestamp", self.pubtimestamp)
        self.area = data.get("area", self.area)
        self.zone = data.get("zone", self.zone)
        self.subzone = data.get("subzone", self.subzone)
        self.up_name = data.get("up_name", self.up_name)
        self.up_uid = data.get("up_uid", self.up_uid)
        self.badge = data.get("badge", self.badge)
        self.episode_num = data.get("episode_num", self.episode_num)
        self.bangumi_type = data.get("bangumi_type", self.bangumi_type)
        self.template_type = data.get("template_type", self.template_type)

        self.video_width = data.get("video_width", self.video_width)
        self.video_height = data.get("video_height", self.video_height)

        self.source = data.get("source", self.source)

        self.thread_info = data.get("thread_info", self.thread_info)
        self.error_info = data.get("error_info", self.error_info)

    def load_from_file(self, file_path: str):
        with open(file_path, "r", encoding = "utf-8") as f:
            data = json.loads(f.read())

            self.load_from_dict(data)

    def update(self):
        self.min_version = Config.APP.task_file_min_version_code

        self.write(self.to_dict())

    def remove_file(self):
        File.remove_file(self.file_path)

    def write(self, contents: dict):
        with open(self.file_path, "w", encoding = "utf-8") as f:
            f.write(json.dumps(contents, ensure_ascii = False, indent = 4))

    def is_valid(self):
        return self.min_version >= Config.APP.task_file_min_version_code

    @property
    def file_path(self):
        return os.path.join(Config.User.download_file_directory, f"info_{self.id}.json")

class RangeDownloadInfo:
    def __init__(self):
        self.index: str = ""
        self.type: str = ""
        self.url: str = ""
        self.file_path: str = ""
        self.range: List[int] = []

class NotificationMessage:
    def __init__(self):
        self.video_title: str = ""
        self.status: int = 0
        self.video_merge_type: int = 0

class TreeListItemInfo:
    def __init__(self):
        self.number: int = 0
        self.page: int = 0
        self.episode_num: int = 0

        self.title: str = ""

        self.cid: int = 0
        self.aid: int = 0
        self.bvid: str = ""
        self.ep_id: int = 0
        self.season_id: int = 0
        self.media_id: int = 0

        self.pubtime: int = 0
        self.badge: str = ""
        self.duration: str = ""
        self.cover_url: str = ""
        self.link: str = ""

        self.pid: str = ""

        self.section_title: str = ""
        self.part_title: str = ""
        self.collection_title: str = ""
        self.series_title: str = ""
        self.interact_title: str = ""
        self.parent_title: str = ""

        self.area: str = ""
        self.zone: str = ""
        self.subzone: str = ""
        self.up_name: str = ""
        self.up_mid: int = 0

        self.item_type: str = "node"
        self.type: int = 0
        self.bangumi_type: str = ""
        self.template_type: int = 0

    def to_dict(self):
        return {
            "number": self.number,
            "page": self.page,
            "episode_num": self.episode_num,

            "title": self.title,

            "cid": self.cid,
            "aid": self.aid,
            "bvid": self.bvid,
            "ep_id": self.ep_id,
            "season_id": self.season_id,
            "media_id": self.media_id,

            "pubtime": self.pubtime,
            "badge": self.badge,
            "duration": self.duration,
            "cover_url": self.cover_url,
            "link": self.link,

            "pid": self.pid,

            "section_title": self.section_title,
            "part_title": self.part_title,
            "collection_title": self.collection_title,
            "series_title": self.series_title,
            "interact_title": self.interact_title,
            "parent_title": self.parent_title,

            "area": self.area,
            "zone": self.zone,
            "subzone": self.subzone,
            "up_name": self.up_name,
            "up_mid": self.up_mid,

            "item_type": self.item_type,
            "type": self.type,
            "bangumi_type": self.bangumi_type,
            "template_type": self.template_type
        }

    def load_from_dict(self, data: dict):
        self.number = data.get("number", self.number)
        self.page = data.get("page", self.page)
        self.episode_num = data.get("episode_num", self.episode_num)

        self.title = data.get("title", self.title)

        self.cid = data.get("cid", self.cid)
        self.aid = data.get("aid", self.aid)
        self.bvid = data.get("bvid", self.bvid)
        self.ep_id = data.get("ep_id", self.ep_id)
        self.season_id = data.get("season_id", self.season_id)
        self.media_id = data.get("media_id", self.media_id)

        self.pubtime = data.get("pubtime", self.pubtime)
        self.badge = data.get("badge", self.badge)
        self.duration = data.get("duration", self.duration)
        self.cover_url = data.get("cover_url", self.cover_url)
        self.link = data.get("link", self.link)

        self.pid = data.get("pid", self.pid)

        self.section_title = data.get("section_title", self.section_title)
        self.part_title = data.get("part_title", self.part_title)
        self.collection_title = data.get("collection_title", self.collection_title)
        self.series_title = data.get("series_title", self.series_title)
        self.interact_title = data.get("interact_title", self.interact_title)
        self.parent_title = data.get("parent_title", self.parent_title)

        self.area = data.get("area", self.area)
        self.zone = data.get("zone", self.zone)
        self.subzone = data.get("subzone", self.subzone)
        self.up_name = data.get("up_name", self.up_name)
        self.up_mid = data.get("up_mid", self.up_mid)

        self.item_type = data.get("item_type", self.item_type)
        self.type = data.get("type", self.type)
        self.bangumi_type = data.get("bangumi_type", self.bangumi_type)
        self.template_type = data.get("template_type", self.template_type)

class Command:
    def __init__(self):
        self.command = []

    def add(self, command: str):
        self.command.append(command)

    def clear(self):
        self.command.clear()

    def format(self):
        return " && ".join(self.command)

class Process:
    output: str = None
    return_code: int = None

class CommentData:
    def __init__(self):
        self.start_time: int = 0
        self.end_time: int = 0
        self.text: str = ""
        self.width: int = 0
        self.row: int = 0

class ASSStyle:
    Name: str = "Default"
    Fontname: str = ""
    Fontsize: int = 48
    PrimaryColour: str = ""
    SecondaryColour: str = ""
    OutlineColour: str = ""
    BackColour: str = ""
    Bold: int = 0
    Italic: int = 0
    Underline: int = 0
    StrikeOut: int = 0
    ScaleX: int = 100
    ScaleY: int = 100
    Spacing: int = 0
    Angle: int = 0
    BorderStyle: int = 1
    Outline: int = 0
    Shadow: int = 0
    Alignment: int = 2
    MarginL: int = 0
    MarginR: int = 0
    MarginV: int = 0
    Encoding: int = 1

    @classmethod
    def to_string(cls):
        values = [str(value) for key, value in cls.__dict__.items() if not key.startswith("__") and key != "to_string"]

        return ",".join(values)

class LiveRoomInfo:
    def __init__(self):
        self.min_version: int = 0

        self.cover_url: str = ""

        self.room_id: int = 0

        self.up_name: str = ""
        self.title: str = ""

        self.parent_area: str = ""
        self.area: str = ""

        self.live_status: int = 0
        self.recording_status: int = 0

        self.option_setuped: bool = False

        self.base_directory: str = ""
        self.working_directory: str = ""
        self.quality: int = 0
        self.codec: int = 0

        self.total_size: int = 0

        self.file_split: int = 0
        self.split_unit: int = 100

        self.timestamp: int = 0

    def to_dict(self):
        return {
            "min_version": self.min_version,

            "cover_url": self.cover_url,

            "room_id": self.room_id,

            "up_name": self.up_name,
            "title": self.title,

            "parent_area": self.parent_area,
            "area": self.area,

            "live_status": self.live_status,
            "recording_status": self.recording_status,

            "option_setuped": self.option_setuped,

            "base_directory": self.base_directory,
            "working_directory": self.working_directory,
            "quality": self.quality,
            "codec": self.codec,

            "total_size": self.total_size,

            "file_split": self.file_split,
            "split_unit": self.split_unit,

            "timestamp": self.timestamp
        }

    def load_from_dict(self, data: dict):
        self.min_version = data.get("min_version", self.min_version)
        
        self.cover_url = data.get("cover_url", self.cover_url)

        self.room_id = data.get("room_id", self.room_id)

        self.up_name = data.get("up_name", self.up_name)
        self.title = data.get("title", self.title)

        self.parent_area = data.get("parent_area", self.parent_area)
        self.area = data.get("area", self.area)

        self.live_status = data.get("live_status", self.live_status)
        self.recording_status = data.get("recording_status", self.recording_status)

        self.option_setuped = data.get("option_setuped", self.option_setuped)

        self.base_directory = data.get("base_directory", self.base_directory)
        self.working_directory = data.get("working_directory", self.working_directory)
        self.quality = data.get("quality", self.quality)
        self.codec = data.get("codec", self.codec)

        self.total_size = data.get("total_size", self.total_size)

        self.file_split = data.get("file_split", self.file_split)
        self.split_unit = data.get("split_unit", self.split_unit)

        self.timestamp = data.get("timestamp", self.timestamp)

    def load_from_file(self, file_path: str):
        with open(file_path, "r", encoding = "utf-8") as f:
            data = json.loads(f.read())

            self.load_from_dict(data)

    def update(self):
        self.min_version = Config.APP.live_file_min_version_code

        self.write(self.to_dict())

    def remove_file(self):
        File.remove_file(self.file_path)

    def write(self, contents: dict):
        with open(self.file_path, "w", encoding = "utf-8") as f:
            f.write(json.dumps(contents, ensure_ascii = False, indent = 4))

    def is_valid(self):
        return self.min_version >= Config.APP.live_file_min_version_code

    @property
    def file_path(self):
        return os.path.join(Config.User.live_file_directory, f"info_{self.room_id}.json")