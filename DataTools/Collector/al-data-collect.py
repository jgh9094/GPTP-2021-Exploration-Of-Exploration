#####################################################################################################
#####################################################################################################
# Will create a csv how alex's r code expects data
#
# Command Line Inputs
#
# Input 1: file directory location
# Input 2: file dump directory
#
# Output : csv with generations found in dump directory
#
# python3
#####################################################################################################
#####################################################################################################

######################## IMPORTS ########################
import pandas as pd
import numpy as np
import argparse
import math as mth
import sys
import os

# variables we are testing for each replicate range
LC_LIST = ['10', '20', '50', '100', '200', '500', '1000']
DS_LIST = ['0.01', '0.02', '0.03', '0.12', '0.25', '0.5', '1.0']
# seed experiements replicates range
REP_NUM = 50
# columns we are interested in grabbing
POP_FIT_AVG = 'pop_fit_avg'
POP_FIT_MAX = 'pop_fit_max'
POP_OPT_AVG = 'pop_opt_avg'
POP_OPT_MAX = 'pop_opt_max'
POP_UNI_OBJ = 'pop_uni_obj'
COM_SOL_CNT = 'com_sol_cnt'
ELE_AGG_PER = 'ele_agg_per'
ELE_OPT_CNT = 'ele_opt_cnt'
COM_AGG_PER = 'com_agg_per'
COM_OPT_CNT = 'com_opt_cnt'
OPT_AGG_PER = 'opt_agg_per'
OPT_OBJ_CNT = 'opt_obj_cnt'

# return appropiate string dir name (based off run.sb file naming system)
def SetVariant(s):
    # case by case
    if s == 0:
        return 'LEXICASE'
    elif s == 1:
        return 'DOWNSAMPLED'
    elif s == 2:
        return 'COHORT'
    else:
        sys.exit("UNKNOWN VARIANT")

# return appropiate string dir name (based off run.sb file naming system)
def SetVariantVar(s):
    # case by case
    if s == 0:
        return 'EPS'
    elif s == 1:
        return 'PROP'
    elif s == 2:
        return 'COHP'
    else:
        sys.exit("UNKNOWN VARIANT VAR")

# Will set the appropiate list of variables we are checking for
def SetVarList(s):
    # case by case
    if s == 0:
        return LC_LIST
    elif s == 1:
        return DS_LIST
    else:
        sys.exit("UNKNOWN VARIANT LIST")

# return the correct amount of seed ran by experiment treatment
def SetSeeds():
    seed = []
    seed.append([x for x in range(1,51)])
    seed.append([x for x in range(51,101)])
    seed.append([x for x in range(101,151)])
    seed.append([x for x in range(151,201)])
    seed.append([x for x in range(201,251)])
    seed.append([x for x in range(251,301)])
    seed.append([x for x in range(301,351)])
    return seed

# loop through differnt files that exist
def DirExplore(data, dump, var, offs, res, obj, acc, gens):
    # check if data dir exists
    if os.path.isdir(data) == False:
        print('DATA=', data)
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # check if dump dir exists
    if os.path.isdir(dump) == False:
        print('DATA=', data)
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # what directory are we looking into
    SEL_DIR = data + SetVariant(var) + '/'
    print('Selection dir=', SEL_DIR)

    # Set vars that we need to loop through
    VLIST = SetVarList(var)
    SEEDS = SetSeeds()

    # gens we are expecting
    GEN_LIST = [x for x in range(int(gens)+1) if x%res == 0]
    # data frame list for concatanation
    DF_LIST = []

    # iterate through the sets of seeds
    for i in range(len(SEEDS)):
        seeds = SEEDS[i]
        var_val = str(VLIST[i])
        print('i=',i)

        TRT = [VLIST[i]] * len(GEN_LIST)

        # iterate through seeds to collect data
        for s in seeds:
            seed = str(int(s) + offs)
            DATA_DIR = ''

            # check the standard lexicase stuff
            if var == 0:
                DATA_DIR = SEL_DIR + 'TRT_' + var_val + '__ACC_' + acc + '__GEN_' + gens + '/DIA_EXPLORATION__EPS_0.0__SEED_' + seed +'/'
            else:
                DATA_DIR = SEL_DIR + 'TRT_100__ACC_' + acc + '__GEN_' + gens + '/DIA_EXPLORATION__PROP_' + var_val + '__SEED_' + seed +'/'

            print('DATA_DIR=', DATA_DIR)
            # # create pandas data frame of entire csv and grab the row
            df = pd.read_csv(DATA_DIR + 'data.csv')
            df = df.iloc[::res, :]
            ID = [seed] * len(GEN_LIST)

            # time to export the data
            cdf = pd.DataFrame({'gen': pd.Series(GEN_LIST),
                            'trt': pd.Series(TRT),
                            'fit_avg': pd.Series(df[POP_FIT_AVG].tolist()),
                            'fit_max': pd.Series(df[POP_FIT_MAX].tolist()),
                            'opt_avg': pd.Series(df[POP_OPT_AVG].tolist()),
                            'opt_max': pd.Series(df[POP_OPT_MAX].tolist()),
                            'uni_avg': pd.Series(df[POP_UNI_OBJ].tolist()),
                            'com_cnt': pd.Series(df[COM_SOL_CNT].tolist()),
                            'run_id': pd.Series(ID)})

            DF_LIST.append(cdf)

    fin_df = pd.concat(DF_LIST)

    fin_df.to_csv(path_or_buf= dump + 'al-' + SetVariant(var).lower() + '.csv', index=False)

def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_dir",    type=str, help="Target experiment directory.")
    parser.add_argument("dump_dir",    type=str, help="Data dumping directory")
    parser.add_argument("variant",   type=int, help="Lexicase variant we are looking for? \n0: standard\n1: down sampled\n2: cohort")
    parser.add_argument("seed_offset", type=int, help="Experiment seed offset. (REPLICATION_OFFSET + PROBLEM_SEED_OFFSET")
    parser.add_argument("resolution",  type=int, help="The resolution desired for the data extraction")
    parser.add_argument("objectives", type=str, help="Number of objectives being optimized")
    parser.add_argument("accuracy", type=str, help="Accuracy for experiment")
    parser.add_argument("generations", type=str, help="Number of generations experiments ran for")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_dir.strip()
    print('Data directory=',data_dir)
    dump_dir = args.dump_dir.strip()
    print('Dump directory=', dump_dir)
    variant = args.variant
    print('Lexicase varaint=', SetVariant(variant))
    offset = args.seed_offset
    print('Offset=', offset)
    resolution = args.resolution
    print('Resolution=', resolution)
    objectives = args.objectives
    print('Objectives=', objectives)
    accuracy = args.accuracy
    print('Accuracy=', accuracy)
    generations = args.generations
    print('Generations=', generations)

    # Get to work!
    print("\nChecking all related data directories now!")
    DirExplore(data_dir, dump_dir, variant, offset, resolution, objectives, accuracy, generations)

if __name__ == "__main__":
    main()