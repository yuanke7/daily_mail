"""
    Get singer songs by qq music.

    Refer: https://github.com/yangjianxin1/QQMusicSpider

    ``` bash
    cd crawler/qq_music
    python crawler.py initdb
    python crawler.py crawler -s {singer_mid}
    ```

"""
import sqlite3
import sys
import time

import click
import requests
from requests.adapters import HTTPAdapter

sys.path.append("../../")
import config

session = requests.Session()
adapters = HTTPAdapter(max_retries=3)
session.mount('https://', adapters)

SONG_BY_SINGER_URL = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22singerSongList%22%3A%7B%22method%22%3A%22GetSingerSongList%22%2C%22param%22%3A%7B%22order%22%3A1%2C%22singerMid%22%3A%22{singer_mid}%22%2C%22begin%22%3A{begin}%2C%22num%22%3A{num}%7D%2C%22module%22%3A%22musichall.song_list_server%22%7D%7D"


def init_db(filename):
    table_sql = """CREATE TABLE `song`(
    id INT PRIMARY KEY,
    mid VARCHAR(100)  NOT NULL,
    singer_mid VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    created_at INT NOT NULL)"""

    if filename is None:
        filename = config.DB_PATH

    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute(table_sql)
    cursor.close()
    conn.close()


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


def save_to_db(filename, singer_mid, data):
    now_time = int(time.time())
    params = []
    for song in data:
        song_info = song["songInfo"]
        item = [
            song_info["mid"], singer_mid,
            song_info["name"], song_info["title"], now_time
        ]
        params.append(item)

    conn = sqlite3.connect(filename)
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.executemany(
            "INSERT INTO song(mid, singer_mid, name, title, created_at) "
            "VALUES (?,?,?,?,?)",
            params
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Exception save data to db, errors: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        conn.close()


def handler(filename, singer_mid):
    offset = 0
    limit = 100
    while 1:
        data = get_song_from_qq(singer_mid, offset, limit)
        if data:
            st = save_to_db(filename, singer_mid, data)
            click.echo(f"Save data for offset: {offset}, limit: {limit}, status: {st}")
        else:
            break

        offset += limit
    return True


@click.group()
def cli():
    pass


@cli.command(help="Initial database")
@click.option("--filename", "-f", default=None)
def initdb(filename):
    click.echo("Begin to initial db.")
    init_db(filename)
    click.echo("Finished initial.")


@cli.command(help="Crawler music for singer")
@click.option("--filename", "-f", default=None)
@click.option("--singer", "-s", help="The singer mid", default=None)
def crawler(filename, singer):
    if singer is None:
        click.echo("You must need provide singer mid!")
        return

    if filename is None:
        filename = config.DB_PATH

    handler(filename, singer)


if __name__ == '__main__':
    cli()
