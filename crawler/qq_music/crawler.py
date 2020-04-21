"""
    Get singer songs by qq music.

    Refer: https://github.com/yangjianxin1/QQMusicSpider
"""
import requests
from requests.adapters import HTTPAdapter

session = requests.Session()
adapters = HTTPAdapter(max_retries=3)
session.mount('https://', adapters)

SONG_BY_SINGER_URL = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22{singer_mid}%22%2C%22begin%22%3A{begin}%2C%22num%22%3A{num}%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D"


def get_song_from_qq(singer_mid: str, offset: int, limit: int):
    """
    Get music data list from qq
    Args:
        singer_mid: singer mid
        offset:
        limit:

    Returns:
        song data
    """

    try:
        resp = session.get(url=SONG_BY_SINGER_URL.format(singer_mid=singer_mid, begin=offset, num=limit))
        data = resp.json()
        if data["code"] == 0:
            return data["singerSongList"]["data"]["songList"]
        else:
            print(f"Error in req for singer {singer_mid}, offset: {offset}, limit: {limit}")
            return []
    except Exception as e:
        print(f"Exception in get song from qq. errors: {e}")
        return []


def handler():
    data = get_song_from_qq("000Sp0Bz4JXH0o", 0, 10)
    print(data)


if __name__ == '__main__':
    handler()
