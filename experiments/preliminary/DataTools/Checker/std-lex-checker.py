#####################################################################################################
#####################################################################################################
# Will list all of the incomplete id's that need to finish running, for standard lexicase treatments
#
# Command Line Inputs
#
# Input 1: file directory where all the folders are located
# Input 2: Selection scheme we are for
# Input 3: Diagnostic we are looking for
# Input 4: Experiment seed offset
#
# Output : list of seeds that need to be reran in terminal display
#
# python3
#####################################################################################################
#####################################################################################################


######################## IMPORTS ########################
import argparse
import pandas as pd
import csv
import sys
import os

# Experiment variables
REP_CNT = 50

# return the number of rows in a csv file
def CountRows(file_name):
    # create pandas data frame of entire csv
    df = pd.read_csv(file_name)
    gens = df['gen'].to_list()

    return gens[-1]

# responsible for looking through the data directories for success
def CheckDir(dir, acc, gens):

    # check if data dir exists
    if os.path.isdir(dir):
        print('Data dirctory exists=', dir)
    else:
        print('DOES NOT EXIST=', dir)
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    print('Full data Dir=', dir)
    print('Now checking data replicates sub directories')

    # step 2: create seed data directories and check if exist
    VLIST = ['10', '20', '50', '100', '200', '500', '1000']
    DIR_DNE = []
    DAT_DNE = []
    DAT_DNF = []

    SEEDS = [str(x) for x in range(1,351)]

    for seed in SEEDS:
        var_val = VLIST[int((int(seed)-1)/REP_CNT)]
        DATA_DIR = dir + 'TRT_' + var_val + '__ACC_' + acc + '__GEN_' + gens + '/DIA_EXPLORATION__EPS_0.0__SEED_' + seed +'/'

        print('Sub directory:', DATA_DIR)

        # add full directory to missing list if not there
        if os.path.isdir(DATA_DIR) == False:
            DIR_DNE.append(int(seed))
            continue

        # now check if the data file exists in full data director
        if os.path.isfile(DATA_DIR + 'data.csv') == False:
            DAT_DNE.append(int(seed))
            continue

        # make sure that the data.csv file did in fact finish all generations
        if CountRows(DATA_DIR + 'data.csv') != int(gens):
            DAT_DNF.append(int(seed))
            continue

    # print out the list of incomplete seeds
    print()
    print('Directories that were not created:', DIR_DNE)
    print('Data files that do not exist:', DAT_DNE)
    print('Data files that did not finish:', DAT_DNF)
    print('')
    print('Total list of unfinished runs:')

    fin = DIR_DNE + DAT_DNF + DAT_DNE
    fin.sort()
    fins = ''
    for x in fin:
        fins = fins + str(x) + ','
    # print out the sorted list
    print(fins[:len(fins)-1])
    print('-'*(len(fins)-1))


def main():
    # Generate and get the arguments
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("data_directory", type=str, help="Target experiment directory.")
    parser.add_argument("accuracy", type=str, help="Accuracy for experiment")
    parser.add_argument("generations", type=str, help="Number of generations experiments ran for")

    # Parse all the arguments
    args = parser.parse_args()
    data_dir = args.data_directory.strip()
    print('Data directory=',data_dir)
    accuracy = args.accuracy
    print('Accuracy=', accuracy)
    generations = args.generations
    print('Generations=', generations)


    # Get to work!
    print("\nChecking all related data directories now!")
    CheckDir(data_dir, accuracy, generations)


if __name__ == "__main__":
    main()