import random
import numpy as np
import pandas as pd
import h5py
from itertools import combinations




class leg(object):
    def __init__(self, pos, attrs={"terminated": False, "direction": False}):
        """
        A leg has two important attribues: pos (positions) and attrs (a custom list of attributes)
        """
        self.pos = pos
        self.attrs = dict(attrs)


class Fork(object):
    """
    A replication fork class provides fast access to attributes and positions
    """

    def __init__(self, leg1, leg2):
        self.left = leg1
        self.right = leg2


    def any(self, attr):
        return self.left.attrs[attr] or self.right.attrs[attr]

    def all(self, attr):
        return self.left.attrs[attr] and self.right.attrs[attr]
    #
    def get_term_fork(self):
        if self.all('terminated'):
            return 'both'
        elif self.left.attrs['terminated']:
            return 'left'
        elif self.right.attrs['terminated']:
            return 'right'

    def __getitem__(self, item):
        if item == -1:
            return self.left
        elif item == 1:
            return self.right
        else:
            raise ValueError()

def weightSampling(weights):
    """
    sampling from uniform distribution
    """

    ran = np.random.uniform(0, 1)

    weight_sum = 0

    for idx in range(len(weights)):
        weight_sum += weights[idx]

        if ran <= weight_sum:
            return idx

def unloadProb(forks, args):
    """
    Defines unloading probability based on a state of fork
    """

    if forks.any('terminated'):
        return 1

    #return 1 / args['LIFETIME']
    return 0

def getComb(args):
    """
    Get init combinations of forks

    Return combinations of forks and their directions
    """
    n_forks = args['n_forks']
    all_directions = np.tile([-1, 1], n_forks//2)

    combs = list(combinations(range(n_forks), 2))

    # get directions for each combination
    combs_directions = [
        (all_directions[i[0]], all_directions[i[1]]) for i in combs
    ]

    return combs, combs_directions


def loadOne(forks, args):
    """
    forks: a list used to store all pairs of forks
    """

    # loading sites: [fork1,fork2,fork3,fork4...]
    loading_sites = args['loadingSites']


    weights = args['loadingWeights']
    norm_scales = args['norm_scales']

    # get combinations and directions
    combs, combs_directions = getComb(args)

    # get index of combination based on sampling
    idx = weightSampling(weights = weights)

    # get target combination
    target_comb, target_direction = combs[idx], combs_directions[idx]

    target_loading_pairs = (loading_sites[target_comb[0]], loading_sites[target_comb[1]])
    target_norm_scales = (norm_scales[target_comb[0]], norm_scales[target_comb[1]])

    # get initiations of forks
    # initiations from same site
    if target_loading_pairs[0] == target_loading_pairs[1]:
        fork_loc = int(np.random.normal(
            loc = target_loading_pairs[0], scale = target_norm_scales[0]
        ))

        forks.append(
            Fork(
                leg1=leg(pos=fork_loc, attrs={'direction':target_direction[0], 'terminated':False}),
                leg2=leg(pos=fork_loc+1, attrs={'direction':target_direction[1], 'terminated':False})
            )
        )

        args['initiation_arrays'].append((fork_loc,fork_loc))

    # initiations from different sites
    else:
        fork_loc = np.random.normal(
            loc = target_loading_pairs, scale = target_norm_scales
        ).astype(int)

        forks.append(
            Fork(
                leg1=leg(pos=fork_loc[0], attrs={'direction':target_direction[0], 'terminated':False}),
                leg2=leg(pos=fork_loc[1], attrs={'direction':target_direction[1], 'terminated':False})
            )
        )

        args['initiation_arrays'].append(fork_loc)

def setTermination(args):
    """
    get termination sites using normal distribution
    """
    termCenter = args['termCenters']
    termStd = args['termStds']
    boundary = args['N']

    # random select termination sites based on normal distribution
    randomTermSites = np.random.normal(
        loc=termCenter, scale=termStd).astype(int)

    randomTermSites[randomTermSites<0] = 0
    randomTermSites[randomTermSites>=boundary] = boundary-1

    # record information of term sites
    args['termination_arrays'].append(list(randomTermSites))

    return randomTermSites
    
def translocate(forks, args):
    """
    This function describes everything that happens with forks -
    loading/unloading them

    It relies on the functions defined above: unload probability

    terminations: location of termination sites, ndarray object
    thresholdRadius: min absolute distance to termination site, int object

    """

    # init occupied array if this is the first
    # time of iteration
    time = args['times']
    occupied = args['occupied']
    boundary = args['N']

    if time < 1:
        # termination sites are labeled as 1 in occupied array
        # get termination sites from normal distribution based on given centers and standard variations
        terminations = setTermination(args)
        if not type(terminations) is np.ndarray:
            terminations = np.array(terminations)
        occupied[terminations] = 1

    speed_left = args['speed_left']
    speed_right = args['speed_right']

    assert speed_left > 0, 'Invalid speed of left fork'
    assert speed_right > 0, 'Invalid speed of right fork'

    # first we try to unload forks and free the matching occupied sites
    del_list = []
    for i in range(len(forks)):
        prob = unloadProb(forks[i], args)

        if prob < 1:
            ran = np.random.uniform()
            if ran < prob:
                del_list.append(i)
        else:
            del_list.append(i)

    # delete forks and reload one
    # after that, renew the termination sites
    for i in del_list:
        del forks[i]
        loadOne(forks, args)
        terminations = setTermination(args)
        #print(terminations)
        occupied = np.zeros_like(occupied)
        occupied[terminations] = 1
        args['occupied'] = occupied


    # translocate and mark terminated forks
    # here, we only have one pair of forks
    for i in range(len(forks)):
        paired_forks = forks[i]

        fork_left_direction = paired_forks.left.attrs['direction']
        fork_right_direction = paired_forks.right.attrs['direction']

        # consider the speed and update step
        # left fork
        for _ in range(speed_left):

            if paired_forks.left.pos + fork_left_direction <=0 or \
                    paired_forks.left.pos + fork_left_direction >= boundary-1:
                paired_forks.left.attrs['terminated'] = True
                continue

            if occupied[paired_forks.left.pos + fork_left_direction] != 0:
                paired_forks.left.attrs['terminated'] = True

            else:
                # update steps for left fork
                paired_forks.left.pos += fork_left_direction

        # right fork
        for _ in range(speed_right):

            if paired_forks.right.pos + fork_right_direction <=0 or \
                    paired_forks.right.pos + fork_right_direction >= boundary-1:
                paired_forks.right.attrs['terminated'] = True
                continue

            if occupied[paired_forks.right.pos + fork_right_direction] != 0:
                paired_forks.right.attrs['terminated'] = True

            else:
                # update steps for right fork
                paired_forks.right.pos += fork_right_direction

        # update forks
        forks[i] = paired_forks

    args['times'] += 1

def color(forks, args):

    def state(attrs):
        if attrs["terminated"]:
            return 2
        return 1

    ar = np.zeros(args["N"])
    for i in forks:
        ar[i.left.pos] = state(i.left.attrs)
        ar[i.right.pos] = state(i.right.attrs)
    return ar

