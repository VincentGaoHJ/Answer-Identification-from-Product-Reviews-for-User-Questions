# coding=utf-8
"""
@Time   : 2020/3/3  22:23 
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@scishang.com hjgao@std.uestc.edu.cn
@Sketch : 
"""

import os
import pandas as pd


def read_from_csv(filename, dir_path='./', **kwargs):
    file_path = os.path.join(dir_path, filename)
    df = pd.read_csv(file_path, **kwargs)
    return df


def save_to_csv(df, filename, dir_path='./', index=False,
                encoding='utf-8-sig', **kwargs):
    file_path = os.path.join(dir_path, filename)
    kwargs.update({'index': index, 'encoding': encoding})
    df.to_csv(file_path, **kwargs)
