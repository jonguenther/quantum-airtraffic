#!/usr/bin/env python
# Copyright 2017 German Aerospace Center (http://www.DLR.de)
# Author: Tobias Stollenwerk
# all rights reserved
# Modified by Jonathan Günther 2019

import itertools as it
import random
import numpy as np

# ----- Arguments for the function ------
# parser = argparse.ArgumentParser(description='Create ATM instances', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument('-o', '--output', default='data', help='output folder')
#     parser.add_argument('-n', '--repetitions', default='10', help='number of repetitions', type=int)
#     parser.add_argument('-f', '--Fmin', default='10', help='Minimum number of flights', type=int)
#     parser.add_argument('-F', '--Fmax', default='10', help='Maximum number of flights', type=int)
#     parser.add_argument('-c', '--Cmin', default='4', help='Minimum number of conflicts', type=int)
#     parser.add_argument('-C', '--Cmax', default='4', help='Max number of conflicts', type=int)
#     parser.add_argument('--Tmin', default='100', help='Minimum value of total time range', type=int)
#     parser.add_argument('--Tmax', default='100', help='Maximum value of total time range ', type=int)
#     parser.add_argument('--tmin', default='10', help='Minimum value of uncertainty in arrival time at conflict', type=int)
#     parser.add_argument('--tmax', default='10', help='Maximum value of uncertainty in arrival time at conflict', type=int)
#     parser.add_argument('--tspread', default='3', help='Maximum spread in time difference between trajctory points inside conflict', type=int)
#     parser.add_argument('--Dmin', default='18', help='Minimum value maximal delays', type=int)
#     parser.add_argument('--Dmax', default='18', help='Maximum value maximal delays', type=int)
#     parser.add_argument('--dmin', default='3', help='Minimum value delay steps', type=int)
#     parser.add_argument('--dmax', default='3', help='Maximum value delay steps ', type=int)

def create_instances(output='data/',
                     repetitions=10,
                     Fmin=10,
                     Fmax=10,
                     Cmin=4,
                     Cmax=4,
                     Tmin=100,
                     Tmax=100,
                     tmin=10,
                     tmax=10,
                     tspread=3,
                     Dmin=18,
                     Dmax=18,
                     dmin=3,
                     dmax=3,
                     names_only=False,
                     seed=0):

    FValues = list(range(Fmin, Fmax + 1))
    CValues = list(range(Cmin, Cmax + 1))
    TValues = list(range(Tmin, Tmax + 1))
    tValues = list(range(tmin, tmax + 1))
    DValues = list(range(Dmin, Dmax + 1))
    dValues = list(range(dmin, dmax + 1))
    Nr = repetitions
    output = []
    random.seed(seed)

    NInstances = len(FValues) * len(CValues) * len(TValues) * len(tValues) * len(DValues) * len(dValues) * Nr
    print('Calculate %i instances' % NInstances)
    count = 0
    for F, C, TRangeMax, TRangeDelta, delayMax, delayDelta in it.product(FValues, CValues, TValues, tValues, DValues, dValues):
        for n in range(Nr):
            flights = [int(f) for f in np.arange(1, F+1)]
            conflicts = []
            for c in range(C):
                i = flights[random.randint(1, F - 1)]
                j = flights[random.randint(1, F - 1)]
                while (j == i):
                    j = flights[random.randint(1, F - 1)]
                if(i < j):
                    if((i,j) in conflicts):
                        continue
                    conflicts.append((i, j))
                else: 
                    if((j,i) in conflicts):
                        continue
                    conflicts.append((j,i))
            timeLimits = []
            for c in range(len(conflicts)):
                T = random.randint(0 + TRangeDelta, TRangeMax - TRangeDelta)
                Tmin = T - TRangeDelta
                Tmax = T + TRangeDelta
                t1 = random.randint(Tmin, Tmax)
                t2 = random.randint(Tmin, Tmax)
                ts = random.randint(0, tspread)
                tmin = t1 - t2 - ts
                tmax = t1 - t2 + ts
                if(tmin == tmax):
                    tmin = tmin - random.randint(1,TRangeDelta)
                timeLimits.append((tmin, tmax))
            delays = [int(d) for d in np.arange(0, delayMax + 1, delayDelta)]
            if not names_only:
                temp = {"flights": flights, "conflicts": conflicts, "timeLimits":timeLimits,"delays":delays}
                output.append(temp)
    return output
