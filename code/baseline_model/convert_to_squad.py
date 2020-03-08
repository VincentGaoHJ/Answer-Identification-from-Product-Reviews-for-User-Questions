#!/usr/bin/env python
# coding: utf-8

import json
from code.vincent_model.config import PROCESSED_DATA_DIR


def to_english(string):
    return ' '.join(list(string))


def convert_to_squad(filepath, output_file):
    """Convert to squad-like dataset."""
    rv = {'data': []}
    for line in open(filepath, encoding="utf-8-sig"):
        datum = json.loads(line)
        context = to_english(datum['context'])
        query = to_english(datum['query'])
        orig_answer = datum['answer']['text']
        if 'span' not in datum['answer']:
            print('no span')
            continue
        span = datum['answer']['span']
        span = [span[0] * 2, span[1] * 2]
        answer = context[span[0]:span[1] + 1]
        ex = {'title': 'fake title',
              'paragraphs': [{
                  'context': context,
                  "qas": [{
                      "answers": [{
                          "answer_start": span[0],
                          "text": answer}],
                      'question': query,
                      'id': datum['qid']
                  }]
              }]}
        rv['data'].append(ex)
    json.dump(rv, open(output_file, 'w', encoding="utf-8-sig"), indent=2, ensure_ascii=False)


def convert_test_to_squad(filepath, output_file):
    rv = {'data': []}
    for line in open(filepath, encoding="utf-8-sig"):
        datum = json.loads(line)
        context = to_english(datum['context'])
        query = to_english(datum['query'])
        ex = {'title': 'fake title',
              'paragraphs': [{
                  'context': context,
                  "qas": [{
                      "answers": [{
                          "answer_start": 0,
                          "text": ''}],
                      'question': query,
                      'id': datum['qid']
                  }]
              }]}
        rv['data'].append(ex)
    json.dump(rv, open(output_file, 'w', encoding="utf-8-sig"), indent=2, ensure_ascii=False)


if __name__ == '__main__':
    # Input files
    train_answer_file = f'{PROCESSED_DATA_DIR}/train_answer.jsonl'
    test_file = f'{PROCESSED_DATA_DIR}/test.jsonl'
    # Output files
    train_squad_file = f'{PROCESSED_DATA_DIR}/train_squad.json'
    test_squad_file = f'{PROCESSED_DATA_DIR}/test_squad.json'

    convert_to_squad(
        filepath=train_answer_file,
        output_file=train_squad_file)
    convert_test_to_squad(
        filepath=test_file,
        output_file=test_squad_file)
