import subprocess
import sys
from unittest import TestCase
from os import listdir
from os import path, makedirs, rmdir
from os.path import isfile, join, isdir, exists


#######################################################################################################################
# You may need to change this, depending on where you placed the tests
#######################################################################################################################

# this assumes your project structure is as follows:
# ex2/
# ex2/tests
# ex2/tests/tester.py
# ex2/tests/tester_files
# ex2/cmake-build-debug/
# ex2/cmake-build-debug/TreeAnalyzer
# (If using CLion, the 'cmake-build-debug' folder should be created automatically)
PATH_TO_EXECUTABLE_FOLDER = "../cmake-build-debug/"

# You can also compile via gcc, by running the following in the terminal:
# cd <TYPE THE PATH TO ex2 FOLDER>
# mkdir cmake-build-debug
# cd cmake-build-debug
# cmake .. && make


#######################################################################################################################
# You shouldn't have to modify anything below this line in order to run the tests
#######################################################################################################################

EXECUTABLE_NAME = "TreeAnalyzer"
if sys.platform == "win32":
    EXECUTABLE_NAME += ".exe"

path_to_compiled_files = path.join(PATH_TO_EXECUTABLE_FOLDER, EXECUTABLE_NAME)

if not isfile(path_to_compiled_files):
    print(f"Couldn't find the TreeAnalyzer executable at \"{path_to_compiled_files}\"\n"
          f"Either you didn't compile it or you didn't configure the path at the python file \"{__file__}\"",
          file=sys.stderr)
    sys.exit(-1)


# paths to files and folder
# these shouldn't need any changes
name_of_good = "good_trees"
name_of_invalid_trees = "invalid_trees"
name_of_no_tree = "no_trees"

path_to_test_files = path.join("tester_files")
path_to_good_trees = path.join(path_to_test_files, name_of_good)
path_to_invalid_trees = path.join(path_to_test_files, name_of_invalid_trees)
path_to_no_trees = path.join(path_to_test_files, name_of_no_tree)

path_to_system_out = path.join(path_to_test_files, "system_out")

name_of_school_solution_output_no_folder = "_school_solution" + "_output" + ".txt"
name_of_school_solution_errors_no_folder = "_school_solution" + "_errors" + ".txt"

invalid_file = "invalid.txt"
no_tree_file = "no_tree.txt"
num_of_parm_file = "num_of_parm.txt"

simple_path = path.join(path_to_good_trees, "simple.txt")

invalid = {
    "no_int_num_first": simple_path + " 1.1 2",
    "no_int_num_sec": simple_path + " 1 2.5",
    "char_in_num_1": simple_path + " 2g 4",
    "char_in_num_2": simple_path + " 2 m3",
    "neg_num_1": simple_path + " -2 6",
    "neg_num_2": simple_path + " 2 -6",
    "big_num_1": simple_path + " 8 3",


}

def path_to(name_of_file):
    return path.join(path_to_good_trees, name_of_file)

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

    "one_kodkod" : path_to("one_kodkod.txt") + " 0 0"
}


num_of_parm = {
    "les_parm": simple_path + " 1",
    "more_parm": simple_path + " 1 2 3",
    "no_file": "1 3"
}


def run_with_cmd(command_list, str=""):
    """
    Execute the given command list with the command line
    Return a tuple containing the return code, output and errors.
    """

    process = subprocess.run(command_list, shell=False, input=str,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True)
    return process.returncode, process.stdout, process.stderr


tests_invalid_trees = [t for t in listdir(path_to_invalid_trees)]
tests_no_tree = [t for t in listdir(path_to_no_trees)]

number_of_tests = len(num_of_parm) + len(invalid) + len(tests_invalid_trees) + len(tests_no_tree) +len(valid)


class Tester(TestCase):

    """ Whether to strip newlines(Windows/Linux) when comparing strings for equality """
    __ignore_newlines: bool

    def setUp(self) -> None:
        self.__ignore_newlines = True

    def __clean_string(self, s: str) -> str:
        """ If 'ignore_newlines' is enabled, strips newlines from given string,
            otherwise doesn't change it."""
        if self.__ignore_newlines:
            return s.rstrip('\r\n')
        return s

    def test_invalid_number_of_parameters(self):
        for name in num_of_parm:
            with self.subTest(name=num_of_parm[name], file=num_of_parm_file):
                self.run_one_invalid_test(num_of_parm[name], num_of_parm_file)

    def test_invalid_parameters(self):
        for name in invalid:
            with self.subTest(name=invalid[name], file=invalid_file):
                self.run_one_invalid_test(invalid[name], invalid_file)

    def test_invalid_tree_files(self):
        for name in tests_invalid_trees:
            name = path.join(path_to_invalid_trees, name) + " 1 2"
            with self.subTest(name=name, file=invalid_file):
                self.run_one_invalid_test(name, invalid_file)

    def test_check_non_graph_trees(self):
        for name in tests_no_tree:
            name = path.join(path_to_no_trees, name) + " 1 2"
            with self.subTest(name=name, file=no_tree_file):
                self.run_one_invalid_test(name, no_tree_file)

    def test_valid_trees(self):
        for name in valid:
            with self.subTest(name=name, file=valid[name]):
                self.run_one_good_test(name, valid[name])

    def run_one_invalid_test(self, parm, error):
        name_of_school_solution_output = "empty.txt"
        name_of_school_solution_errors = error

        path_to_school_solution_output = path.join(path_to_system_out,
                                                   name_of_school_solution_output)
        path_to_school_solution_errors = path.join(path_to_system_out,
                                                   name_of_school_solution_errors)

        command_list = [path_to_compiled_files] + parm.split()
        code, user_output, user_errors = run_with_cmd(command_list)

        user_output, user_errors = self.__clean_string(user_output), self.__clean_string(user_errors)

        with open(path_to_school_solution_output) as file:
            school_output = self.__clean_string(file.read())

        with open(path_to_school_solution_errors) as file:
            school_error = self.__clean_string(file.read())

        self.assertEquals(user_output, school_output.strip('\r\n'), "Your STDOUT doesn't match school's STDOUT")
        self.assertEquals(school_error, user_errors.strip('\r\n'), "Your STDERR doesn't match school's STDERR")

    def run_one_good_test(self, name_of_test, parm):
        path_to_school_solution_output = path.join(path_to_system_out,
                                                   name_of_test + name_of_school_solution_output_no_folder)
        path_to_school_solution_errors = path.join(path_to_system_out, "empty.txt")

        command_list = [path_to_compiled_files] + parm.split()
        code, user_output, user_errors = run_with_cmd(command_list)  # run your code

        user_output, user_errors = self.__clean_string(user_output), self.__clean_string(user_errors)

        with open(path_to_school_solution_output) as file:
            school_output = self.__clean_string(file.read())

        with open(path_to_school_solution_errors) as file:
            school_error = self.__clean_string(file.read())

        self.assertEquals(user_output, school_output, "Your STDOUT doesn't match school's STDOUT")
        self.assertEquals(school_error, user_errors, "Your STDERR doesn't match school's STDERR")
