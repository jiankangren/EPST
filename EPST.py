from __future__ import division
import random
import math
import numpy as np
import sys, getopt
import matplotlib.pyplot as plt
from scipy.optimize import *
from sympy import *
from bounds import *

def ktda_pt(task, higherPriorityTasks, criteria, bound): #only for one deadline miss
    kpoints = []
    # pick up k testing points here
    for i in higherPriorityTasks:
        point = math.floor(task['period']/i['period'])*i['period']
        kpoints.append(point)
    kpoints.append(task['period'])

    # for loop checking k points time
    minP = 1.
    for t in kpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)
#        res = minimize_scalar(lambda x : Chernoff_bounds(task, higherPriorityTasks, fy, x), method='bounded', bounds=[0,bound])
        probRes = Chernoff_bounds(task, higherPriorityTasks, fy, 1)
        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP

def probabilisticTest_pt(tasks, numDeadline, bound):
    seqP = []
    x = 0
    res = 0
    for i in tasks:
        hpTasks = tasks[:x]
        x+=1
        if numDeadline == 1:
            resP = ktda_pt(i, hpTasks, 'abnormal_exe', bound)
        else:
            print "only for one deadline"
        seqP.append(resP)
        res = resP
    return res

def ptda_pt(task, higherPriorityTasks, criteria, bound): #only for one deadline miss
    # while loop checking all points time
    kpoints = []
    # pick up k testing points here
    for i in higherPriorityTasks:
        for r in range(1, int(math.floor(task['period']/i['period']))+1):
            point = r*i['period']
            kpoints.append(point)
    kpoints.append(task['period'])
#    print kpoints
    minP = 1.
    for t in kpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)
        probRes = Chernoff_bounds(task, higherPriorityTasks, fy, 1)
        t = workload
        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP

def probabilisticTest_ptda_pt(tasks, numDeadline, bound):
    seqP = []
    x = 0
    res = 0
    for i in tasks:
        hpTasks = tasks[:x]
        x+=1
        resP = ptda_pt(i, hpTasks, 'abnormal_exe', bound)
        seqP.append(resP)

        res = resP
    return res

def probabilisticTest_po(tasks, numDeadline, bound):
    seqP = []
    x = 0
    for i in tasks:
        if x != len(tasks)-1:
            x+=1
            continue
        hpTasks = tasks[:x]
        resP = ktda_p(i, hpTasks, 'abnormal_exe', bound)
        seqP.append(resP)
    return max(seqP)

def determineWorkload(task, higherPriorityTasks, criteria, time):
    workload = task[criteria]
    for i in higherPriorityTasks:
        jobs = math.ceil(time / i['period'])
        workload += jobs * i[criteria]
        #print("jobs " + repr(jobs) + " wl task " + repr(jobs * i[criteria]) + " total workload " + repr(workload))
    return workload

def probabilisticTest_ptda(tasks, numDeadline, bound):
    seqP = []
    x = 0
    for i in tasks:
        hpTasks = tasks[:x]
        resP = ptda(i, hpTasks, 'abnormal_exe', bound)
        seqP.append(resP)
        x+=1

    return max(seqP)

def ptda(task, higherPriorityTasks, criteria, bound): #only for one deadline miss
    # while loop checking all points time
    kpoints = []
    # pick up k testing points here
    for i in higherPriorityTasks:
        for r in range(1, int(math.floor(task['period']/i['period']))+1):
            point = r*i['period']
            kpoints.append(point)
    kpoints.append(task['period'])
#    print kpoints
    minP = 1.
    for t in kpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)
        res = minimize_scalar(lambda x : Chernoff_bounds(task, higherPriorityTasks, fy, x), method='bounded', bounds=[0,bound])
        probRes = Chernoff_bounds(task, higherPriorityTasks, fy, res.x)
        t = workload
        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP

def ktda_p(task, higherPriorityTasks, criteria, bound): #only for one deadline miss
    kpoints = []
    # pick up k testing points here
    for i in higherPriorityTasks:
        point = math.floor(task['period']/i['period'])*i['period']
        kpoints.append(point)
    kpoints.append(task['period'])

    # for loop checking k points time
    minP = 1.
    for t in kpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)
        res = minimize_scalar(lambda x : Chernoff_bounds(task, higherPriorityTasks, fy, x), method='bounded', bounds=[0,bound])
        probRes = Chernoff_bounds(task, higherPriorityTasks, fy, res.x)
        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP

def ktda_k(task, higherPriorityTasks, criteria, window, bound):
    kpoints = []
    # pick up k testing points here
    if window != 1:
        for i in higherPriorityTasks:
            for j in range(1, window+1):
                point = math.floor((j)*task['period']/i['period'])*i['period']
                kpoints.append(point)
    else:
        for i in higherPriorityTasks:
            point = math.floor(task['period']/i['period'])*i['period']
            kpoints.append(point)

    if window != 1:
        kpoints.append((window+1)*task['period'])
    else:
        kpoints.append(task['period'])

    '''
    kpoints.sort()
    if len(higherPriorityTasks) == 9:
        print "dtda_points:\n"
        print kpoints
    '''
    # for loop checking k points time
    minP = 1.
    for t in kpoints:
        workload = determineWorkload(task, higherPriorityTasks, criteria, t)
        if workload <= t:
            return 0
        #as WCET does not pass, check if the probability is acceptable
        fy = float(t)
        try:
            res = minimize_scalar(lambda x : Chernoff_bounds(task, higherPriorityTasks, fy, x), method='bounded', bounds=[0,bound]) #find the x with minimum
            probRes = Chernoff_bounds(task, higherPriorityTasks, fy, res.x) #use x to find the minimal
        except TypeError:
            print "TypeError"
            probRes = 1
        if minP > probRes: #find out the minimum in k points
            minP = probRes
    return minP


def kltda(task, higherPriorityTasks, criteria,  numDeadline, oneD, bound):
    #oneD is precalculated outside of function call
    if numDeadline == 0:
        return 1
    if numDeadline == 1:
        return oneD
    else:
        maxi = 0.
        for w in range(0, numDeadline):
            tmpP=ktda_k(task, higherPriorityTasks, criteria,  numDeadline-w, bound) * kltda(task, higherPriorityTasks, criteria, w, oneD, bound)
            if(tmpP > maxi):
                maxi = tmpP
        return maxi

def probabilisticTest_p(tasks, numDeadline, bound):
    seqP = []
    x = 0
    for i in tasks:
        hpTasks = tasks[:x]
        if numDeadline == 1:
            resP = ktda_p(i, hpTasks, 'abnormal_exe', bound)
        else:
            resP = kltda(i, hpTasks, 'abnormal_exe',  numDeadline, ktda_p(i, hpTasks, 'abnormal_exe', bound),bound)
        seqP.append(resP)
        x+=1
    return max(seqP)


