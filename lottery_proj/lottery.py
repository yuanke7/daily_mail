import random

from loguru import logger
from tqdm import tqdm


class Lottery:
    FRONT_SINGLE = [i for i in range(1, 10)]
    FRONT_DOUBLE = [i for i in range(10, 36)]
    BACK_SINGLE = [i for i in range(1, 10)]
    BACK_DOUBLE = [i for i in range(10, 13)]
    FRONT_COL = ['front_1', 'front_2', 'front_3', 'front_4', 'front_5']
    BACK_COL = ['back_1', 'back_2']

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
        return res_str

    def recommand_number(self, shot_per_each_group: int):
        res = [self.choose_number(front=(1, 4), back=(1, 1)) for _ in range(shot_per_each_group)
               ] + [self.choose_number(front=(0, 5), back=(2, 0)) for _ in range(shot_per_each_group)
                    ] + [self.choose_number(front=(1, 4), back=(2, 0)) for _ in range(shot_per_each_group)
                         ] + [self.choose_number(front=(2, 3), back=(1, 1)) for _ in range(shot_per_each_group)]
        return '\n'.join(res)

if __name__ == '__main__':
    ins = Lottery(high_probability=False)
    print(ins.recommand_number(1))
