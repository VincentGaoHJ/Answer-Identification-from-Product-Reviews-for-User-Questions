#!/usr/bin/env python
# coding: utf-8

import json
import sys
import pandas as pd


def load_context():
    docid2context = {}
    f = True
    for line in open('data/NCPPolicies_context_20200301.csv'):
        if f:
            f = False
            continue
        r = line.strip().split('\t')
        docid2context[r[0]] = r[1]
    return docid2context


def convert_trainset(filename):
    docid2context = load_context()
    first_line = True
    fout = open('data/train.jsonl', 'w')
    for line in open(filename):
        if first_line:
            first_line = False
            continue
        r = line.strip().split('\t')
        rv = {'qid': r[0], 'context': docid2context[r[1]], 'query': r[2], 'answer': {'text': r[3]}}
        fout.write(json.dumps(rv, ensure_ascii=False) + '\n')


def load_retrieval_docids():
    q2docid = {}
    for line in open('data/query_docids_v1.csv'):
        r = line.strip().split('\t')
        q2docid[r[0]] = r[1].split(',')[0]
    return q2docid


def convert_testset(filename):
    """Convert test set to json format."""
    q2docid = load_retrieval_docids()
    docid2context = load_context()

    first_line = True
    fout = open('data/test.jsonl', 'w')
    for line in open(filename):
        if first_line:
            first_line = False
            continue
        r = line.strip().split('\t')
        if r[1] not in q2docid:
            print(f'cannot find retrieval results: {r[1]}')
        rv = {'qid': r[0], 'context': docid2context[q2docid.get(r[1],'c129c1bc387c312284c3ef61b551c432')], 'query': r[1], 'answer': {'text': ''}}
        fout.write(json.dumps(rv, ensure_ascii=False) + '\n')

def stat_length(filename):
    df = pd.read_csv(filename, sep='\t', error_bad_lines=False)
    df['context_length'] = df['text'].apply(len)
    print(f"context length: {df['context_length'].mean()}")

if  __name__ == '__main__':
    #stat_length('data/NCPPolicies_context_20200301.csv')
    #convert_trainset('data/NCPPolicies_train_20200301.csv')
    convert_testset('data/NCPPolicies_test.csv')
