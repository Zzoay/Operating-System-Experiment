#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yaozz
# Date: 2019-11-29
# Remark: 操作系统实验1-短进程优先调度


class PCB:
    def __init__(self):
        self.name = ""
        self.arr = 0   # 到达时间
        self.ser = 0    # 服务时间
        self.finish = 0     # 完成时间
        self.round = 0  # 周转时间
        self.weighted = 0   # 带权周转时间


    def prt_pcb(self):
        print("进程名|到达时间|服务时间|完成时间|周转时间|带权周转时间")
        print("{:^6}|{:^6}|{:^6}|{:^6}|{:^6}|{:^6}".format(self.name, self.arr, self.ser, self.finish, self.round, self.weighted))


def execute(p, tmp_finish=0):
    p.finish = tmp_finish + p.ser
    p.round = p.finish - p.arr
    p.weighted = p.round / p.ser
    tmp_finish = p.finish
    tmp_p = p
    return tmp_finish, tmp_p


def spf(tmp_pcb_lst, tmp_finish):
    # 通过两次的稳定排序，将先到达的，或同时到达而服务时间最短的，放在列表的首位
    idx_arr = sorted(range(len(tmp_pcb_lst)), key=lambda k: tmp_pcb_lst[k].ser)
    tmp_pcb_lst = [tmp_pcb_lst[i] for i in idx_arr]

    idx_arr = sorted(range(len(tmp_pcb_lst)), key=lambda k: tmp_pcb_lst[k].arr)
    tmp_pcb_lst = [tmp_pcb_lst[i] for i in idx_arr]

    # 上次任务完成的时间，0表示初始状态
    if tmp_finish == 0:
        tmp_pcb_lst[0].finish = tmp_pcb_lst[0].arr + tmp_pcb_lst[0].ser
        tmp_finish = int(tmp_pcb_lst[0].finish)
    else:
        tmp_pcb_lst[0].finish = tmp_finish + tmp_pcb_lst[0].ser

    tmp_pcb_lst[0].round = tmp_pcb_lst[0].finish - tmp_pcb_lst[0].arr
    tmp_pcb_lst[0].weighted = tmp_pcb_lst[0].round / tmp_pcb_lst[0].ser

    tmp_pcb_lst.pop(0)

    p_que = []
    # 若在第一个任务完成前，其他任务已到达，则将到达的任务放入队列，同时移除列表中的这些任务
    for i, p in enumerate(tmp_pcb_lst[:]):
        if int(p.arr) <= int(tmp_finish):
            p_que.append(p)
            tmp_pcb_lst.remove(p)

    # 在就绪队列中，执行任务，直到队列中的任务全部完成
    while len(p_que) > 0:
        idx_arr = sorted(range(len(p_que)), key=lambda k: p_que[k].ser)
        p_que = [p_que[i] for i in idx_arr]

        tmp_finish, _ = execute(p_que[0], tmp_finish)

        # 任务完成后，若进程列表中已有到达的任务，则将其加入队列
        for p in tmp_pcb_lst:
            if p.arr <= tmp_finish:
                p_que.append(p)
                tmp_pcb_lst.remove(p)

        p_que.pop(0)    # 弹出第一个

    if len(tmp_pcb_lst) == 0:
        return

    return spf(tmp_pcb_lst, tmp_finish)


if __name__ == '__main__':
    # 测试用例
    name_lst = ["A","B","C","D","E"]
    num = len(name_lst)
    arr_lst = [0,1,2,3,4]
    ser_lst = [4,3,5,2,4]
    pcb_lst = []
    for i in range(num):
        pcb = PCB()
        pcb.name = name_lst[i]
        pcb.arr = arr_lst[i]
        pcb.ser = ser_lst[i]
        pcb_lst.append(pcb)

    tmp_finish = 0
    spf(pcb_lst, tmp_finish)
    for p in pcb_lst:
        p.prt_pcb()
