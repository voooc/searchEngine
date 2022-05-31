# -!- coding: utf-8 -!-
import os
from collections import Counter
import pandas as pd


def open_file():
    """
    打开文件并建立每篇文章所对应的字典形式
    :return: {'001': ['computer', 'data', 'structures']}
    """""
    docu_set = {}
    path_list = os.listdir('../data/spilt')
    path_list.sort(key=lambda x: int(x[2:-4]))
    for filename in path_list:
        fr = open('./spilt\\' + filename, 'r', encoding='utf-8')
        line = fr.read()
        line = line.rstrip('\n').split(' ')
        for i in range(1, len(line)):
            docu_set.setdefault(line[0], []).append(line[i])
    return docu_set


def all_word(docu_set):
    """
    建立所有单词的集合
    :param docu_set:每篇文章对应的字典形式
    :return: {'structures', 'design', 'computer'}
    """""
    all_words = []
    for i in docu_set.values():
        all_words.extend(i)
    nums = dict(Counter(all_words))
    all_words = set(all_words)
    print(len(all_words))
    return all_words, nums


def invert_index():
    """
    倒排索引，建立每个单词所在的文件
    :return: 写入文件{'structures': ['001', '002', '003']}
    """""
    s = 0
    docu_set = open_file()
    all_words, nums = all_word(docu_set)
    # df = pd.DataFrame(columns=['Num', 'WorldId', 'NHits', 'DocHits'])
    for b in all_words:
        print(s)
        temp = {}
        for j in docu_set.keys():
            field = docu_set[j]
            if b in field:
                temp[int(j)] = Counter(field)[b]
        # df = df.append(
        #     pd.DataFrame({'Num': [s], 'WorldId': [b], 'NHits': [nums[b]], 'DocHits': [temp]}), ignore_index=True)
        # s += 1
        # df.to_csv("测试倒序.csv", index=False)


if __name__ == '__main__':
    invert_index()
