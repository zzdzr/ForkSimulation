#!/usr/bin/env python
from itertools import combinations
import pandas as pd
import itertools
import click
import sys
import os
from simulation_1d_type2_fountains_new import *


# params of loading sites
N1 = 3000
M = 1
N = N1 * M
LEFNum = 1
args = {}

args['N'] = N
args["n_forks"] = 4
args['occupied'] = np.zeros(N)
args['loadingSites'] = [1000, 1000, 2000, 2000]
args['termCenters'] = [500, 1500, 2500]
args['times'] = 0
args['speed_left'] = 5
args['speed_right'] = 5

#norm_scales = [[50,50,50,50],[70,70,70,70],[90,90,90,90]]
norm_scales = [[15,15,15,15]]
termStds = [[200,200,200]]

# weights
#weight1 = np.repeat(1 / 6, 6)
# weights = [[0.25, 0.125, 0.125, 0.125, 0.125, 0.25],
#            [0.35, 0.075, 0.075, 0.075, 0.075, 0.35],
#            [0.4, 0.05, 0.05, 0.05, 0.05, 0.4]]
# [[0.5, 0, 0, 0, 0, 0.5]]
# combs = [
#     (0, 1),
#     (0, 2),
#     (0, 3),
#     (1, 2),
#     (1, 3),
#     (2, 3)
# ]
weights = [[0.3, 0.1, 0.1, 0.1, 0.1, 0.3]]
restartSimulationEveryBlocks = 100



# create list of all file names
n = 1
for weight, norm_scale, termStd in list(itertools.product(weights, norm_scales,termStds)):
    # make folders and file names
    fname = 'LEFPositions.h5'

    args['loadingWeights'] = weight
    args['termStds'] = termStd
    args['norm_scales'] = norm_scale
    args['initiation_arrays'] = []
    args['termination_arrays'] = []

    norm_scale_string = '_'.join(str(i) for i in norm_scale)
    termStd_string = '_'.join(str(i) for i in termStd)
    weights_string = '_'.join(str(i) for i in weights)
    save_folder = f"FullSims_{n}"


    # load forks
    myforks = []
    for i in range(LEFNum):
        loadOne(myforks, args)

    # translocate
    # shape of cur: (150,1,2)

    #translocating_times = 0
    cur = []
    #while len(args['initiation_arrays']) < 300:
    while len(args['initiation_arrays']) < 300:
        # translocate!
        translocate(myforks, args)
        # get positions
        positions = [(fork.left.pos, fork.right.pos) for fork in myforks]
        cur.append(positions)

    translocating_times = args['times']
    trajectoryLength = restartSimulationEveryBlocks*((translocating_times//restartSimulationEveryBlocks)-1)
    print('trajectoryLength is %d' % trajectoryLength)

    # resize cur
    cur = cur[:trajectoryLength]
    print('length of cur is %d' % len(cur))

    # get bins
    steps = 50
    bins = np.linspace(0, trajectoryLength, steps, dtype=int)

    # make directory
    file = os.path.join(save_folder, fname)
    print(file)
    os.makedirs(save_folder)

    # store into hdf5
    with h5py.File(file, mode='w') as myfile:
        dset = myfile.create_dataset(
            "positions",
            shape=(trajectoryLength, LEFNum, 2),
            dtype=np.int32,
            compression="gzip"
        )

        for st, end in zip(bins[:-1], bins[1:]):
            dset[st:end] = cur[st:end]
        myfile.attrs["N"] = N
        myfile.attrs["LEFNum"] = LEFNum

    # write initiation sites and termination sites to hdf5 file
    initiation_first_df = pd.DataFrame(
        [i[0] for i in args['initiation_arrays']]
    )

    initiation_second_df = pd.DataFrame(
        [i[1] for i in args['initiation_arrays']]
    )


    termination_first_df = pd.DataFrame(
        [i[0] for i in args['termination_arrays']]
    )
    termination_second_df = pd.DataFrame(
        [i[1] for i in args['termination_arrays']]
    )
    termination_third_df = pd.DataFrame(
        [i[2] for i in args['termination_arrays']]
    )


    initiation_first_df_name = save_folder + '_initations_fisrt.txt'
    initiation_second_df_name = save_folder + '_initations_second.txt'

    termination_first_df_name = save_folder + '_terminations_first.txt'
    termination_second_df_name = save_folder + '_terminations_second.txt'
    termination_third_df_name = save_folder + '_terminations_third.txt'

    initiation_first_df.to_csv(
        initiation_first_df_name,
        sep='\t', index=None, header=None
    )
    initiation_second_df.to_csv(
        initiation_second_df_name,
        sep='\t', index=None, header=None
    )

    termination_first_df.to_csv(
        termination_first_df_name,
        sep='\t', index=None, header=None
    )
    termination_second_df.to_csv(
        termination_second_df_name,
        sep='\t', index=None, header=None
    )
    termination_third_df.to_csv(
        termination_third_df_name,
        sep='\t', index=None, header=None
    )


    # run 3d simulations
    command = 'python /home/members/zdzr/project/Fun2/simulations/two_origins/simulation_3d.py --folder {} --myfile {} --rs {} &'.format(
        save_folder, file, restartSimulationEveryBlocks
    )

    os.system(command)

    args['times'] = 0
    n+=1
