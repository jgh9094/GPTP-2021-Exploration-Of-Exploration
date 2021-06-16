# GPTP 2021 Experiments

This directory contains the HPCC submission scripts, configuration files, and analyses for each of the experiments included in our GPTP contribution.

`requirements.txt` specifies the requisite Python packages for our Python scripts.

The name of each experiment directory indicates the date we created and ran the experiment and descriptive tag.
Each directory associated with a particular experiment contains two directories: `analysis` and `hpcc`.
The `analysis` directory contains the Python script(s) used to aggregate data into a single `.csv` file and the R markdown documents used to analyze the data.
The `hpcc` directory contains the scripts used to submit jobs to our HPCC; in general, the `gen-sub.py` script specifies the experiment's configuration.
Modify and run the `job_gen.sh` to generate slurm job submission scripts.