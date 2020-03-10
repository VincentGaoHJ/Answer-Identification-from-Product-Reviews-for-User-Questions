#!/usr/bin/env python
# coding: utf-8

import os
import json
from utils.config import DATA_DIR, RESULT_DIR, RAW_DATA_DIR


def load_test(test_file_dir):
    qid2query = {}
    f = True
    file_path = os.path.join(test_file_dir, "NCPPolicies_test.csv")
    for line in open(file_path, encoding="utf-8-sig"):
        if f:
            f = False
            continue
        r = line.strip().split('\t')
        qid2query[r[0]] = r[1]
    return qid2query


def format_submission(model_name, checkpoint, data_dir, test_file_dir, result_dir):
    """

    :param model_name:
    :param checkpoint:
    :param data_dir:
    :param result_dir:
    :return:
    """

    prediction_file = os.path.join(data_dir, model_name, checkpoint, "predictions_.json")
    output_file = os.path.join(result_dir, f"{model_name}_{checkpoint}_submit.csv")

    qid2query = load_test(test_file_dir)
    res = json.load(open(prediction_file))
    fout = open(output_file, 'w', encoding="utf-8-sig")
    fout.write(f'qid\tdocid\tanswer\n')
    for k, v in res.items():
        v = v.replace(' ', '')
        fout.write(f'{k}\t123123\t{v}\n')
    for qid in (qid2query.keys() - res.keys()):
        fout.write(f'{qid}\t12asd\tfake answer\n')


if __name__ == '__main__':
    model_name = "bert-base-chinese"
    checkpoint = "checkpoint-12000"
    format_submission(model_name=model_name,
                      checkpoint=checkpoint,
                      data_dir=DATA_DIR,
                      test_file_dir=RAW_DATA_DIR,
                      result_dir=RESULT_DIR)
