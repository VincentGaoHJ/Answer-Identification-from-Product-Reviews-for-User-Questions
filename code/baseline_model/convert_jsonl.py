#!/usr/bin/env python
# coding: utf-8

import sys
import json
import pandas as pd
from code.vincent_model.config import RAW_DATA_DIR, PROCESSED_DATA_DIR


def load_context(context_file):
    docid2context = {}
    f = True
    for line in open(context_file, encoding="utf-8-sig"):
        if f:
            f = False
            continue
        r = line.strip().split('\t')
        docid2context[r[0]] = r[1]
    return docid2context


def convert_trainset(filename, context_file, output_path):
    docid2context = load_context(context_file)
    first_line = True
    fout = open(f'{output_path}/train.jsonl', 'w', encoding="utf-8-sig")
    for line in open(filename, encoding="utf-8-sig"):
        if first_line:
            first_line = False
            continue
        r = line.strip().split('\t')
        rv = {'qid': r[0], 'context': docid2context[r[1]], 'query': r[2], 'answer': {'text': r[3]}}
        fout.write(json.dumps(rv, ensure_ascii=False) + '\n')


def load_retrieval_docids(retrival_file):
    q2docid = {}
    for line in open(retrival_file, encoding="utf-8-sig"):
        r = line.strip().split('\t')
        q2docid[r[0]] = r[1].split(',')[0]
    return q2docid


def convert_testset(filename, context_file, retrival_file, output_path):
    """Convert test set to json format."""
    q2docid = load_retrieval_docids(retrival_file)
    docid2context = load_context(context_file)

    first_line = True
    fout = open(f'{output_path}/test.jsonl', 'w', encoding="utf-8-sig")
    for line in open(filename, encoding="utf-8-sig"):
        if first_line:
            first_line = False
            continue
        r = line.strip().split('\t')
        if r[1] not in q2docid:
            print(f'cannot find retrieval results: {r[1]}')
        rv = {'qid': r[0], 'context': docid2context[q2docid.get(r[1], 'c129c1bc387c312284c3ef61b551c432')],
              'query': r[1], 'answer': {'text': ''}}
        fout.write(json.dumps(rv, ensure_ascii=False) + '\n')


def stat_length(filename):
    df = pd.read_csv(filename, sep='\t', error_bad_lines=False)
    df['context_length'] = df['text'].apply(len)
    print(f"context length: {df['context_length'].mean()}")


if __name__ == '__main__':
    context_file = f'{RAW_DATA_DIR}/NCPPolicies_context_20200301.csv'
    train_file = f'{RAW_DATA_DIR}/NCPPolicies_train_20200301.csv'
    test_file = f'{RAW_DATA_DIR}/NCPPolicies_test.csv'
    retrival_file = f'{PROCESSED_DATA_DIR}/query_docids_v1.csv'

    stat_length(context_file)
    convert_trainset(
        train_file, context_file,
        output_path=PROCESSED_DATA_DIR)
    convert_testset(
        test_file, context_file, retrival_file,
        output_path=PROCESSED_DATA_DIR)
