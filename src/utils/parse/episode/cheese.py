from utils.common.enums import ParseType, TemplateType
from utils.common.map import cheese_status_map

from utils.parse.episode.episode_v2 import EpisodeInfo, Filter

class Cheese:
    target_section_title: str = ""
    target_ep_id: int = 0

    @classmethod
    def parse_episodes(cls, info_json: dict, target_ep_id: int = None):
        cls.target_ep_id = target_ep_id
        EpisodeInfo.parser = cls

        EpisodeInfo.clear_episode_data()

        cls.sections_parser(info_json)

        Filter.episode_display_mode()

    @classmethod
    def sections_parser(cls, info_json: dict, parent_title: str = ""):
        episode_info_list = []

        if not parent_title:
            cheese_pid = EpisodeInfo.add_item(EpisodeInfo.root_pid, EpisodeInfo.get_node_info(info_json.get("title"), label = "课程"))

        for section in info_json["sections"]:
            if section["episodes"]:
                section_title = section["title"]

                if not parent_title:
                    section_pid = EpisodeInfo.add_item(cheese_pid, EpisodeInfo.get_node_info(section_title, label = "章节"))

                for episode in section["episodes"]:
                    episode["section_title"] = section_title
                    episode["season_id"] = info_json["season_id"]

                    entry_info = cls.get_entry_info(episode.copy(), info_json, parent_title)

                    if parent_title:
                        episode_info_list.append(entry_info)
                    else:
                        EpisodeInfo.add_item(section_pid, entry_info)

                        cls.update_target_section_title(episode, section_title)

        return episode_info_list
    
    @classmethod
    def get_entry_info(cls, episode: dict, info_json: dict, parent_title: str):
        episode["pubtime"] = episode.get("release_date")
        episode["ep_id"] = episode.get("id")
        episode["badge"] = cls.get_badge(episode)
        episode["cover_url"] = episode.get("cover")
        episode["link"] = f"https://www.bilibili.com/cheese/play/ep{episode.get('id')}"
        episode["type"] = ParseType.Cheese.value
        episode["series_title"] = info_json.get("title")
        episode["up_name"] = info_json.get("up_info", {"uname": ""}).get("uname", "")
        episode["up_mid"] = info_json.get("up_info", {"mid": 0}).get("mid", 0)
        episode["template_type"] = TemplateType.Cheese.value
        episode["parent_title"] = parent_title

        return EpisodeInfo.get_entry_info(episode)
    
    @classmethod
    def update_target_section_title(cls, episode: dict, section_title: str):
        if episode.get("id") == cls.target_ep_id:
            cls.target_section_title = section_title

    @classmethod
    def condition_single(cls, episode: dict):
        return episode.get("item_type") == "item" and episode.get("ep_id") == cls.target_ep_id
    
    @classmethod
    def condition_in_section(cls, episode: dict):
        return episode.get("item_type") == "node" and episode.get("title") == cls.target_section_title
    
    @classmethod
    def get_badge(cls, episode: dict):
        if "label" in episode:
            return episode["label"]
        else:
            if episode["status"] != 1:
                return cheese_status_map.get(episode.get("status"))
            else:
                return ""