# -*- coding: UTF-8 -*-
import random
import numpy as np
import matplotlib.pyplot as plt


def localcomput(pro,task_size,UE_com,UE_P):
    t_local = pro * task_size * UE_com
    E_local = t_local * UE_P
    return t_local,E_local

def offloding(pro,task_size,p_trans,CAP_com,CAP_P,rate):
    t_trans = (1 - pro) * task_size / rate
    E_trans = t_trans * p_trans
    t_cap = (1 - pro) * task_size * CAP_com
    E_cap = t_cap * CAP_P
    t_off = t_trans + t_cap
    E_off = E_cap + E_trans
    return t_off,E_off


def optimum(task_size, UE_com, CAP_com, UE_P, CAP_P, p_trans, rate):
    pro = 0
    best_pro = 0
    min_cost = 1000000000
    while pro < 1:
        # local computing
        t_local, E_local=localcomput(pro,task_size,UE_com,UE_P);
        # offloading
        # ignore downlink time
        t_off, E_off=offloding(pro, task_size, p_trans, CAP_com, CAP_P, rate)
        # total cost
        t = max(t_local, t_off)
        e = E_off + E_local
        cost = t + e
        if cost <= min_cost:
            best_pro = pro
            min_cost = cost
        pro += 0.01
    return cost, best_pro


ratelist=[]
costlist=[]
ramdcost=[]
offcostlist=[]

provelist=[]


def mian():
    task_size = random.uniform(100, 200)  # 任务大小 MB

    UE_com = random.uniform(1, 2)  # 设备处理1MB时间
    CAP_com = random.uniform(0.2, 0.8)  # 服务器处理1MB时间
    UE_P = random.uniform(0.005, 0.015)  # 用户设备功率 5w~15W
    CAP_P = random.uniform(0.05, 0.1)  # 服务器功率 50~100w
    p_trans = 0.0005  # 发射功率0.5w

    rate = random.uniform(1, 5)  # 传输速率 1~5MB/s


    t_local, E_local = localcomput(1,task_size,UE_com,UE_P)
    originalcost=t_local+ E_local


    #  best pro and its cost
    cost, pro = optimum(task_size, UE_com, CAP_com, UE_P, CAP_P, p_trans, rate)

    for rate in range(1,10):
        ratelist.append(rate)

        t_off, E_off = offloding(0, task_size, p_trans, CAP_com, CAP_P, rate)
        alloffcost = t_off + E_off
        offcostlist.append(alloffcost)

        clist = []
        rlist = []
        plist=[]

        if UE_com + UE_P*UE_com - CAP_com*CAP_P - p_trans/rate > 0:
            ppro = 1 - (UE_com *rate/ (UE_com*rate + CAP_com + 1))
        else:
            ppro = 1

        for i in range(1,10000):
             t_local, E_local = localcomput(pro, task_size, UE_com, UE_P)
             t_off, E_off = offloding(pro, task_size, p_trans, CAP_com, CAP_P, rate)
             clist.append(max(t_local,t_off)+E_local+E_off)

             randpro = random.random();
             randpro_t_local, randpro_E_local = localcomput(randpro, task_size, UE_com, UE_P)
             randpro_t_off, randpro_E_off = offloding(randpro, task_size, p_trans, CAP_com, CAP_P, rate)
             rlist.append(max(randpro_t_local, randpro_t_off) + randpro_E_local + randpro_E_off)


             ppro_t_local, ppro_E_local = localcomput(ppro, task_size, UE_com, UE_P)
             ppro_t_off, ppro_E_off = offloding(ppro, task_size, p_trans, CAP_com, CAP_P, rate)
             plist.append(max(ppro_t_local, ppro_t_off) + ppro_E_local + ppro_E_off)

        provelist.append(np.mean(plist))
        costlist.append(np.mean(clist))
        ramdcost.append(np.mean(rlist))
    return originalcost,alloffcost


originalcost,alloffcost=mian();





plt.xlabel("bandwidth")
plt.ylabel("cost")

plt.plot(ratelist,costlist,c="yellow",label="Proposed")
plt.plot(ratelist,ramdcost,c="black",label="Random")
plt.axhline(y=originalcost,c="blue",label="All-Local")
plt.plot(ratelist,offcostlist,c="red",label="All-CAP")
plt.plot(ratelist,provelist,c="green",label="Prove")
plt.legend()
plt.show();

