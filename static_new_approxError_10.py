import cprta
import timing
import random
import math
import numpy as np
import task_generator
import mixed_task_builder
import sort_task_set
import EPST
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
name='test'

# Information about the general task set
tasksinBkt = [10]

# Information about the mixed task set
wcetF2 = 2.2/1.2
faultRate = [10**-6.]
hardTaskFactor = [wcetF2]
numDeadline = [1]

stampCPRTA=[]
tasks=[]
keepsTasks=[]
numberOfRuns = 1
c_prob = []
seq_prob = []
for j in tasksinBkt:
    fileName = 'static_mp_tasks'+repr(j)+'_utilization'+repr(60)
    folder = 'comparison/'
    file = open(folder + 'txt/' +  fileName + '.txt', "w")
    file.write('Num of deadline miss: ' + repr(1) + '\n')
    file.write('Utilization: '+repr(60) + '\n')

    for i in range(numberOfRuns):
        print "Sample", i
        file.write('Generated '+ repr(j) +'samples:'+repr(i)+'\n')
        tasks=[{'period': 7.813062365925364, 'abnormal_exe': 1.2056916589204292, 'deadline': 7.813062365925364, 'execution': 0.6576499957747795, 'type': 'hard', 'prob': 1e-06},{'period': 10.389079642540985, 'abnormal_exe': 1.3682131320747648, 'deadline': 10.389079642540985, 'execution': 0.7462980720407807, 'type': 'hard', 'prob': 1e-06},{'period': 11.455577025853394, 'abnormal_exe': 0.040053587424360805, 'deadline': 11.455577025853394, 'execution': 0.021847411322378617, 'type': 'hard', 'prob': 1e-06},{'period': 13.329483118797697, 'abnormal_exe': 0.4179661173558873, 'deadline': 13.329483118797697, 'execution': 0.2279815185577567, 'type': 'hard', 'prob': 1e-06},{'period': 18.939533947948206, 'abnormal_exe': 0.2940969141370769, 'deadline': 18.939533947948206, 'execution': 0.16041649862022375, 'type': 'hard', 'prob': 1e-06},{'period': 20.62984435378786, 'abnormal_exe': 2.397627445940501, 'deadline': 20.62984435378786, 'execution': 1.3077967886948185, 'type': 'hard', 'prob': 1e-06},{'period': 27.29430617559634, 'abnormal_exe': 6.250771835669994, 'deadline': 27.29430617559634, 'execution': 3.409511910365451, 'type': 'hard', 'prob': 1e-06},{'period': 44.64020573051159, 'abnormal_exe': 1.1622487274497593, 'deadline': 44.64020573051159, 'execution': 0.6339538513362323, 'type': 'hard', 'prob': 1e-06},{'period': 44.75904828442813, 'abnormal_exe': 16.80828954471461, 'deadline': 44.75904828442813, 'execution': 9.168157933480696, 'type': 'hard', 'prob': 1e-06},{'period': 49.39112337206257, 'abnormal_exe': 0.830012758734867, 'deadline': 49.39112337206257, 'execution': 0.45273423203720015, 'type': 'hard', 'prob': 1e-06}]
        #tasks=task_generator.taskGeneration_p(j,60)
        #tasks=mixed_task_builder.hardtaskWCET(tasks, 1.83, 10**-6.)
        keepsTasks=tasks[:]
        for k in tasks:
            file.write(repr(k) + ',')
            file.write('\n')

        #the following part is for testing
        file.write('DMP:\n')
        tdar = EPST.probabilisticTest_po(tasks, 3, 10)
        timing.tlog_start("CPRTA starts", 1)
        cpa = cprta.cprtao(keepsTasks)
        timing.tlog_end("CPRTA ends", stampCPRTA, 1)
        if len(stampCPRTA)!=0):
            file.write('Duration: '+repr(stampCPRTA[-1])+'\n')
        if tdar < cpa:
            file.write('bug?\n')

        file.write('EPST-K:\n')
        file.write(repr(tdar) + ',')
        file.write('\n')
        file.write('CPRTA:\n')
        file.write(repr(cpa) + ',')
        file.write('\n')
        c_prob.append(cpa)
        seq_prob.append(tdar)
        file.write('\n')

file.write('DMP:\n')
file.write('EPST-K:\n')
for i in seq_prob:
    file.write(repr(i) + ',')

file.write('\n')
file.write('CPRTA:\n')
for i in c_prob:
    file.write(repr(i) + ',')

file.write('\n')
file.close()
