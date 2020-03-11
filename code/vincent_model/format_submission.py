# coding=utf-8
"""
@Time   : 2020/3/11  10:14 
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@scishang.com hjgao@std.uestc.edu.cn
@Sketch : 
"""

import os
import json
from utils.config import DATA_DIR, RESULT_DIR, RAW_DATA_DIR

from code.baseline_model.format_submission import format_submission

if __name__ == '__main__':
    # model_name = "bert-base-chinese"
    model_name = "chinese_wwm_ext_pytorch"
    checkpoint = "checkpoint-12000"
    format_submission(model_name=model_name,
                      checkpoint=checkpoint,
                      data_dir=DATA_DIR,
                      test_file_dir=RAW_DATA_DIR,
                      result_dir=RESULT_DIR)
