"""
    墨迹天气爬虫模块
"""

from typing import Optional, List
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

import config

BASE_URL = "https://tianqi.moji.com/weather/"
AREA = config.AREA

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


def get_weather_html() -> Optional[BeautifulSoup]:
    try:
        resp = requests.get(BASE_URL + AREA)
        soup = BeautifulSoup(resp.text, "lxml")
        return soup
    except Exception as e:
        print(f"Exception in get html. errors: {e}")
        return None


def get_tips(soup: BeautifulSoup) -> str:
    return soup.select(".left > .wea_tips.clearfix > em")[0].get_text()


def get_days_wea(soup: BeautifulSoup) -> List[Weather]:
    days_forecast: List[BeautifulSoup] = soup.select(".wrap.clearfix")[2].select(
        ".left > .forecast.clearfix > .days.clearfix"
    )

    data_set = []
    for day_f in days_forecast:
        day = day_f.select("li")[0].get_text().strip()
        wea = day_f.select("li")[1].get_text().strip()
        wea_icon = day_f.select("li > span > img")[0]["src"]
        temp = day_f.select("li")[2].get_text().strip()
        wind = day_f.select("li")[3].select("em")[0].get_text()
        wind_level = day_f.select("li")[3].select("b")[0].get_text()
        air = day_f.select("li")[4].get_text().strip()
        air_level = day_f.select("li")[4].select("strong")[0]["class"][0]

        data_set.append(
            Weather(
                day=day,
                wea=wea,
                wea_icon=wea_icon,
                temp=temp,
                wind=f"{wind}--{wind_level}",
                air=air,
                air_level=air_level,
            )
        )

    return data_set
