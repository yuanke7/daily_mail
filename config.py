"""
    配置
"""

sentry_dsn = ""

sender = ""
email_password = ""
receiver = ""
sender_name = ""
receiver_name = ""

NICK_NAME = []  # 随机挑选昵称作为标题

# crawler
AREA = "china/beijing/haidian-district"

# image
IMAGE_FILE_PATH = "img"
XINGZUOWU_URL = "https://www.xzw.com/fortune/scorpio/"
ONE_URL = "http://wufazhuce.com/"

# says
HITOKOTO_URL = "https://v1.hitokoto.cn/?type=b"
JINRISHICI_URL = "https://v1.jinrishici.com/shuqing/aiqing"

# DB
DB_PATH = "music.db"
PG_HOST = "127.0.0.1"
PG_USER = "ikaros"
PG_PASSWORD = "123456"
PG_DB = "love_db"

DEFAULT_DRIVER = ""

try:
    from local_settings import *
except ImportError:
    pass
