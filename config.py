"""
    config
"""

sentry_dsn = ""

sender = ""
email_password = ""
receiver = ""
sender_name = ""
receiver_name = ""
constellation = ''

NICK_NAME = []  # 随机挑选昵称作为标题

# crawler
AREA = "china/beijing/haidian-district"

# image
IMAGE_FILE_PATH = "img"
CONSTELLATION_MAP = {'白羊': 'Aries', '金牛': 'Taurus', '双子': 'Gemini',
                     '巨蟹': 'Cancer', '狮子': 'Leo', '处女': 'Virgo',
                     '天秤': 'Libra', '天蝎': 'Scorpio', '射手': 'Sagittarius',
                     '摩羯': 'Capricorn', '水瓶': 'Aquarius', '双鱼': 'Pisces'}
XINGZUOWU_URL = "https://www.xzw.com/fortune/"
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
    from lottery_proj.local_settings import *
except ImportError:
    pass
