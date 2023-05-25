import datetime
import json

import zmail
from loguru import logger
from settings import receivers, sender, pwd, bccs
from lottery import Lottery

ins = Lottery(high_probability=True)
today = datetime.datetime.today().strftime('%Y-%m-%d')
logger.add('log/' + today + '.log')
server = zmail.server(sender,
                      pwd,
                      smtp_host="smtp.qq.com",
                      smtp_port=465)

json_name = 'today_send.json'


def main(debug=False):
    items = {}

    for recv in receivers:

        daletou_str, daletou = ins.recommand_number_daletou(2)
        mail_daletou = {
            'subject': f'大乐透推荐号码 {today}',
            'content_text': f'今天是{today}, 为您推荐以下号码，祝您早日中大奖，发大财！\n\n {daletou_str}',
        }

        # mail_double_color = {
        #     'subject': f'双色球推荐号码 {today}',
        #     'content_text': f'今天是{today}, 为您推荐以下号码，祝您早日中大奖，发大财！\n\n {ins.recommand_number_doublecolor(8)}',
        # }

        addr = recv.get('email')
        items[addr] = daletou

        if not debug:
            if recv.get('大乐透'):
                server.send_mail(recipients=addr, mail=mail_daletou, cc=bccs)  # 接收者
                logger.info(f'Sending mail({mail_daletou}) to {addr}')

            # if recv.get('双色球'):
            #     server.send_mail(recipients=addr, mail=mail_double_color, cc=bccs)  # 接收者
            #     logger.info(f'Sending mail({mail_double_color}) to {addr}')

    # 写入
    with open(json_name, 'w') as f:
        json.dump(items, f)


def check():
    today_win = ins.get_history()
    today_win = today_win.to_dict('records')[0]
    today = today_win['date']
    front = today_win['front'].split(' ')
    back = today_win['back'].split(' ')
    win_shot = {'front': [int(item) for item in front], 'back': [int(item) for item in back]}

    logger.warning(win_shot)

    with open(json_name, 'rb') as f:
        data = json.loads(f.read())

    for recv, items in data.items():
        win_info_lst = []
        for item in items:
            win_info = ins.check_prize_of_shot(win_shot=win_shot, my_shot=item, date=today)
            if win_info:
                win_info_lst.append(win_info)

        win_info_sum = '\n\n'.join(win_info_lst)
        content = f"""今天是{today}, {' 恭喜您中奖了！ 详情如下：' if win_info_lst else '很遗憾本期推荐未中奖，敬请期待下一次开奖推荐！'}
        \n\n{win_info_sum}\n\n
        {'千万不要忘记去兑奖嗷 ~~~' if win_info_lst else '越努力越幸运, 人生不如意十之八九, 一定要相信明天会更好！'}
        """

        mail_daletou = {
            'subject': f'大乐透今日推荐号码中奖情况 {today}',
            'content_text': content,
        }
        server.send_mail(recipients=recv, mail=mail_daletou, cc=bccs)  # 接收者
        logger.info(f'Sending mail({mail_daletou}) to {recv}')


if __name__ == '__main__':
    main(debug=False)
    # check()
