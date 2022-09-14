"""
    拼接并发送邮件
"""
import random
import smtplib
from datetime import datetime, date
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from pathlib import Path
import requests
from jinja2 import Environment, PackageLoader
from loguru import logger

import config
from app.utils.entities import Content, Image
from app.utils.weather_crawler import WeatherCrawler
from app.utils.screenshot_lib import Driver

def get_edm_config():
    day = date.today().isoformat()
    conn = psycopg2.connect(
        database=config.PG_DB, user=config.PG_USER,
        password=config.PG_PASSWORD, host=config.PG_HOST
    )
    with conn.cursor() as cur:
        cur.execute(
            "SELECT subject,title FROM official_edmconfig "
            "WHERE day=%s;",
            (day,)
        )
        row = cur.fetchone()
        if row:
            return row
    conn.close()
    return "", ""


def update_edm_config(poetry, hitokoto):
    day = date.today().isoformat()
    conn = psycopg2.connect(
        database=config.PG_DB, user=config.PG_USER,
        password=config.PG_PASSWORD, host=config.PG_HOST
    )
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE official_edmconfig SET poetry=%s,hitokoto=%s "
                "WHERE day=%s;",
                (poetry, hitokoto, day)
            )
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Update db error: {e}")
    finally:
        conn.close()


def render_html() -> str:
    """
    获取数据并渲染 HTML 文件
    """
    # 准备数据
    # 初始化基础信息类
    content = Content()

    # 获取天气信息
    with WeatherCrawler() as wea:
        wea: WeatherCrawler
        # _, title = get_edm_config()
        # if not title:
        content.title = f"早安，亲爱的你"
        # else:
        #     content.title = title
        wea_tips = wea.get_tips() or "快来看今天的天气呀"
        weather_data = wea.get_days_wea()

    # 获取截图
    image = get_image_code()

    # 获取一言
    content.hitokoto_say = get_hitokoto_say()
    logger.info(f"获得一言： {content.hitokoto_say}")

    # 获取今日诗词
    content.shici_say = get_gushici_say()

    # update_edm_config(poetry=content.shici_say, hitokoto=content.hitokoto_say)

    # 生成 HTML 文件
    env = Environment(loader=PackageLoader("app"))
    template = env.get_template("hei.html")
    html_content = template.render(
        content=content, weather_data=weather_data, image=image,
        wea_tips=wea_tips,
    )
    return html_content


def get_hitokoto_say() -> str:
    default_msg = "看，你的眼里有星辰大海！"
    try:
        resp = requests.get(config.HITOKOTO_URL)
        if resp.status_code == 200:
            data = resp.json()
            return data["hitokoto"]
        else:
            return default_msg
    except Exception as e:
        logger.error(f"Exception in get hitokoto say, errors: {e}")
        return default_msg


def get_gushici_say() -> str:
    default_msg = "北方有佳人，绝世而独立。"
    try:
        resp = requests.get(config.JINRISHICI_URL)
        if resp.status_code == 200:
            data = resp.json()
            return data["content"]
        else:
            return default_msg
    except Exception as e:
        logger.error(f"Exception in get jinri shici, errors: {e}")
        return default_msg


def get_image_code() -> Image:
    """
    获取 一个 和 星座屋的截图
    """
    img = Image()

    # one
    one_filename = f"{config.IMAGE_FILE_PATH}/one.png"
    with Driver() as webdriver:
        webdriver.save_screenshot(
            url=config.ONE_URL, filename=one_filename, class_name="carousel-inner",
            one=True,
        )
        img.one = f"data:image/png;base64,{webdriver.to_base64(one_filename)}"

    # xingzuowu
    xzw_filename = f"{config.IMAGE_FILE_PATH}/xzw.png"
    with Driver() as webdriver:
        webdriver.save_screenshot(
            url=config.XINGZUOWU_URL + config.CONSTELLATION_MAP.get(config.constellation),
            filename=xzw_filename,
            class_name="c_main",
            xzw=True
        )
        img.xingzuowu = f"data:image/png;base64,{webdriver.to_base64(xzw_filename)}"

    return img


def send_email(html):
    def _format_address(name, addr):
        return formataddr((Header(name, "utf-8").encode(), addr))

    message = MIMEText(html, "html", "utf-8")
    message["From"] = _format_address(config.sender_name, config.sender)
    message["To"] = _format_address(config.receiver_name, config.receiver)

    # subject, _ = get_edm_config()
    # if not subject:
    subject = f"早安，{random.choice(config.NICK_NAME)}"
    message["Subject"] = Header(subject, "utf-8")

    smtp_obj = smtplib.SMTP("smtp.qq.com", port=587)
    smtp_obj.ehlo("smtp.qq.com")
    smtp_obj.login(config.sender, config.email_password)
    smtp_obj.sendmail(config.sender, config.receiver, message.as_string())
    logger.info("邮件发送成功")


def handler():
    """
    流程处理函数
    """
    logger.info(f"Begin task.")
    # HTML 文件
    html = render_html()
    # 存储一下每日的html源
    month = date.today().strftime("%Y%m")
    p = Path(config.IMAGE_FILE_PATH) / month
    if not p.exists():
        p.mkdir(parents=True)
    with open(f"{p}/{date.today().isoformat()}.html", "w") as f:
        f.write(html)
    # 下发邮件
    send_email(html)
    logger.info(f"End task.")


if __name__ == "__main__":
    handler()
