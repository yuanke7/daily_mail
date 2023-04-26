import datetime

import zmail
from loguru import logger

from lottery_proj.config import receivers
from lottery_proj.lottery import Lottery


ins = Lottery(high_probability=False)
today = datetime.datetime.today().strftime('%Y-%m-%d')
logger.add(today)
mail = {
    'subject': f'大乐透推荐号码 {today}',  # Anything you want.
    'content_text': f'今天是{today}, 为您推荐以下号码，祝您早日中大奖，发大财！\n\n {ins.recommand_number(2)}',
}

server = zmail.server('yuanke7@foxmail.com',
                      'ewppwarmavnzhiad',
                      smtp_host="smtp.qq.com",
                      smtp_port=465)

server.send_mail(receivers, mail)  # 接收着

logger.info(f'Sending mail({mail}) to {receivers}')
