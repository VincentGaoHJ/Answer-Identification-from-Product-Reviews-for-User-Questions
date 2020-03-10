# coding=utf-8
"""
@Time   : 2020/3/3  22:10 
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@scishang.com hjgao@std.uestc.edu.cn
@Sketch : 
"""

import os
import csv
import pandas as pd
from utils.data_porter import save_to_csv
from code.vincent_model.config import RAW_DATA_DIR, PROCESSED_DATA_DIR

context_df = pd.DataFrame(columns=["docid", "text"])
context_path = os.path.join(RAW_DATA_DIR, "NCPPolicies_context_20200301.csv")
with open(context_path, "r", encoding="utf-8-sig") as csvFile:
    reader = csv.reader(csvFile)
    k = -1
    for line in reader:
        if k == -1:
            k += 1
            continue
        context_list = line[0].split("\t")
        if len(context_list) == 2:
            context_df.loc[k] = [context_list[0], context_list[1]]
        elif len(context_list) > 2:
            context_df.loc[k] = [context_list[0], "。".join(context_list[1:])]
        else:
            raise Exception
        k += 1

test_df = pd.DataFrame(columns=["id", "question"])
testfile_path = os.path.join(RAW_DATA_DIR, "NCPPolicies_test.csv")
with open(testfile_path, "r", encoding="utf-8-sig") as csvFile:
    reader = csv.reader(csvFile)
    k = -1
    for line in reader:
        if k == -1:
            k += 1
            continue
        context_list = line[0].split("\t")
        if len(context_list) == 2:
            test_df.loc[k] = [context_list[0], context_list[1]]
        else:
            raise Exception
        k += 1

train_df = pd.DataFrame(columns=["id", "docid", "question", "answer"])
train_path = os.path.join(RAW_DATA_DIR, "NCPPolicies_train_20200301.csv")
with open(train_path, "r", encoding="utf-8-sig") as csvFile:
    reader = csv.reader(csvFile)
    k = -1
    for line in reader:
        if k == -1:
            k += 1
            continue
        context_list = line[0].split("\t")
        if len(context_list) == 4:
            train_df.loc[k] = [context_list[0], context_list[1], context_list[2], context_list[3]]
        elif len(context_list) > 4:
            raise Exception
        else:
            continue
        k += 1

save_to_csv(context_df, "context_cleaned.csv", PROCESSED_DATA_DIR, index=True)
save_to_csv(test_df, "test_cleaned.csv", PROCESSED_DATA_DIR, index=True)
save_to_csv(train_df, "train_cleaned.csv", PROCESSED_DATA_DIR, index=True)
