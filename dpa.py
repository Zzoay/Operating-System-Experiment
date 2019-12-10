#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Yaozz
# Date: 2019-11-29
# Remark: 动态分区分配


'''
    memory : [内存空间(int)| 标识符(str)| 使用的进程号(int)（-1表示未使用）]
    job: (进程号(int)| 空间(int)| 标识符(str))
    标识符说明：
    memory: 'F'表示Free,即该内存空闲；'U'表示Used,表示该内存正在被使用。
    job: 'a'表示申请内存，'f'表示释放内存。
'''

# 申请空间（先进先出）
def alloc_ff(memory, job):
    jid = job[0]
    asize = job[2]
    if memory is None:
        return
    for i, m in enumerate(memory):
        if m[1] is 'F' and m[0] > asize:
            memory.insert(i + 1, [m[0] - asize, 'F', -1])
            try:
                if memory[i + 2][1] is 'F':
                    memory[i + 1][0] += memory[i + 2][0]
                    memory.pop(i + 2)
            except IndexError:
                pass

            m[0] = asize
            m[1] = 'U'
            m[2] = jid
            return memory


# 申请空间（最佳适应）
def alloc_bf(memory, job, reverse=False):
    jid = job[0]
    asize = job[2]
    if memory is None:
        return
    m_sorted = sorted(memory, key=lambda x: x[0], reverse=reverse)
    for ms in m_sorted:
        if ms[1] is 'F' and ms[0] > asize:
            break
    for i, m in enumerate(memory):
        if m[1] is 'F' and m[0] == ms[0]:
            memory.insert(i + 1, [m[0] - asize, 'F', -1])
            try:
                if memory[i+2][1] is 'F':
                    memory[i+1][0] += memory[i+2][0]
                    memory.pop(i+2)
            except IndexError:
                pass

            m[0] = asize
            m[1] = 'U'
            m[2] = jid
            return memory


# 回收空间
def recycle(memory, job):
    if memory is None:
        return
    for i, m in enumerate(memory):
        if m[2] == job[0] and m[1] is 'U':
            m[1] = 'F'
            m[2] = -1
            if i != 0 and memory[i - 1][1] is 'F' :
                memory[i - 1][0] += m[0]
                memory.remove(m)
                if memory[i][1] is 'F':
                    memory[i - 1][0] += memory[i][0]
                    memory.pop(i)
            elif i != len(memory) and memory[i + 1][1] is 'F':
                memory[i][0] += memory[i + 1][0]
                memory.remove(memory[i + 1])
    return memory


def first_fit(memory, job_lst):
    for i, m in enumerate(job_lst):
        if job_lst[i][1] is 'a':
            memory = alloc_ff(memory, job_lst[i])
            print(memory)
        if job_lst[i][1] is 'f':
            memory = recycle(memory, job_lst[i])
            print(memory)

    return memory


def best_fit(memory, job_lst, reverse=False):
    for i, m in enumerate(job_lst):
        if job_lst[i][1] is 'a':
            memory = alloc_bf(memory, job_lst[i], reverse)
            print(memory)
        if job_lst[i][1] is 'f':
            memory = recycle(memory, job_lst[i])
            print(memory)
    return memory



if __name__ == '__main__':
    # 测试用例
    memory = [[640,'F',-1]]
    job_lst = [(1,'a',130), (2,'a',60), (3,'a',100), (2,'f',60), (4,'a',200), (3,'f',100), (1,'f',130), (5,'a',140),
           (6,'a',60),(7,'a',50),(8,'a',60)]

    print("--------首次适应：------")
    first_fit(memory, job_lst)

    memory = [[640,'F',-1]]
    print("--------最佳适应：------")
    best_fit(memory, job_lst)

    memory = [[640,'F',-1]]
    print("--------最差适应：------")
    best_fit(memory, job_lst, reverse=True)