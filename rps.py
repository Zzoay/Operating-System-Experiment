#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yaozz
# Date: 2019-11-29
# Remark: 请求分页存储管理

import random

# 生成指令序列
def build_order_seq(nums):
    seq = []
    cnt = nums
    while True:
        m = random.randint(0, nums)
        seq.append(m+1)
        cnt -=1
        if cnt == 0: break

        m1 = random.randint(0, m)
        seq.append(m1)
        cnt -=1
        if cnt == 0: break

        seq.append(m1+1)
        cnt -=1
        if cnt == 0: break

        m2 = random.randint(m1+2, nums)
        seq.append(m2)
        cnt -=1
        if cnt == 0: break

        seq.append(m2+1)
        cnt -=1
        if cnt == 0: break

    return seq


# 构建页地址流
def build_page_flow(seq):
    flow = []
    for i,ord in enumerate(seq):
        page = int(ord/10)
        flow.append(page)
    return flow


# 先进先出
def fifo(flow, blocks, block_num):
    ms_cnt = 0
    q_cnt = 0
    for i,op in enumerate(flow):
        # print(blocks)
        if len(blocks) < block_num and op not in blocks:
            blocks.append(op)
            ms_cnt += 1
            continue
        if op not in blocks:
            blocks[q_cnt] = op
            q_cnt += 1
            if q_cnt >= block_num:
                q_cnt = 0
            ms_cnt += 1

    return ms_cnt


# 最佳置换
def opt(flow, blocks, block_num):
    ms_cnt = 0
    for i,op in enumerate(flow):
        # print(blocks)
        if len(blocks) < block_num and op not in blocks:
            blocks.append(op)
            ms_cnt += 1
            continue
        if op not in blocks:
            next_t = []

            for item in blocks:
                found = 0
                for idx,opx in enumerate(flow[i:]):
                    if item == opx:
                        next_t.append(idx)
                        found = 1
                        break
                if found == 0:
                    next_t.append(len(flow))

            idx_arr = sorted(range(len(next_t)), key=lambda k: next_t[k], reverse=True)
            blocks[idx_arr[0]] = op

            ms_cnt += 1

    return ms_cnt


# 最近最近未使用
def lru(flow, blocks, block_num):
    # print(flow)
    ms_cnt = 0
    pre_t = [] # 标记块中页面上次访问的时间t的列表
    for i,op in enumerate(flow):
        # print(op)
        # print(blocks)
        if len(blocks) < block_num and op not in blocks:
            blocks.append(op)
            pre_t.append(i)
            ms_cnt += 1
            continue
        if op not in blocks:
            # print(pre_t)
            # 对上次时间进行排序，返回下标
            idx_arr = sorted(range(len(pre_t)), key=lambda k: pre_t[k])

            # print(idx_arr)
            # 将最近最久未使用的替换
            blocks[idx_arr[0]] = op
            pre_t[idx_arr[0]] = i
            ms_cnt += 1
        else:
            for idx,item in enumerate(blocks):
                if item==op:
                    pre_t[idx] = i

    return ms_cnt


if __name__ == '__main__':
    n = 320 # 指令数量
    block_num = 4   # 块的大小

    seq = build_order_seq(n)
    flow = build_page_flow(seq)

    print("指令序列： {}".format(seq))
    print("页地址流： {}".format(flow))
    # 书上的例子
    # block_num = 3
    # flow = [7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1]

    print("---------各个页面置换算法的缺页率---------")

    blocks = []
    ms_cnt = fifo(flow, blocks, block_num)
    ms_rate = ms_cnt/len(flow)
    print("FIFO: {}".format(ms_rate))

    blocks = []
    ms_cnt = opt(flow, blocks, block_num)
    ms_rate = ms_cnt/len(flow)
    print("OPT: {}".format(ms_rate))

    blocks = []
    ms_cnt = lru(flow, blocks, block_num)
    ms_rate = ms_cnt/len(flow)
    print("LRU: {}".format(ms_rate))