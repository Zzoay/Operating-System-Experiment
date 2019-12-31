#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yaozz
# Date: 2019-12-27
# Remark: Multiprogrammed Batch Processing System 多道批处理系统


import spf
import dpa

class PCB(spf.PCB): # 继承
    def __init__(self):
        super().__init__()
        self.memory = 0
        self.tape_drive = 0
        self.arr_memory = 0

    # 方法重写
    def prt_pcb(self):
        print("作业名|到达时间|进入内存时间|服务时间|完成时间|周转时间|带权周转时间")
        print("{:^6}|{:^8}|{:^10}|{:^8}|{:^8}|{:^8}|{:.2f}".format(self.name, self.arr, self.arr_memory, self.ser, self.finish, self.round, self.weighted))


class Resource:
    def __init__(self):
        self.memory = [[100,'F',-1]]
        self.tape_drive = 5


def execute(p, tmp_finish=0):
    p.finish = tmp_finish + p.ser
    p.round = p.finish - p.arr
    p.weighted = p.round / p.ser
    tmp_finish = p.finish
    tmp_p = p
    return tmp_finish, tmp_p


def schedule(pcb_lst, ready_lst, sign=0, tmp_p=None, recur=0):
    # 作业调度FIFO
    idx_arr = sorted(range(len(pcb_lst)), key=lambda k: pcb_lst[k].arr)
    tmp_pcb_lst = [pcb_lst[i] for i in idx_arr]

    if tmp_p is None:
        tmp_finish = 0
    else:
        tmp_finish = tmp_p.finish

    reserve_lst = []
    for i, p in enumerate(tmp_pcb_lst):
        if sign == 0 and  p.arr > tmp_finish:
            r.tape_drive += tmp_p.tape_drive
            dpa.recycle(r.memory, (tmp_p.name, 'a', tmp_p.memory))
            print("内存: {}, 磁带机: {}".format(r.memory, r.tape_drive))
            print("\n执行{}".format(ready_lst[0].name))

            tmp_finish, tmp_p = execute(ready_lst[0], tmp_finish)
            ready_lst.pop(0)

        job = (p.name, 'a', p.memory)
        if dpa.alloc_ff(r.memory, job) and r.tape_drive-p.tape_drive >= 0:
            r.tape_drive -= p.tape_drive
            ready_lst.append(p)
            if recur >= 1:
                tmp_t = tmp_finish
            else:
                tmp_t = p.arr
            p.arr_memory = tmp_t

            # 短进程优先排序
            idx_arr = sorted(range(len(ready_lst)), key=lambda k: ready_lst[k].ser)
            ready_lst = [ready_lst[i] for i in idx_arr]
            print("就绪队列: {}".format([_.name for _ in ready_lst]))
        else:
            dpa.recycle(r.memory, job)
            reserve_lst.append(p)

        if sign == 1:
            # 执行
            print("内存: {}, 磁带机: {}".format(r.memory, r.tape_drive))
            print("\n执行{}".format(ready_lst[0].name))
            tmp_finish, tmp_p = execute(ready_lst[0], tmp_finish)

            ready_lst.pop(0)
            sign = 0

    r.tape_drive += tmp_p.tape_drive
    dpa.recycle(r.memory, (tmp_p.name, 'a', tmp_p.memory))
    print("内存: {}, 磁带机: {}".format(r.memory, r.tape_drive))

    if len(reserve_lst) == 0:
        print("\n执行{}".format(ready_lst[0].name))
        _, _ = execute(ready_lst[0], tmp_finish)
        r.tape_drive += ready_lst[0].tape_drive
        dpa.recycle(r.memory, (ready_lst[0].name, 'a', ready_lst[0].memory))
        print("内存: {}, 磁带机: {}".format(r.memory, r.tape_drive))
        ready_lst.pop(0)
        return

    if len(ready_lst) == 0 :
        return

    recur += 1
    schedule(reserve_lst, ready_lst, 1, tmp_p, recur)


if __name__ == '__main__':
    print("--------------多道批处理系统两级调度--------------")
    print("蒋功耀 \t 3117005125")
    print("----------------------开始----------------------")

    '''
    测试用例
    作业| 到达时间 | 估计运行时间| 内存需要| 磁带机需要
    1 10:00 25 15k 2
    2 10:20 30 60k 1
    3 10:30 10 50k 3
    4 10:35 20 10k 2
    5 10:40 15 30k 2
    '''
    name_lst = ["JOB1", "JOB2", "JOB3", "JOB4", "JOB5"]
    num = len(name_lst)
    arr_lst = [0, 20, 30, 35, 40]
    ser_lst = [25, 30, 10, 20, 15]
    memory_need = [15, 60, 50, 10, 30]
    taped_need = [2, 1, 3, 2, 2]
    pcb_lst = []

    for i in range(num):
        pcb = PCB()
        pcb.name = name_lst[i]
        pcb.arr = arr_lst[i]
        pcb.ser = ser_lst[i]
        pcb.memory = memory_need[i]
        pcb.tape_drive = taped_need[i]
        pcb_lst.append(pcb)

    r = Resource()
    schedule(pcb_lst, [], 1)

    print("\n--------------------------------------------")
    for p in pcb_lst:
        p.prt_pcb()

    print("\n----------------------结束----------------------")
