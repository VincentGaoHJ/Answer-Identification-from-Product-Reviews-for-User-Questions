# coding: utf-8
# 从训练集中选取数据使用BERT进行相关度二分类训练
# https://cloud.tencent.com/developer/article/1042161

import os
import json
import jieba
import random
import pandas as pd

from tqdm import tqdm
from utils.config import RAW_DATA_DIR
from utils.normalize import filter_tags
from utils.data_porter import read_from_csv
from nltk.translate.bleu_score import sentence_bleu


def gene_pos_neg(answer, context):
    """Generate positive and negative examples"""
    answer_seg = list(jieba.cut(answer))
    context_sentence_list = context.split("。")
    for sentence in context_sentence_list:
        sentence_seg = list(jieba.cut(sentence))
        print(sentence_seg)
        print(answer_seg)
        score = sentence_bleu(sentence_seg, answer_seg)
        print(score, answer)
        print(sentence)
    print(context)
    raise Exception



def prepare_dataset(train_file, context_file):
    """Prepare the sentence pair task training dataset for bert"""
    train_df = read_from_csv(train_file, index_col=[0])
    context_df = read_from_csv(context_file, index_col=[0])
    dataset = pd.merge(left=train_df, right=context_df, on="docid")
    print(dataset)
    print(dataset.columns.values)
    for index, row in dataset.iterrows():
        print(index, row)
        question = row["question"]
        answer = row["answer"]
        context = row["text"]
        gene_pos_neg(answer, context)



    raise Exception

    with open(filename, 'r', encoding='utf-8') as f:
        datasets = []
        for lidx, line in enumerate(tqdm(f)):
            sample = json.loads(line.strip())
            qid = sample['question_id']
            question = sample['question']
            if not len(sample['match_scores']):
                continue
            if sample['match_scores'][0] < 0.7:
                continue
            if not len(sample['answer_docs']):
                continue
            if sample['answer_docs'][0] >= len(sample['documents']):
                continue
            doc = sample['documents'][int(sample['answer_docs'][0])]
            related_para = doc['paragraphs'][int(doc['most_related_para'])].replace('\n', '')
            datasets.append([1, question, related_para])
            for i in range(len(doc['paragraphs'])):
                if i != int(doc['most_related_para']):
                    irrelated_para = doc['paragraphs'][i].replace('\n', '')
                    datasets.append([0, question, irrelated_para])
    return datasets


def write_tsv(output_path, datasets):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, data in enumerate(datasets):
            write_line = '\t'.join([str(data[0]), str(i), str(i), filter_tags(data[1]),
                                    filter_tags(data[2])])
            f.write(write_line + '\n')


def main():
    print('Start loading preprocessed train json file.')
    context_file = os.path.join(RAW_DATA_DIR, "context_cleaned.csv")
    train_file = os.path.join(RAW_DATA_DIR, "train_cleaned.csv")
    train_datasets = prepare_dataset(train_file, context_file)
    random.shuffle(train_datasets)
    write_tsv('./retriever_data/train.tsv', train_datasets)
    print('Done with preparing training dataset.')


if __name__ == "__main__":
    main()
