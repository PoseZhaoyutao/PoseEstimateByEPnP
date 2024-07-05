# -*- coding: utf-8 -*-
# @Author  : Zhao Yutao
# @Time    : 2024/7/1 12:29
# @Function: 测试redis服务端发送图像
# @mails: zhaoyutao22@mails.ucas.ac.cn
import math
import numpy as np


def precision(data_list_gt_filepath, data_list_es_filepath):
    data_list_gt_file = open(data_list_gt_filepath, "r")
    data_list_es_file = open(data_list_es_filepath, "r")
    data_list_gt = []
    data_list_es = []
    for line in data_list_es_file.readlines():
        dataline = line.split(" ")[1:9]
        data_list_es.append(dataline)
    for line in data_list_gt_file.readlines():
        dataline = line.split(" ")[1:9]
        data_list_gt.append(dataline)

    score = []
    # 计算位置误差
    for i in range(len(data_list_gt)):
        err_p = math.sqrt((float(data_list_gt[i][0]) - float(data_list_es[i][0])) ** 2 +
                          (float(data_list_gt[i][1]) - float(data_list_es[i][1])) ** 2 +
                          (float(data_list_gt[i][2]) - float(data_list_es[i][2])) ** 2) / math.sqrt(
            float(data_list_gt[i][0]) ** 2 + float(data_list_gt[i][1]) ** 2 + float(data_list_gt[i][2]) ** 2)
        if err_p < 0.002173:
            score_p = 0
        else:
            score_p = err_p
        name_q = np.array(list(map(float(data_list_gt[i][4:8]))))
        q_opt = np.array(list(map(float(data_list_es[i][4:8]))))
        qq_cos = name_q @ q_opt.T / (np.linalg.norm(name_q) * np.linalg.norm(q_opt))
        if qq_cos > 1:
            qq_cos = 2 - qq_cos

        err_o = 2 * math.acos(qq_cos)
        if err_o < 0.169:
            score_o = 0
        else:
            score_o = err_o
        score.append(score_o + score_p)

    score_ = np.sum(score) / len(score)
    print(score_)
    return score_


if __name__ == '__main__':
    precision(r"C:\Users\zhaoy\Desktop\AI4Space\train\train\RT590.txt","RT590_estimate.txt")