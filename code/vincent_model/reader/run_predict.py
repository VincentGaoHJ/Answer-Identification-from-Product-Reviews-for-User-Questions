# coding=utf-8
"""
@Time   : 2020/3/11  1:27 
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@scishang.com hjgao@std.uestc.edu.cn
@Sketch : 
"""

import os
import sys
from utils.config import DATA_DIR, PROCESSED_DATA_DIR
from code.baseline_model.run_squad import main

if __name__ == "__main__":
    model_name = "chinese_wwm_ext_pytorch"
    model_path = os.path.join(DATA_DIR, model_name)
    checkpoint = "checkpoint-12000"
    # 这个地方不能用 os.path.join 因为源代码写的太烂，不支持跨平台
    # 原因是 list(filter(None, args.model_name_or_path.split("/"))).pop()
    # 而 os.sep 中 windows 的路径分隔符会被转译成 \\
    checkpoint_path = f"{model_path}/{checkpoint}"
    sys.argv[1:] = ["--model_type=bert",
                    "--data_dir={}".format(PROCESSED_DATA_DIR),
                    "--model_name_or_path={}".format(checkpoint_path),
                    "--do_eval",
                    "--predict_file=test_squad.json",
                    "--output_dir={}".format(checkpoint_path)]

    main()
