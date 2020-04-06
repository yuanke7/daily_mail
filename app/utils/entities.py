"""
    一些实体类
"""
from dataclasses import dataclass

AIR_BACK_COLOR = {
    "level_1": "#8fc31f",
    "level_2": "#d7af0e",
    "level_3": "#f39800",
    "level_4": "#e2361a",
    "level_5": "#5f52a0",
    "level_6": "#631541",
}


@dataclass
class Weather:
    day: str
    wea: str
    wea_icon: str
    temp: str
    wind: str
    air: str
    air_level: str

    def get_air_color(self):
        return AIR_BACK_COLOR.get(self.air_level)


@dataclass
class Image:
    one: str = ""
    xingzuowu: str = ""


@dataclass
class Content:
    title: str = ""
    shici_say: str = ""
    hitokoto_say: str = ""
