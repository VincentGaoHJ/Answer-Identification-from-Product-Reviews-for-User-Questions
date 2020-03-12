# coding=utf-8
"""
@Time   : 2020/3/11  1:24 
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
    sys.argv[1:] = ["--model_type=bert",
                    "--data_dir={}".format(PROCESSED_DATA_DIR),
                    "--model_name_or_path={}".format(model_path),
                    "--do_train",
                    "--do_lower_case",
                    "--train_file=train_squad.json",
                    "--learning_rate=3e-5",
                    "--num_train_epochs=2.0",
                    "--max_seq_length=384",
                    "--doc_stride=128",
                    "--output_dir={}".format(model_path),
                    "--overwrite_output_dir"]

    main()
