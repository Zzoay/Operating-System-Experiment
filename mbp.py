#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yaozz
# Date: 2019-12-27
# Remark: Two Level Scheduling in Multi-Batch Processing ScheduleSystem 多道批处理系统两级调度的模拟

import sys
import argparse

import spf
import dpa


class PCB(spf.PCB): # 继承
    def __init__(self):
        super().__init__()
        self.memory = 0
        self.tape_drive = 0
        self.arr_memory = 0 # 到达内存时间
        self.status = 0 # 0表示未完成，1表示完成，2表示资源已回收
        self.running = 0 # 已经运行时间
        self.remain = self.ser # 剩余需要运行时间


    # 方法重写
    def prt_pcb(self):
        print("作业名|到达时间|进入内存时间|服务时间|完成时间|周转时间|带权周转时间")
        print("{:^6}|{:^8}|{:^10}|{:^8}|{:^8}|{:^8}|{:.2f}".format(self.name, self.arr, self.arr_memory, self.ser, self.finish, self.round, self.weighted))


# 资源
class Resource(object):
    def __init__(self, memory, tape_drive):
        self.memory = memory
        self.tape_drive = tape_drive

    def prt_resource(self):
        print("内存: {}, 磁带机: {}\n".format(self.memory, self.tape_drive))

    # 回收资源
    def recycle(self, p):
        if p.status not in [0, 1, 2]:
            raise MBPError("002", "Resource.recycle() 任务状态有误")
        if p.status == 0:
            raise MBPError("003", "Resource.recycle() 任务未完成，无法回收资源")
        elif p.status == 2:
            # 任务已完成资源回收
            return
        self.tape_drive += p.tape_drive
        dpa.recycle(self.memory, (p.name, 'a', p.memory))
        p.status = 2
        r.prt_resource()


