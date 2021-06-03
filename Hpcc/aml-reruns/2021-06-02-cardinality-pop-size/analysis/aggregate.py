
import argparse, os, copy, errno, csv, re, sys

run_dir_identifier = "RUN_"

# Parameters to exclude from aggregate data file
config_exclude = {
    "MU",
    "FIT_SIGMA",
    "FIT_ALPHA",
    "PNORM_EXP",
    "NOVEL_K",
    "DSLEX_PROP",
    "COH_LEX_PROP",
    "SNAP_INTERVAL",
    "PRINT_INTERVAL",
    "OUTPUT_DIR"
}

data_field_exclude = {

}

SELECTION_SCHEME_MAP = {
    "0":"MuLambda",
    "1":"Tournament",
    "2":"FitnessSharing",
    "3":"NoveltySearch",
    "4":"EpsilonLexicase",
    "5":"DownSampledLexicase",
    "6":"CohortLexicase",
    "7":"NoveltyLexicase"
}

"""
This is functionally equivalent to the mkdir -p [fname] bash command
"""
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def read_csv(file_path):
    content = None
    with open(file_path, "r") as fp:
        content = fp.read().strip().split("\n")
    header = content[0].split(",")
    # header_lu = {header[i].strip():i for i in range(0, len(header))}
    content = content[1:]
    lines = [{header[i]: l[i] for i in range(len(header))} for l in csv.reader(content, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)]
    return lines

"""
Given the path to a run's config file, extract the run's settings.
"""
def extract_settings(run_config_path):
    content = None
    with open(run_config_path, "r") as fp:
        content = fp.read().strip().split("\n")
    header = content[0].split(",")
    header_lu = {header[i].strip():i for i in range(0, len(header))}
    content = content[1:]
    configs = [l for l in csv.reader(content, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)]
    return {param[header_lu["parameter"]]:param[header_lu["value"]] for param in configs}

def gen_to_eval(gen, pop_size, tests, sample_prop=1.0):
    return gen * ( pop_size * (tests * sample_prop) )

def main():
    # Setup the commandline argument parser
    parser = argparse.ArgumentParser(description="Data aggregation script.")
    parser.add_argument("--data", type=str, nargs="+", help="Where should we pull data (one or more locations)?")
    parser.add_argument("--dump", type=str, help="Where to dump this?", default=".")
    parser.add_argument("--units", type=str, default="generations", choices=["generations", "evaluations", "interval"], help="Unit for resolution of time series: generations, evaluations, interval")
    parser.add_argument("--resolution", type=int, default=1, help="What resolution should we collect time series data at?")
    parser.add_argument("--out_fname", type=str, help="What should we call the output file?", default="timeseries.csv")

    args = parser.parse_args()
    data_dirs = args.data
    dump_dir = args.dump
    units = args.units
    resolution = args.resolution
    out_fname = args.out_fname

    # Are all data directories for real?
    if any([not os.path.exists(loc) for loc in data_dirs]):
        print("Unable to locate all data directories. Able to locate:", {loc: os.path.exists(loc) for loc in data_dirs})
        exit(-1)

    if resolution < 1:
        print("Resolution must be >= 1")
        exit(-1)

    mkdir_p(dump_dir)

    # aggregate run directories
    run_dirs = [os.path.join(data_dir, run_dir) for data_dir in data_dirs for run_dir in os.listdir(data_dir) if run_dir_identifier in run_dir]

    # sort run directories by seed to make easier on the eyes
    run_dirs.sort(key=lambda x : int(x.split("_")[-1]))
    print(f"Found {len(run_dirs)} run directories.")

    time_series_header_set = set() # Use this to guarantee all data file headers match

    time_series_info = []
    extra_fields = [
        "evaluations",
        "selection_name",
        "test_sample_prop"
    ]

    unfinished_runs = []
    for run in run_dirs:
        print(f"Extracting information from {run}")
        run_config_path = os.path.join(run, "run_config.csv")
        data_path = os.path.join(run, "data.csv")

        # does the run config file exist?
        if not os.path.exists(run_config_path):
            print(f"Failed to find run parameters ({run_config_path})")
            exit(-1)

        # does the data file exist?
        if not os.path.exists(data_path):
            print(f"Failed to find data file ({data_path})")
            exit(-1)

        # extract run settings
        run_settings = extract_settings(run_config_path)

        # process a few settings
        selection_name = SELECTION_SCHEME_MAP[run_settings["SELECTION"]]
        max_gen = int(run_settings["MAX_GENS"])
        test_sample_prop = 1.0
        if selection_name == "DownSampledLexicase":
            test_sample_prop = float(run_settings["DSLEX_PROP"])
        elif selection_name == "CohortLexicase":
            test_sample_prop = float(run_settings["COH_LEX_PROP"])

        # extract data file
        data = read_csv(data_path)

        # is run finished?
        gens_in_data = {int(line["gen"]) for line in data}
        if not max_gen in gens_in_data:
            unfinished_runs.append(run)

        # compute extra fields for each line
        line_keys = []
        for line in data:
            line["evaluations"] = gen_to_eval(
                gen=int(line["gen"]),
                pop_size=int(run_settings["POP_SIZE"]),
                tests=int(run_settings["OBJECTIVE_CNT"]),
                sample_prop=test_sample_prop
            )
            line["selection_name"] = selection_name
            line["test_sample_prop"] = test_sample_prop
            line_keys = line.keys()

        # filter data to appropriate resolution
        keep_line = lambda x,g : (not bool( x % resolution ) or g==max_gen)
        if units == "interval":
            data = [ data[i] for i in range(len(data)) if keep_line(i, int(data[i]["gen"])) ]
        elif units == "generations":
            data = [ line for line in data if keep_line(int(line["gen"]), int(line["gen"])) ]
        elif units == "evaluations":
            data = [ line for line in data if keep_line(int(line["evaluations"]), int(line["gen"])) ]

        data_fields = [field for field in line_keys if not field in data_field_exclude]
        config_fields = [field for field in run_settings if not field in config_exclude]
        fields = data_fields + config_fields
        fields.sort()
        header = ",".join(fields)

        # confirm that header is same as other data files
        time_series_header_set.add(header)
        if len(time_series_header_set) > 1:
            print(f"Header mismatch! ({run})")
            exit(-1)

        # add fields to info
        for line in data:
            info = {}
            for field in data_fields: info[field] = line[field]
            for field in config_fields: info[field] = run_settings[field]
            time_series_info.append(",".join([str(info[field]) for field in fields]))
        print(f"  Time points: {len(data)}")


    print("=============================")
    # Report any unfinished runs
    print(f"Unfinished runs ({len(unfinished_runs)})")
    for run in unfinished_runs:
        print(f"  - {run}")

    # write output
    out_content = list(time_series_header_set)[0] + "\n"
    out_content += "\n".join(time_series_info)
    with open(os.path.join(dump_dir, out_fname), "w") as fp:
        fp.write(out_content)
    print(f"DONE! Output written to {os.path.join(dump_dir, out_fname)}")


if __name__ == "__main__":
    main()