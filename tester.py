import subprocess
import sys
import random
from pathlib import Path
from os import listdir
from os import path, makedirs, rmdir
from os.path import isfile, join, isdir, exists
from tempfile import NamedTemporaryFile
from shutil import which
import pytest
import re

#######################################################################################################################
# You may need to change this, depending on where you placed the tests
# See README for information
#######################################################################################################################

# Use the executable built via CLion
PATH_TO_EXECUTABLE_FOLDER = "../cmake-build-debug/"

# If system has valgrind available, use it to ensure your program has no memory leaks.
# On Windows/other systems with no 'valgrind' in path, this doesn't do anything.
USE_VALGRIND_IF_AVAILABLE = True

# Ignore trailing newlines at end of each line when comparing strings
# A proper solution should handle them correctly, but you can temporarily enable this for debugging
IGNORE_NEWLINES = False

# Tries updating the school files if we're on a HUJI system.
UPDATE_SCHOOL_FILES = True

# Correct for 2019-2020 semester A course
SCHOOL_EXECUTABLE_PATH = "/cs/course/current/labcc/www/c_ex2/TreeAnalyzer"

#######################################################################################################################
# You shouldn't have to modify anything below this line in order to run the tests
#######################################################################################################################

ON_HUJI = exists(SCHOOL_EXECUTABLE_PATH)

EXECUTABLE_NAME = "TreeAnalyzer"
if sys.platform == "win32":
    EXECUTABLE_NAME += ".exe"

PATH_TO_EXECUTABLE = path.join(PATH_TO_EXECUTABLE_FOLDER, EXECUTABLE_NAME)
PATH_TO_TESTER_DIR = path.join("tester_files")
PATH_TO_VALID_TREES = path.join(PATH_TO_TESTER_DIR, 'good_trees')
PATH_TO_INVALID_GRAPHS = path.join(PATH_TO_TESTER_DIR, 'invalid_graphs')
PATH_TO_NON_TREE_GRAPHS = path.join(PATH_TO_TESTER_DIR, 'no_trees')
PATH_TO_GENERATED_GRAPHS = path.join(PATH_TO_TESTER_DIR, 'generated')

PATH_TO_EXPECTED_OUTPUTS = path.join(PATH_TO_TESTER_DIR, "system_out")

name_of_school_solution_output_no_folder = "_school_solution" + "_output" + ".txt"
name_of_school_solution_errors_no_folder = "_school_solution" + "_errors" + ".txt"

invalid_file = "invalid.txt"
empty_file = "empty.txt"
no_tree_file = "no_tree.txt"
num_of_parm_file = "num_of_parm.txt"

simple_path = path.join(PATH_TO_VALID_TREES, "simple.txt")

invalid_params = {
    "no_int_num_first": simple_path + " 1.1 2",
    "no_int_num_sec": simple_path + " 1 2.5",
    "char_in_num_1": simple_path + " 2g 4",
    "char_in_num_2": simple_path + " 2 m3",
    "neg_num_1": simple_path + " -2 6",
    "neg_num_2": simple_path + " 2 -6",
    "big_num_1": simple_path + " 8 3"

}


def path_to(name_of_file):
    return path.join(PATH_TO_VALID_TREES, name_of_file)


valid = {
    "simple_1": simple_path + " 4 5",
    "simple_2": simple_path + " 7 2",

    "normal_1_1": path_to("normal_tree_1.txt") + " 1 13",
    "normal_1_2": path_to("normal_tree_1.txt") + " 9 13",
    "normal_1_3": path_to("normal_tree_1.txt") + " 3 3",
    "normal_1_4": path_to("normal_tree_1.txt") + " 11 10",
    "normal_1_5": path_to("normal_tree_1.txt") + " 2 6",

    "long_1": path_to("long.txt") + " 7 10",
    "long_2": path_to("long.txt") + " 8 2",
    "long_3": path_to("long.txt") + " 10 3",
    "long_4": path_to("long.txt") + " 2 10",

    "big_1": path_to("big_tree.txt") + " 2 10",
    "big_2": path_to("big_tree.txt") + " 30 23",
    "big_3": path_to("big_tree.txt") + " 0 19",
    "big_4": path_to("big_tree.txt") + " 15 29",
    "big_5": path_to("big_tree.txt") + " 7 27",

    "one_kodkod": path_to("one_kodkod.txt") + " 0 0"
}

num_of_parm = {
    "les_parm": simple_path + " 1",
    "more_parm": simple_path + " 1 2 3",
    "no_file": "1 3"
}