# 调度系统
class ScheduleSystem():
    def __init__(self, pcb_lst, resource, preempt):
        self.preempt = preempt
        self.core_nums = 1 # 核心数
        self.input_well = pcb_lst.copy()    # 输入井
        self.reserve_lst = []   # 后备队列
        self.ready_lst = []     # 就绪队列
        self.running_lst = []   # 运行队列
        self.time = 0# 时间
        self.resource = resource    # 资源
        self.done = False   # 是否完成

    def prt_NowTime(self):
        print("当前时间：{}".format(self.time))

    # 将任务加入后备队列
    def reserve(self):
        arr_lst = [_.arr for _ in self.input_well]
        if self.time in arr_lst:
            self.prt_NowTime()
            self.reserve_lst.append(self.input_well[0])
            print("后备队列: {}".format([_.name for _ in self.reserve_lst]))
            self.input_well.pop(0)

    # 调度方法
    def schedule_func(self, pj_lst:list, pj_scd:str):
        tmp_pj_lst = pj_lst
        if pj_scd.upper() == "FIFO":
            idx_arr = sorted(range(len(tmp_pj_lst)), key=lambda k: tmp_pj_lst[k].arr)
        elif pj_scd.upper() == "SJF":
            idx_arr = sorted(range(len(tmp_pj_lst)), key=lambda k: tmp_pj_lst[k].ser)
        elif pj_scd.upper() == "SPF":
            idx_arr = sorted(range(len(tmp_pj_lst)), key=lambda k: tmp_pj_lst[k].ser)
        else:
            raise MBPError("001", "mbp.py 调度方式参数输入有误")
        result_pj_lst = [tmp_pj_lst[i] for i in idx_arr]
        return result_pj_lst

    # 作业调度
    def schedule_job(self, j_scd):
        self.reserve_lst = self.schedule_func(self.reserve_lst, pj_scd=j_scd)

    # 进程调度，分配资源
    def schedule_process(self, p_scd):
        for i, reserve_p in enumerate(self.reserve_lst):
            job = (reserve_p.name, 'a', reserve_p.memory)
            # 预分配
            if dpa.alloc_ff(r.memory, job) and r.tape_drive - reserve_p.tape_drive >= 0:
                r.tape_drive -= reserve_p.tape_drive

                # 进程调度
                reserve_p.arr_memory = self.time
                self.ready_lst.append(reserve_p)
                self.ready_lst = self.schedule_func(self.ready_lst, pj_scd=p_scd)
                print("就绪队列: {}".format([_.name for _ in self.ready_lst]))
                r.prt_resource()
                self.reserve_lst.pop(i)
            else:
                dpa.recycle(r.memory, job)

    # 抢占
    def preemption(self, ready_p, running_p):
        print("--{}剩余: {}个单位时间".format(running_p.name, running_p.remain))
        print("--{}抢占".format(ready_p.name))
        print("--执行{}".format(ready_p.name))

        self.running_lst.remove(running_p)
        self.running_lst.append(ready_p)
        print("运行任务数 {}".format(len(self.running_lst)))
        ready_p.running += 1
        ready_p.remain = ready_p.ser - ready_p.running

    # 进程运行
    def process_running(self, running_p):
        running_p.running += 1
        running_p.remain = running_p.ser - running_p.running

    # 进程完成，回收资源
    def process_finished(self, running_p):
        if running_p.remain == 0:
            running_p.finish = self.time
            running_p.round = running_p.finish - running_p.arr
            running_p.weighted = running_p.round / running_p.ser
            running_p.status = 1
            print("--执行{}: {}个单位时间".format(running_p.name, running_p.running))
            print("--完成{}".format(running_p.name))
            self.prt_NowTime()
            r.recycle(running_p)
            self.ready_lst.remove(running_p)
            self.running_lst.pop(0)

    # 执行进程
    def execute_process(self):
        run_nums = 0
        for ready_p in self.ready_lst:
            if run_nums == self.core_nums:
                break
            if len(self.running_lst) < self.core_nums:
                self.prt_NowTime()
                print("\n--执行{}".format(ready_p.name))
                self.running_lst.append(ready_p)
            else:
                for i, running_p in enumerate(self.running_lst):
                    if self.preempt and (running_p is not ready_p):
                        # 抢占
                        self.preemption(ready_p, running_p)
                    else:
                        self.process_running(running_p)

                    run_nums += 1
                    self.time += 1
                    # 进程完成，回收资源
                    self.process_finished(running_p)

    # 检查是否调度完成
    def check_done(self):
        if len(self.input_well) == 0 and len(self.reserve_lst) == 0 and len(self.running_lst) == 0:
            self.done = True
        return self.done

    # 运行调度
    def run_schedule(self, j_scd, p_scd):
        while True:
            # 后备队列
            self.reserve()

            # 作业调度
            self.schedule_job(j_scd=j_scd)
    
            # 进程调度
            self.schedule_process(p_scd=p_scd)

            # 进程执行
            self.execute_process()

            # 调度完成
            if self.check_done(): break


# 自定义异常
class MBPError(Exception):
    def __init__(self, code, error):
        super().__init__(self)  # 初始化父类
        self.error = error
        self.code = code

    def __str__(self):
        return '\033[1;31m<{}> {}\033[0m'.format(self.code, self.error)


def parse_argument(params):
    parser = argparse.ArgumentParser()
    for param in params:
        parser.add_argument(param[0], type=param[1], default=param[2])
    args = parser.parse_args(sys.argv[1:])
    return args

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

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
        pcb.remain = ser_lst[i]
        pcb.memory = memory_need[i]
        pcb.tape_drive = taped_need[i]
        pcb_lst.append(pcb)

    memory = [[100, "F", -1]]
    tape_drive = 4
    r = Resource(memory, tape_drive)
    r.prt_resource()

    default_params = [
        ('--j_scd', str, 'fifo'),
        ('--p_scd', str, 'fifo'),
        ('--preempt', str2bool, 'f')
    ]
    args = parse_argument(default_params)

    s = ScheduleSystem(pcb_lst, r, preempt=args.preempt)
    s.run_schedule(j_scd=args.j_scd, p_scd=args.p_scd)

    print("--------------------------------------------")
    for p in pcb_lst:
        p.prt_pcb()

    print("\n----------------------结束----------------------")
