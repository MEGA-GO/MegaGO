import getopt
import sys
import subprocess
import pandas as pd
from io import StringIO
import os

# 1. Parse command line arguments
# 2. cd to the test directory
# 3. run tests
# 4. Print summary of successes and failures, exit with 0 if
#    all tests pass, else exit with 1

# The name of this test script
this_program_name = "megago-test.py"
# The program we want to test (either a full path to an executable, or the name of an executable in $PATH)
test_program = ""
# Directory containing the test data files and expected outputs
test_data_dir = ""
# Number of failed test cases
num_errors = 0
# Total number of tests run
num_tests = 0
# Is the program executed in verbose mode?
verbose = False


def show_help():
    print(f"""
{this_program_name}: run integration/regression tests for megago

Usage:
    {this_program_name} [-h] [-v] -p program -d test_data_dir

Example:
    {this_program_name} -p bin/megago -d data/tests

-h shows this help message

-v verbose output
    """)


# echo an error message $1 and exit with status $2
def exit_with_error(message, status):
    print(f"{this_program_name}: ERROR: {message}\n")
    exit(status)


# if -v is specified on the command line, print a more verbaose message to stdout
def verbose_message(message):
    if verbose:
        print(f"{this_program_name} {message}")


# Parse the command line arguments and set the global variables program and test_data_dir
def parse_args():
    global test_program
    global test_data_dir
    global verbose

    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'hp:d:v')
        for opt, arg in opts:
            if opt == "-h":
                show_help()
                exit(0)
            elif opt == "-p":
                test_program = arg
            elif opt == "-d":
                test_data_dir = arg
            elif opt == "-v":
                verbose = True
    except getopt.GetoptError:
        show_help()
        exit(1)

    if test_program == "":
        exit_with_error("missing command line argument: -p program, use -h for help", 2)

    if test_data_dir == "":
        exit_with_error("missing command line argument: -d test_data_dir, use -h for help", 2)


# Run a command and check that the output is
# exactly equal the contents of a specified file
# ARG1: command we want to test as a string
# ARG2: a file path containing the expected output
# ARG3: expected exit status
def test_stdout_exit(cmd, expected_output_file, expected_exit_status):
    global num_tests
    global num_errors

    num_tests += 1
    verbose_message(f"Testing stdout and exit status: $cmd")
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    exit_status = result.returncode

    if exit_status != expected_exit_status:
        num_errors += 1
        print(f"Test exit status failed: {cmd}")
        print(f"Actual exit status: {exit_status}")
        print(f"Expected exit status: {expected_exit_status}")
    else:
        df1 = pd.read_csv(StringIO(output))
        df2 = pd.read_csv(expected_output_file)

        try:
            pd.testing.assert_frame_equal(df1, df2, check_dtype=False)
        except AssertionError as e:
            num_errors += 1
            expected_output = open(expected_output_file).read()
            print(f"""
Test output failed: {cmd}
Actual output:
{output}
Expected output:
{expected_output}
Difference:
Tables are not equal!
left:\texpected output ({expected_output_file})
right:\tactual output

File comparison result (first unequal column):
{e}
            """)


# Run a command and check that the exit status is
# equal to an expected value
# exactly equal the contents of a specified file
# ARG1: command we want to test as a string
# ARG2: expected exit status
# NB: this is mostly for checking erroneous conditions, where the
# exact output message is not crucial, but the exit status is
# important
def test_exit_status(cmd, expected_exit_status):
    global num_tests
    global num_errors

    num_tests += 1
    verbose_message(f"Testing exit status: {cmd}")
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    exit_status = result.returncode

    if exit_status != expected_exit_status:
        num_errors += 1
        print(f"Test exit status failed: {cmd}")
        print(f"Actual exit status: {exit_status}")
        print(f"Expected exit status: {expected_exit_status}")


# 1. Parse command line arguments.
parse_args()
# 2. Change to test directory
os.chdir(test_data_dir)
# 2. Run tests
test_stdout_exit(f"{test_program} example_input-compare_goa.csv", "example_input-compare_goa.csv.expected", 0)
# Test parsing of stdin
# test_exit_status(f"cat example_input-compare_goa.csv | {test_program}", 0)
# Test exit status for a bad command line invocation
test_exit_status(f"{test_program} --this_is_not_a_valid_argument", 2)
# Test exit status for a non existent input FASTA file
test_exit_status(f"{test_program} this_file_does_not_exist.fasta", 2)


# 3. End of testing - check if any errors occurred
if num_errors > 0:
    print(f"{test_program} failed {num_errors} out of {num_tests} tests")
    exit(1)
else:
    print(f"{test_program} passed all {num_tests} tests successfully")
    exit(0)
