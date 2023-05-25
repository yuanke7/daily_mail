import collections
import datetime
import json
import random

import pandas
import requests
from loguru import logger
from lxml import etree
from tqdm import tqdm


class Lottery:
    FRONT_SINGLE = [i for i in range(1, 10)]
    FRONT_DOUBLE = [i for i in range(10, 36)]
    BACK_SINGLE = [i for i in range(1, 10)]
    BACK_DOUBLE = [i for i in range(10, 13)]
    FRONT_COL = ['front_1', 'front_2', 'front_3', 'front_4', 'front_5']
    BACK_COL = ['back_1', 'back_2']
    # double c
    DC_FRONT = [i for i in range(1, 34)]
    DC_BACK = [i for i in range(1, 17)]

    def __init__(self, high_probability: bool = False):
        # self.con = create_engine(f"mysql+pymysql://root:123456@localhost/invest?charset=utf8")
        # self.df = pd.read_sql(con=self.con, sql='select * from invest.lottery_proj order by date_num')
        # self.front = list(np.concatenate(self.df[self.FRONT_COL].values))
        # self.back = list(np.concatenate(self.df[self.BACK_COL].values))
        if high_probability:
            self.FRONT_SINGLE = [5, 7, 1]
            self.FRONT_DOUBLE = [19,
                                 31,
                                 22,
                                 34,
                                 32,
                                 30,
                                 33,
                                 35,
                                 29]
            self.BACK_SINGLE = [6, 2, 4, 9, 3, 5, 7]
            self.BACK_DOUBLE = [10, 11, 12]

    # 前后区号码出现的频率
    def num_frequency(self):
        front_map = {}
        for i in range(1, 36):
            nums = self.front.count(i)
            front_map[i] = round(nums / len(self.front), 4)
        front_map = dict(sorted(front_map.items(), key=lambda x: x[1]))

        back_map = {}
        for i in range(1, 13):
            nums = self.back.count(i)
            back_map[i] = round(nums / len(self.back), 4)
        back_map = dict(sorted(back_map.items(), key=lambda x: x[1]))

        print(front_map, back_map)
        return front_map, back_map

    # 前区两位数与一位数的组合关系频率
    def group_frequency(self, df, partition: str):
        # 统计每一行数字是 n 个一位数和 m 个两位数的组合出现概率
        result = {}
        total_rows = df.shape[0]
        for _, row in df.iterrows():
            n_single = 0
            m_double = 0
            for val in row:
                if val < 10:
                    n_single += 1
                elif val >= 10 and val < 100:
                    m_double += 1
            key = f'{n_single}个一位数 + {m_double}个两位数'
            if key not in result:
                result[key] = 0
            result[key] += 1

        for key, value in result.items():
            probability = value / total_rows
            print(f'{partition}组合 {key} 出现的概率：{probability:.6f}')

    # 选择前区号码和后区号码的位数
    def choose_number(self, front: tuple, back: tuple):
        """
        :param front: （1,4） 代表1个一位数 4个两位数
        :param back: （1,1） 代表1个一位数 1个两位数
        :return:
        """
        res = {}
        front_res, back_res = [], []

        def choose(size: int, arr: list, res_lst: list):
            res_lst.extend(random.sample(arr, size))

        choose(front[0], self.FRONT_SINGLE, front_res)
        choose(front[1], self.FRONT_DOUBLE, front_res)
        choose(back[0], self.BACK_SINGLE, back_res)
        choose(back[1], self.BACK_DOUBLE, back_res)
        front_res.sort()
        back_res.sort()
        res['front'] = front_res
        res['back'] = back_res
        res_str = f"前区：{front_res} 后区：{back_res}"
        logger.info(res_str)
        return res_str, res

    def recommand_number_daletou(self, shot_per_each_group: int):
        res, res_str = [], []
        for _ in range(shot_per_each_group):
            str1, d1 = self.choose_number(front=(1, 4), back=(1, 1))
            str2, d2 = self.choose_number(front=(0, 5), back=(2, 0))
            str3, d3 = self.choose_number(front=(1, 4), back=(2, 0))
            str4, d4 = self.choose_number(front=(2, 3), back=(1, 1))
            res.append(d1)
            res.append(d2)
            res.append(d3)
            res.append(d4)
            res_str.append(str1)
            res_str.append(str2)
            res_str.append(str3)
            res_str.append(str4)

        # res = [self.choose_number(front=(1, 4), back=(1, 1)) for _ in range(shot_per_each_group)
        #        ] + [self.choose_number(front=(0, 5), back=(2, 0)) for _ in range(shot_per_each_group)
        #             ] + [self.choose_number(front=(1, 4), back=(2, 0)) for _ in range(shot_per_each_group)
        #                  ] + [self.choose_number(front=(2, 3), back=(1, 1)) for _ in range(shot_per_each_group)]
        return '\n'.join(res_str), res

    def recommand_number_doublecolor(self, shots: int):
        # 红球号码范围为01～33，蓝球号码范围为01～16。双色球每期从33个红球中开出6个号码，从16个蓝球中开出1个号码作为中奖号码，双色球玩法即是竞猜开奖号码的6个红球号码和1个蓝球号码，顺序不限
        res = []
        for _ in range(shots):
            front = random.sample(self.DC_FRONT, 6)
            back = random.sample(self.DC_BACK, 1)
            front.sort()
            s = f"前区：{front} 后区：{back}"
            res.append(s)

        res_str = '\n'.join(res)
        logger.info(res_str)
        return res_str

    @staticmethod
    def get_history():
        # User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
        # 本次爬取使用的网站为中国体彩网：https://www.lottery.gov.cn/kj/kjlb.html?dlt
        # 多次查看后，所需的开奖数据储存在json文件中，以下为页数和前100的url
        # https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=71
        # url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=100&isVerify=1&pageNo=1&termLimits=100'
        # 'lotteryDrawNum': '21011', 'lotteryDrawResult': '06 09 11 14 21 01 03',
        # 'lotteryDrawStatus': 20, 'lotteryDrawTime': '2021-01-25'
        columns = ['date', 'id', 'front', 'back']
        data = {'date': '', 'id': '', 'front': '', 'back': ''}
        data = collections.OrderedDict()  # 定义为有序字典
        dates = []
        ids = []
        front = []  # 前区
        behind = []  # 后区
        for pageNos in tqdm(range(1, 71)):
            url = 'https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo={}'.format(
                pageNos)
            # 发送请求（获取json文件）
            response = requests.get(url, headers=header)
            content = response.content.decode('utf-8')
            # 使用lxml的etree解析html文件
            html = etree.HTML(content)
            js = json.loads(content)  # json.loads 用于解码 JSON 数据。该函数返回 Python 字段的数据类型。
            numbers = js.get('value')  # 获取js内储存所需要数据的字典
            lists = numbers.get('list')  # 获取字典内的列表，但list内部还有30个字典储存着每一期的开奖数据（第一页开奖数据）
            for data_dict in lists:
                date = data_dict.get('lotteryDrawTime')
                dates.append(date)
                id = data_dict.get('lotteryDrawNum')
                ids.append(id)
                shuju = data_dict.get('lotteryDrawResult')
                number = shuju.split(' ')
                # qianqu = number[:5] #转为列表显示效果较差，有[]、'、,三种符号
                # houqu = number[-2:]
                qianqu = shuju[:14]
                houqu = shuju[-5:]
                front.append(qianqu)
                behind.append(houqu)
            data['date'] = dates
            data['id'] = ids
            data['front'] = front
            data['back'] = behind
        df = pandas.DataFrame(data, columns=columns)
        return df

    # def check_if_won(self, shots):
    #     for shot in shots:
    #         # 模拟号码
    #         front_lst = shot.get('front')
    #         front: set = set(front_lst)
    #         back_lst = shot.get('back')
    #         back: set = set(back_lst)
    #         info_string = lambda x,
    #                              y: f'{x}等奖({y}元) at 期号 {date}\n中奖号码:{cur_front_lst}|{cur_back_lst}\n自选号码:{front_lst}|{back_lst}'
    #     front_intersection_num = len(cur_front.intersection(front))
    #     back_intersection_num = len(cur_back.intersection(back))
    #     if front == cur_front and back == cur_back:
    #         logger.debug(info_string(1, '百万'))
    #         prize_1.append(date)
    #         all_earned += 5000000
    #     elif front == cur_front and back_intersection_num == 1:
    #         logger.debug(info_string(2, '十万'))
    #         prize_2.append(date)
    #         all_earned += 100000
    #     elif front == cur_front and back_intersection_num == 0:
    #         logger.debug(info_string(3, '一万'))
    #         prize_3.append(date)
    #         all_earned += 10000
    #     elif front_intersection_num == 4 and back == cur_back:
    #         logger.debug(info_string(4, '三千'))
    #         prize_4.append(date)
    #         all_earned += 3000
    #     elif front_intersection_num == 4 and back_intersection_num == 1:
    #         logger.debug(info_string(5, '三百'))
    #         prize_5.append(date)
    #         all_earned += 300
    #     elif front_intersection_num == 3 and back == cur_back:
    #         logger.debug(info_string(6, '二百'))
    #         prize_6.append(date)
    #         all_earned += 200
    #     elif front_intersection_num == 4 and back_intersection_num == 0:
    #         logger.debug(info_string(7, '一百'))
    #         prize_7.append(date)
    #         all_earned += 100
    #     elif (front_intersection_num == 3 and back_intersection_num == 1) or (
    #             front_intersection_num == 2 and back_intersection_num == 2):
    #         logger.debug(info_string(8, '十五'))
    #         prize_8.append(date)
    #         all_earned += 15
    #     elif (front_intersection_num == 3 and back_intersection_num == 0
    #     ) or (front_intersection_num == 2 and back_intersection_num == 1
    #     ) or (front_intersection_num == 1 and back_intersection_num == 2
    #     ) or (front_intersection_num == 0 and back_intersection_num == 2
    #     ):
    #         logger.debug(info_string(9, '五'))
    #         prize_9.append(date)
    #         all_earned += 5
    #
    # # 统计概率
    #
    # tmp_str = lambda x: f"{len(x)} 次，概率：{round(len(x) / dates, 5) * 100}%"  # 期号:{x}
    # logger.info(f"""
    #         一等奖(百万元)：{tmp_str(prize_1)}
    #         二等奖(十万元)：{tmp_str(prize_2)}
    #         三等奖(一万元)：{tmp_str(prize_3)}
    #         四等奖(三千元)：{tmp_str(prize_4)}
    #         五等奖(三百元)：{tmp_str(prize_5)}
    #         六等奖(二百元)：{tmp_str(prize_6)}
    #         七等奖(一百元)：{tmp_str(prize_7)}
    #         八等奖(十五元)：{tmp_str(prize_8)}
    #         九等奖(五元)：{tmp_str(prize_9)}
    #
    #         四种组合，每种组合买{shot_per_each_group}注，每次花费{per_spend}元，共花费{all_spend}，中奖{all_earned}，盈亏{all_earned - all_spend}
    #         """)

    def check_prize_of_shot(self, win_shot, my_shot, date):
        res_info = ''

        win_front_lst = win_shot.get('front')
        win_back_lst = win_shot.get('back')
        my_front_lst = my_shot.get('front')
        my_back_lst = my_shot.get('back')

        win_front = set(win_front_lst)
        win_back = set(win_back_lst)
        my_front = set(my_front_lst)
        my_back = set(my_back_lst)
        all_earned = 0
        info_string = lambda x, y: f'{x}等奖({y}元) {date}\n中奖号码:{win_front_lst} | {win_back_lst}\n自选号码:{my_front_lst} | {my_back_lst}'
        front_intersection_num = len(win_front.intersection(my_front))
        back_intersection_num = len(win_back.intersection(my_back))
        if win_front == my_front and win_back == my_back:
            res_info = info_string(1, '百万')
            logger.debug(res_info)
            all_earned += 5000000
        elif win_front == my_front and back_intersection_num == 1:
            res_info = info_string(2, '十万')
            logger.debug(res_info)
            all_earned += 100000
        elif win_front == my_front and back_intersection_num == 0:
            res_info = info_string(3, '一万')
            logger.debug(res_info)
            all_earned += 10000
        elif front_intersection_num == 4 and win_back == my_back:
            res_info = info_string(4, '三千')
            logger.debug(res_info)
            all_earned += 3000
        elif front_intersection_num == 4 and back_intersection_num == 1:
            res_info = info_string(5, '三百')
            logger.debug(res_info)
            all_earned += 300
        elif front_intersection_num == 3 and win_back == my_back:
            res_info = info_string(6, '二百')
            logger.debug(res_info)
            all_earned += 200
        elif front_intersection_num == 4 and back_intersection_num == 0:
            res_info = info_string(7, '一百')
            logger.debug(res_info)
            all_earned += 100
        elif (front_intersection_num == 3 and back_intersection_num == 1) or (
                front_intersection_num == 2 and back_intersection_num == 2):
            res_info = info_string(8, '十五')
            logger.debug(res_info)
            all_earned += 15
        elif front_intersection_num + back_intersection_num == 3:
            res_info = info_string(9, '五')
            logger.debug(res_info)
            all_earned += 5
        return res_info

    def check_latest_win_status(self, ):
        # 爬取最新结果与今日推荐号码比较

        pass


if __name__ == '__main__':
    ins = Lottery(high_probability=False)
    print(ins.recommand_number_doublecolor(2))
    print(ins.get_history())
