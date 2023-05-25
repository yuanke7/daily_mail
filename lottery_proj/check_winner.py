import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 注意 在bat模式下启动时 相对路径导包必须在此行之下

from lottery_proj.run import check

if __name__ == '__main__':
    check()