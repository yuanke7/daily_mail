"""
    拼接并发送邮件
"""
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

import requests
import sentry_sdk
from jinja2 import Environment, PackageLoader

import config
from app.utils.entities import Content, Image
from app.utils.weather_crawler import WeatherCrawler
from app.utils.screenshot_lib import Driver

sentry_sdk.init(dsn=config.sentry_dsn)


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
        if not config.CONTENT_TITLE:
            content.title = f"早安，{wea.get_tips()}"
        else:
            content.title = config.CONTENT_TITLE
        weather_data = wea.get_days_wea()

    # 获取截图
    image = get_image_code()

    # 获取一言
    content.hitokoto_say = get_hitokoto_say()
    print(f"获得一言： {content.hitokoto_say}")

    # 获取今日诗词
    content.shici_say = get_gushici_say()

    # 生成 HTML 文件
    env = Environment(loader=PackageLoader("app"))
    template = env.get_template("hei.html")
    html_content = template.render(
        content=content, weather_data=weather_data, image=image
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
        print(f"Exception in get hitokoto say, errors: {e}")
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
        print(f"Exception in get jinri shici, errors: {e}")
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
            url=config.ONE_URL, filename=one_filename, class_name="carousel-inner"
        )
        img.one = f"data:image/png;base64,{webdriver.to_base64(one_filename)}"

    # xingzuowu
    xzw_filename = f"{config.IMAGE_FILE_PATH}/xzw.png"
    with Driver() as webdriver:
        webdriver.save_screenshot(
            url=config.XINGZUOWU_URL,
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
    message["From"] = _format_address("Ikaros", config.sender)
    message["To"] = _format_address("柠柠", config.receiver)

    subject = config.EMAIL_SUBJECT
    message["Subject"] = Header(subject, "utf-8")

    try:
        smtp_obj = smtplib.SMTP("smtp.qq.com", port=587)
        smtp_obj.ehlo("smtp.qq.com")
        smtp_obj.login(config.sender, config.email_password)
        smtp_obj.sendmail(config.sender, [config.receiver], message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def handler():
    """
    流程处理函数
    """
    print(f"Begin task at {datetime.now().isoformat()}")
    # HTML 文件
    try:
        html = render_html()
    except Exception as e:
        sentry_sdk.capture_exception(e)
        print(f"Exception in render html. errors: {e}")
        return False

    # 下发邮件
    send_email(html)
    print(f"End task at {datetime.now().isoformat()}")


if __name__ == "__main__":
    handler()
