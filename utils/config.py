# coding=utf-8
"""
@Time   : 2020/3/3  22:20 
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@scishang.com hjgao@std.uestc.edu.cn
@Sketch : 
"""

import os

# 日志等级
LOG_LEVEL = 'DEBUG'

# 路径
__proj_dir = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(__proj_dir, 'data')

RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw_data')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed_data')
RESULT_DIR = os.path.join(DATA_DIR, 'result')
MODEL_DIR = os.path.join(DATA_DIR, 'model')

if __name__ == '__main__':
    pass