def update_school_files(command_list, school_stdout_file, school_stderr_file):
    """ Given an argument list of a TreeAnalyzer call, performs that call on
        the school's solution, updating the corresponding school output files in system_out """
    command_list = command_list.copy()
    command_list[0] = SCHOOL_EXECUTABLE_PATH
    code, out, err, valgrind = run_with_cmd(command_list, valgrind=False)

    with open(school_stdout_file, 'w') as stdout_file:
        stdout_file.write(out)

    with open(school_stderr_file, 'w') as stderr_file:
        stderr_file.write(err)


def run_with_cmd(command_list, str="", valgrind=False):
    """
    Execute the given command list with the command line
    Return a tuple containing the return code, output, errors and valgrind output
    """
    valgrind_outfile, valgrind_output = None, ""
    if valgrind:
        valgrind_outfile = NamedTemporaryFile(mode='r+', encoding='utf-8')
        command_list = ['valgrind', '--leak-check=yes', f'--log-file={valgrind_outfile.name}'] + command_list

    print(f"Running command \"{' '.join(command_list)}\"")
    try:
        process = subprocess.run(command_list, shell=False, input=str,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True)

        if valgrind:
            valgrind_outfile.seek(0)
            valgrind_output = valgrind_outfile.read()
            valgrind_outfile.close()

        return process.returncode, process.stdout, process.stderr, valgrind_output
    except Exception as e:
        print(f"Error while running subprocess: {e}")
        sys.exit(-1)


def clean_string(s: str) -> str:
    """ If 'ignore_newlines' is enabled, strips newlines from given string,
         otherwise doesn't change it."""
    if IGNORE_NEWLINES:
        return s.rstrip('\r\n')
    return s


@pytest.mark.parametrize("param_name", list(num_of_parm.values()))
def test_invalid_parameter_count(param_name: str):
    run_one_invalid_test(param_name, num_of_parm_file)


@pytest.mark.parametrize("params", invalid_params.values())
def test_invalid_parameter(params: str):
    run_one_invalid_test(params, invalid_file)


@pytest.mark.parametrize("file_name", list(listdir(PATH_TO_INVALID_GRAPHS)))
def test_invalid_graph(file_name: str):
    full_path = path.join(PATH_TO_INVALID_GRAPHS, file_name) + " 1 2"
    run_one_invalid_test(full_path, invalid_file)


@pytest.mark.skip("Not relevant for this semester")
@pytest.mark.parametrize("path", list(listdir(PATH_TO_NON_TREE_GRAPHS)))
def test_valid_graph_not_a_tree(path: str):
    run_one_invalid_test(path, no_tree_file)


@pytest.mark.parametrize("test_name", valid.keys(), ids=list(valid.values()))
def test_valid_tree(test_name: str):
    run_one_good_test(test_name, valid[test_name])


@pytest.mark.parametrize("txt_path", [Path(PATH_TO_GENERATED_GRAPHS) / f for f in map(Path, listdir(PATH_TO_GENERATED_GRAPHS))
                                      if f.stem.startswith('valid') and f.name.endswith('.txt')],
                         ids=lambda path: str(path.stem))
def test_valid_generated(txt_path: Path):
    name = txt_path.stem
    elements = name.split('-')
    node_count = int(elements[1])
    school_out_path = txt_path.with_suffix('.expected_out')
    school_err_path = txt_path.with_suffix('.expected_stderr')
    if UPDATE_SCHOOL_FILES:
        # randomly generate valid 'from' and 'to' parameters
        from_node = random.randint(0, node_count - 1)
        to_node = random.randint(0, node_count - 1)
        command_list = [PATH_TO_EXECUTABLE, str(txt_path), str(from_node), str(to_node)]
        with open(school_out_path, 'w') as expected_out,\
             open(school_err_path, 'w') as expected_err:
            update_school_files(command_list, expected_out.name, expected_err.name)
    elif not (school_out_path.exists() and school_err_path.exists()):
        pytest.skip(f"Couldn't find generated school output/error files for {txt_path}, skipping.")
        return
    else:
        # find the 'from' and 'to' parameters for this test
        with open(school_out_path, 'r') as out_file:
            out_st = out_file.read()
            match = re.search(r"Shortest Path Between (\d+) and (\d+)", out_st)
            if match:
                from_node = match.group(1)
                to_node = match.group(2)
            else:
                from_node = to_node = "0"
        command_list = [PATH_TO_EXECUTABLE, str(txt_path), from_node, to_node]

    run_test(command_list, school_out_path, school_err_path)


