# coding: utf-8
# 从训练集中选取数据使用BERT进行相关度二分类训练
# https://cloud.tencent.com/developer/article/1042161

import re
import os
import json
import random
import pandas as pd

from tqdm import tqdm
from utils.config import RAW_DATA_DIR, RETRIEVER_DATA_DIR
from utils.normalize import filter_tags
from utils.data_porter import read_from_csv


def is_subset(a, b):
    """Determine if it is a subset"""
    a = "".join(re.findall(u'[\u4e00-\u9fff]+', a))
    b = "".join(re.findall(u'[\u4e00-\u9fff]+', b))
    if set(b).issubset(a) or set(a).issubset(b):
        return True
    else:
        return False


def gene_pos_neg(question, answer, context):
    """Generate positive and negative examples"""
    context_sentence_list = context.split("。")
    sub_dataset = []
    positive_number = 0
    if "。" in answer:
        answer_list = context.split("。")
    else:
        answer_list = [answer]
    for sentence in context_sentence_list:
        for answer in answer_list:
            if is_subset(sentence, answer):
                sub_dataset.append([1, question, sentence])
                positive_number += 1
                break
            else:
                sub_dataset.append([0, question, sentence])
    if positive_number != 0:
        return sub_dataset
    else:
        sub_dataset = regene_pos_neg(sub_dataset, answer)
        return sub_dataset


def regene_pos_neg(sub_dataset, answer):
    print("=" * 20)
    print("question: ", sub_dataset[0][1])
    print("answer: ", answer)
    for sub_sample in sub_dataset:
        print("paragraph: ", sub_sample[2])
    return sub_dataset


def prepare_dataset(train_file, context_file):
    """Prepare the sentence pair task training dataset for bert"""
    train_df = read_from_csv(train_file, index_col=[0])
    context_df = read_from_csv(context_file, index_col=[0])
    dataset = pd.merge(left=train_df, right=context_df, on="docid")
    new_dataset = []
    for index, row in dataset.iterrows():
        question = row["question"]
        answer = row["answer"]
        context = row["text"]
        sub_dataset = gene_pos_neg(question, answer, context)

        new_dataset.extend(sub_dataset)
    return new_dataset


def write_tsv(output_path, dataset):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, data in enumerate(dataset):
            write_line = '\t'.join([str(data[0]), str(i), str(i), filter_tags(data[1]),
                                    filter_tags(data[2])])
            f.write(write_line + '\n')


def main():
    print('Start loading preprocessed train json file.')
    context_file = os.path.join(RAW_DATA_DIR, "context_cleaned.csv")
    train_file = os.path.join(RAW_DATA_DIR, "train_cleaned.csv")
    train_dataset = prepare_dataset(train_file, context_file)
    random.shuffle(train_dataset)
    output_file = os.path.join(RETRIEVER_DATA_DIR, "train.tsv")
    write_tsv(output_file, train_dataset)
    print('Done with preparing training dataset.')


if __name__ == "__main__":
    main()
