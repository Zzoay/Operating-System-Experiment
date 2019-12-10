#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yaozz
# Date: 2019-12-1
# Remark: 银行家算法

import numpy as np
import random


def init(p_lst, resource):
    # 随机生成各个进程所需资源和已占资源
    max = []
    allocation = []
    for p in p_lst:
        tmp = []
        for r in resource:
            m = random.randint(0, r)
            m = random.randint(0, m)     # 双随机，防止生成的资源需求太大
            tmp.append(m)
        max.append(tmp)

    for i,m in enumerate(max):
        tmp = []
        for j,m_j in enumerate(m):
            a = random.randint(0, m_j)
            t = resource[j] - a
            if t>=0:
                resource[j] = t
                tmp.append(a)
                # tmp.append(0)
            else:
                tmp.append(0)
        allocation.append(tmp)

    print("============随机初始化============")
    return np.array(max), np.array(allocation), np.array(resource)


def check(res, req):    # res: 资源数序列； req：请求数序列
    if len(res) != len(req):
        print("序列长度不等")
        return
    for i,j in zip(res, req):
        if i < j:
            return False
    return True


def safe(available):
    finish = [False for _ in range(len(need))]
    work = available
    safe_lst = []
    i = 0
    while True:
        if finish[i] or check(work, need[i]) is False:
            i += 1
            if i == len(need):
                break
            continue
        # print(work)
        work = work + allocation[i]
        finish[i] = True
        safe_lst.append(i)
        i = 0

    for f in finish:
        if f == False:
            print("------当前分配不安全-----")
            return False, None
    safe_lst = ["p{}".format(_) for _ in safe_lst]
    print("存在安全序列：{}".format(safe_lst))
    return True, safe_lst


def banker_algorithm(request, available):
    request_i, i = request[0],request[1]
    if check(need[i], request_i) is False:
        print('申请资源超过所需资源：申请：{}，所需{}'.format(request_i, need[i]))
        return False, available, allocation, need
    if check(available, request_i) is False:
        print('申请资源超过现有资源：申请：{}，现有{}'.format(available, request_i))
        return False, available, allocation, need
    available = available - request_i
    allocation[i] = allocation[i] + request_i
    need[i] = need[i] - request_i

    saf, safe_lst = safe(available)  # 检测此分配是否安全，若不安全，则取消分配
    if saf is False:
        available = available + request_i
        allocation[i] = allocation[i] - request_i
        need[i] = need[i] + request_i
        return False, available, allocation, need
    prt_table(safe_lst, allocation, need, available)
    return True, available, allocation, need


def prt_table(p_lst, allocation, need, available):
    print("-------------------------------")
    print("\t\tMax\t\tAllocation\t\tNeed\t\tAvailable")
    for i,m in enumerate(max):
        if i == 0:
            print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(p_lst[i], m, allocation[i], need[i], available))
        else:
            print("{}\t\t{}\t\t{}\t\t{}".format(p_lst[i], m, allocation[i], need[i]))
    print("-------------------------------")
    return


if __name__ == '__main__':
    p_lst = ['p0', 'p1', 'p2', 'p3', 'p4']  # 进程列表
    available = [10, 5, 7]  # 各个资源数

    '''
            max   |  allocation |  available  | need
         最大需求矩阵 | 分配矩阵 | 资源向量  | 需求矩阵
    '''
    max, allocation, available = init(p_lst, available)
    need = max - allocation

    # 打印初始状态的资源分配表，并检查此时是否安全
    prt_table(p_lst, allocation, need, available)
    if safe(available)[0]:
        print("\n============发送请求向量============")
        request = [np.array([0,0,1]), 2] # 请求向量
        print("请求向量：{}".format(request))
        saf, available, allocation, need = banker_algorithm(request, available)
