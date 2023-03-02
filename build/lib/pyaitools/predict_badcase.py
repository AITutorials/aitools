# coding:utf-8
# @Time    : 2022/3/26 9:24 上午
# @Auther  : liangxinxin
# Description：对样本进行预测，将得到的结果与真实结果进行对比,将预测错误的样本输出到文件
import requests
import pandas as pd
import os


def predict_sentence(url, data):
    """
    :param url: 模型服务url
    :param data: 模型服务要求的数据
    :return:
    """
    res = requests.post(url, json=data, timeout=5000)
    if res.status_code == 200:
        return eval(res.text)[0]
    else:
        return res.status_code


def predicts(datas, labels, url):
    """
    :param datas: 模型服务要求的数据集合
    :param labels: 真实标签
    :param url: 模型服务url
    :return: 预测错误的标签：pred_label，true_label
    """
    results = []
    for index, data in enumerate(datas):
        pred_label = predict_sentence(url, data)
        true_label = labels[index]
        if pred_label != true_label:
            results.append([pred_label, true_label])
    return results