def run_test(command_list, school_out_path, school_err_path):
    """ Runs a test, """
    if UPDATE_SCHOOL_FILES:
        update_school_files(command_list, school_out_path, school_err_path)

    code, user_output, user_errors, valgrind_out = run_with_cmd(command_list, valgrind=USE_VALGRIND_IF_AVAILABLE)
    user_output, user_errors = clean_string(user_output), clean_string(user_errors)

    with open(school_out_path) as file:
        school_output = clean_string(file.read())

    with open(school_err_path) as file:
        school_error = clean_string(file.read())

    success = len(school_error) == 0

    ensure_match(command_list, user_output, user_errors, school_output, school_error)
    ensure_valgrind_output_ok(valgrind_out)
    if success:
        assert code == 0, "On success, program should return 0"
    else:
        assert code == 1, "On failure, program should return 1"


def run_one_invalid_test(parm, error):
    name_of_school_solution_output = "empty.txt"
    name_of_school_solution_errors = error

    path_to_school_solution_output = path.join(PATH_TO_EXPECTED_OUTPUTS,
                                               name_of_school_solution_output)
    path_to_school_solution_errors = path.join(PATH_TO_EXPECTED_OUTPUTS,
                                               name_of_school_solution_errors)
    command_list = [PATH_TO_EXECUTABLE] + parm.split()
    run_test(command_list, path_to_school_solution_output, path_to_school_solution_errors)


def run_one_good_test(name_of_test, parm):
    path_to_school_solution_output = path.join(PATH_TO_EXPECTED_OUTPUTS,
                                               name_of_test + name_of_school_solution_output_no_folder)
    path_to_school_solution_errors = path.join(PATH_TO_EXPECTED_OUTPUTS, "empty.txt")
    command_list = [PATH_TO_EXECUTABLE] + parm.split()
    run_test(command_list, path_to_school_solution_output, path_to_school_solution_errors)


def ensure_match(command_list, user_output, user_errors, school_output, school_error):
    command = " ".join(command_list)
    big_separator = "*" * 80
    separator = "-" * 40
    msg = (f"{big_separator}\n"
           f"Your STDOUT:\n"
           f"{user_output}\n"
           f"{separator}\n"
           f"Your STDERR:\n"
           f"{user_errors}\n"
           f"{separator}\n"
           f"School STDOUT:\n"
           f"{school_output}\n"
           f"{separator}\n"
           f"School STDERR:\n"
           f"{school_error}\n"
           f"{big_separator}")

    print(f"Testing command \"{command_list}\"\n{msg}")
    assert user_output == school_output, f"STDOUT mismatch while running command {command}"
    assert user_errors == school_error, f"STDERR mismatch while running command {command}"


def ensure_valgrind_output_ok(valgrind_out: str):
    if not valgrind_out:
        return
    assert "ERROR SUMMARY: 0" in valgrind_out, (f"There were 1 or more errors detected by valgrind:\n"
                                                f"{valgrind_out}")


def initialize():
    global IGNORE_NEWLINES, USE_VALGRIND_IF_AVAILABLE, UPDATE_SCHOOL_FILES

    if not isfile(PATH_TO_EXECUTABLE):
        print(f"Couldn't find the TreeAnalyzer executable at \"{PATH_TO_EXECUTABLE}\"\n"
              f"Either you didn't compile it or you didn't configure the path at the python file \"{__file__}\"",
              file=sys.stderr)
        sys.exit(-1)
    else:
        if sys.platform == "win32":
            with open(PATH_TO_EXECUTABLE, 'rb') as exe_file:
                binary = exe_file.read()
                for match in re.finditer(b"[^\\x00-\\x1F\\x7F-\\xFF]{4,}", binary):
                    if b"cygwin1.dll" == match.group(0):
                        print(".exe was compiled via Cygwin which is unsupported"
                              " by these tests - use a MSVC/MinGW toolchain instead,"
                              " or use a Linux system.", file=sys.stderr)
                        sys.exit(-1)

    if IGNORE_NEWLINES:
        print("Running tests while ignoring newline differences. Your program should run successfully "
              "without them", file=sys.stderr)

    if USE_VALGRIND_IF_AVAILABLE and not which('valgrind'):
        print("No 'valgrind' executable was found in PATH, tests will be run without it.\n"
              "HUJI systems should have 'valgrind' pre-installed. Other Linux/OSX systems may require\n"
              " it to be manually installed. Windows has no valgrind(unless you use WSL)", file=sys.stderr)
        USE_VALGRIND_IF_AVAILABLE = False

    if UPDATE_SCHOOL_FILES and not ON_HUJI:
        print(f"UPDATE_SCHOOL_FILES is set, but couldn't find the school solution at {SCHOOL_EXECUTABLE_PATH}\n"
              f"Will be using the already included output files instead", file=sys.stderr)
        UPDATE_SCHOOL_FILES = False


if __name__ == '__main__':
    print(f"Run this via `python3 -m pytest tester.py`", file=sys.stderr)
    sys.exit(-1)
else:
    initialize()
