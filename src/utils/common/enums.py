from enum import Enum

class ParseType(Enum):
    Video = 1                     # 投稿视频
    Bangumi = 2                   # 番组
    Live = 3                      # 直播
    Cheese = 4                    # 课程
    List = 5                      # 合集列表
    Space = 6                     # 个人主页
    Popular = 7                   # 热榜
    FavList = 8                   # 收藏夹
    Extra = 100                   # 弹幕、字幕、封面等类型文件
    B23 = 101                     # 短链接
    Festival = 102                # 活动专题

class VideoType(Enum):
    Single = 1                    # 单个视频
    Part = 2                      # 分 P 视频
    Collection = 3                # 合集

class EpisodeDisplayType(Enum):
    Single = 1                    # 获取单个视频
    In_Section = 2                # 获取视频所在的列表
    All = 3                       # 获取全部相关视频

class LiveStatus(Enum):
    Not_Started = 0               # 未开播
    Live = 1                      # 直播中
    Replay = 2                    # 轮播中

class ProxyMode(Enum):
    Disable = 0                   # 不使用
    Follow = 1                    # 跟随系统
    Custom = 2                    # 手动设置

class DanmakuType(Enum):
    XML = 0                       # XML 格式
    Protobuf = 1                  # Protobuf 格式
    JSON = 2                      # JSON 格式
    ASS = 3                       # ASS 格式

class SubtitleType(Enum):
    SRT = 0                       # SRT 格式
    TXT = 1                       # TXT 格式
    LRC = 2                       # LRC 格式
    JSON = 3                      # JSON 格式
    ASS = 4                       # ASS 格式

class CoverType(Enum):
    JPG = 0                       # jpg 格式
    PNG = 1                       # png 格式
    WEBP = 2                      # Webp 格式
    AVIF = 3                      # avif 格式

class StreamType(Enum):
    Dash = "DASH"                 # dash 流
    Flv = "FLV"                   # flv 流
    Mp4 = "MP4"                   # mp4 流

class DownloadStatus(Enum):
    Waiting = 0                   # 等待下载
    Downloading = 1               # 下载中
    Pause = 2                     # 暂停中
    Merging = 3                   # 合成中
    Complete = 4                  # 下载完成
    DownloadError = 5             # 下载失败
    MergeError = 6                # 合成失败
    Invalid = 7                   # 视频失效

    Alive = [Waiting, Downloading, Pause]
    Alive_Ex = [Waiting, Downloading, Pause, MergeError, DownloadError]

class StatusCode(Enum):
    Success = 0                   # 请求成功
    Vip = 600                     # 会员认证
    Pay = 601                     # 付费购买
    URL = 602                     # 无效链接
    Redirect = 603                # 跳转链接
    CallError = 610               # 调用出错
    DownloadError = 611           # 下载失败
    MaxRetry = 612                # 最大重试
    Cancel = 613                  # 取消解析
    DRM = 614                     # DRM 加密
    Area_Limit = -10403           # 区域限制
    NotLogin = -101               # 未登录
    CSRFError = -111              # CSRF 校验失败
    RefreshTokenError = 86095     # Refresh Token 不匹配
    OtherError = None             # 其他错误

class VideoQualityID(Enum):
    _None = 0                     # 无视频
    _360P = 16                    # 360P
    _480P = 32                    # 480P
    _720P = 64                    # 720P
    _1080P = 80                   # 1080P
    _1080P_P = 112                # 1080P 高码率
    _1080P_60 = 116               # 1080P 60帧
    _4K = 120                     # 4K
    _HDR = 125                    # HDR
    _Dolby_Vision = 126           # 杜比视界
    _8K = 127                     # 8K
    _Auto = 200                   # 自动

class AudioQualityID(Enum):
    _None = 0                     # 无音频
    _64K = 30216                  # 64K
    _132K = 30232                 # 132K
    _192K = 30280                 # 192K
    _Dolby_Atoms = 30250          # 杜比全景声
    _Hi_Res = 30251               # Hi-Res 无损
    _Auto = 30300                 # 自动

class VideoCodecID(Enum):
    AVC = 7                       # H264
    HEVC = 12                     # H265
    AV1 = 13                      # AV1

class OverrideOption(Enum):
    Override = 0                  # 覆盖文件
    Rename = 1                    # 重命名

class Platform(Enum):
    Windows = "windows"           # Windows
    Linux = "linux"               # Linux
    macOS = "darwin"              # macOS

class ParseStatus(Enum):
    Success = 0                   # 解析完成
    Parsing = 1                   # 解析中
    Error = 2                     # 解析失败

class NumberType(Enum):
    From_1 = 0                    # 从 1 开始
    Coherent = 1                  # 连续序号
    Episode_List = 2              # 剧集列表序号

class ProcessingType(Enum):
    Process = 1                   # 处理
    Parse = 2                     # 解析
    Interact = 3                  # 解析互动视频
    Page = 4                      # 解析分页

class ExitOption(Enum):
    TaskIcon = 0                  # 托盘图标
    Exit = 1                      # 直接退出
    Ask = 2                       # 总是询问
    AskOnce = 3                   # 询问一次

class SubtitleLanOption(Enum):
    All_Subtitles_With_AI = 0     # 下载全部字幕 + AI 字幕
    All_Subtitles = 1             # 下载全部字幕
    Custom = 2                    # 自定义

class ScopeID(Enum):
    All = 0                       # 所有类型
    Video = 1                     # 投稿视频
    Bangumi = 2                   # 剧集
    Cheese = 3                    # 课程
    Default = 4                   # 默认

class QRCodeStatus(Enum):
    Success = 0                   # 成功
    Confirm = 86090               # 未确认
    Outdated = 86038              # 已失效
    NotScan = 86101               # 未扫码

class WebPageOption(Enum):
    Auto = 0                      # 自动检测
    Webview = 1                   # 使用 Webview
    Websocket = 2                 # 使用 Websocket

class LiveRecordingStatus(Enum):
    Free = 0                      # 未录制
    Recording = 1                 # 录制中

class LiveFileSplit(Enum):
    Disable = 0                   # 不分段
    ByDuration = 1                # 按直播时长分段
    BySize = 2                    # 按文件大小分段

class TemplateType(Enum):
    Video_Normal = 1              # 普通
    Video_Part = 2                # 分P
    Video_Collection = 3          # 合集
    Video_Interact = 4            # 互动视频
    Bangumi = 5                   # 剧集
    Cheese = 6                    # 课程
    Space = 7
    Favlist = 8