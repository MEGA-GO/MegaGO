import time
import subprocess

# Measure the time it takes to process one sample. Gradually increase the size of this sample to be able to model
# the experimental runtime behaviour. All results will be appended to a file called "timings.csv"

OUTPUT_FILE = "timings.csv"
INPUT_FILE_1 = "../data/sample7.csv"
INPUT_FILE_2 = "../data/sample8.csv"
TEMP_FILE_1 = "/tmp/input1.csv"
TEMP_FILE_2 = "/tmp/input2.csv"


# Measure the time it takes to process differently sized datasets. Start = at what size should both sets start?
# step_size = by how many items do the tested sets increase every iteration?
def perform_test(start, step_size):
    with open(OUTPUT_FILE, "w") as output:
        output.write("size set 1,size set 2,execution time (s)\n")
    set1 = read_input(INPUT_FILE_1)
    set2 = read_input(INPUT_FILE_2)
    print(f"Total size for set1 and set2 is ({len(set1)}, {len(set2)})")
    for size in range(start, min(len(set1), len(set2)), step_size):
        print(f"Processing for size: {size} * {size}.")
        s1 = set1[:size]
        s2 = set2[:size]
        write_temp_file(s1, TEMP_FILE_1)
        write_temp_file(s2, TEMP_FILE_2)
        start_time = time.time()
        subprocess.run(["megago", TEMP_FILE_1, TEMP_FILE_2], stdout=subprocess.PIPE)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f"Elapsed: {elapsed}s")
        with open(OUTPUT_FILE, "a") as f:
            f.write(f"{len(s1)},{len(s2)},{elapsed}\n")


def read_input(file):
    with open(file, "r") as f:
        # Skip header
        f.readline()
        return [line.rstrip() for line in f]


def write_temp_file(s, filename):
    lines = ["GO_TERM"]
    lines.extend(s)
    with open(filename, "w") as f:
        f.write("\n".join(lines) + "\n")


perform_test(50, 50)
