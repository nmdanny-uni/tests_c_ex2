# Introduction & Features

These tests were originally made by Nadav Har Tuv (nadav.har-tuv1@mail.huji.ac.il) at the 2018-2019 summer course of
C/C++ workshop, obtained from the [CS-DB](https://drive.google.com/open?id=1B8C1V1gayvntPHvv69T6dbo5BacXdE__) (HUJI mail
required to access), and modified by me 

Some of the new features included:

* Using pytest to setup test infrastructure, this allows using PyCharm's nice test runner to know which
  tests ran, which succeeded, which failed, and use PyCharm's built-in diffing tool.
  
* Generated many valid trees with pictures

* Can now update school outputs automatically via school solution, when on a HUJI system
  
* Runs your executable via 'valgrind', reporting valgrind errors (Linux systems only)

* Disabled 'no tree' tests, as we can assume that all valid graphs are valid trees.
  (For future courses, you can re-enable them by removing the `@unittest.skip` annotation)


# Requirements
Supported systems:
- Linux (Guaranteed to work in the Aquarium)
- Windows only if compiling using the MinGW or MSVC toolchains, and **NOT CYGWIN**.

  See [this tutorial](https://www.jetbrains.com/help/clion/quick-tutorial-on-configuring-clion-on-windows.html#MinGW) 
  for setting up a MinGW toolchain on Windows.
- Haven't tested on OSX, but theoretically should work

Required software(already included in the Aquarium PCs)
- Python 3.7 or higher
- The 'pytest' library(install via `python3 -m pip install --user pytest`)

If you wish to use `graph_generator` (There's no need, as I've already included
plenty of generated graphs), you'll need the following(already included in Aquarium PCs):
- The `dot` program, part of the `graphviz` package on Ubuntu. Google for
  instructions on setting these up on Windows or other OSes.
- The following python libraries(install via pip like before):
  - `networkx`
  - `matplotlib`
  - `pydot`
  - `hypothesis`

# Installation

Type these in your terminal/powershell

```shell
cd PATH_TO_YOUR_EX2_PROJECT/
git clone https://github.cs.huji.ac.il/danielkerbel/tests_c_ex2/ tests
```

If this is your first time using git, you may need to type your CSE user credentials.

Afterwards, your project directory should look like this(assuming you're using CLion)


```
ex2/
ex2/TreeAnalyzer.C
ex2/tests/
ex2/tests/tester.py
ex2/tests/tester_files/
ex2/cmake-build-debug/
ex2/cmake-build-debug/TreeAnalyzer  (or TreeAnalyzer.exe on Windows)
```

The `cmake-build-debug` folder is where CLion compiles your project by default, but you can also compile there manually
via the terminal(Linux only):

```
cd PATH_LEADING_TO_EX2/ex2/cmake-build-debug
cmake .. && make
```

**Remember to recompile your C project if you made changes to your program and want to test them**

# Running

I recommend using PyCharm's test runner to run the tests, as it will give you
prettier output and allow differentiating between subtests easily.

## Running via PyCharm

- Open a PyCharm project at the `tests` folder
- Add a unittests test configuration via: `Run | Edit Configurations | + | Python tests | pytest`
- Fill the following fields:
   
   - Target: `module name`
   - Target - `tester`
   - Python interpreter - `Python 3.7` (or higher)
    

## Running via terminal

To run via terminal, type `python3 -m pytest tester.py`

You can pass arguments like `-k genereated` to run only only tests on generated
trees, or `-vv` to display test progress

# Options

There are several things you can enable/disable in the tests, by
changing the constants at the beginning of `tester.py`, such as whether to use
valgrind or not, whether to ignore newline differences, or update outputs from
school solution when running on HUJI.

# Generating graphs

Also included is a graph generator. I've only tested it in a HUJI system, it requires
several libraries and software (see [requirements](#requirements))
To run, simply type `python3 -m pytest graph_generator.py`. You'll probably want to
generate output files from a HUJI system, by running `python3 -m pytest tester.py` afterwards
(with the `UPDATE_SCHOOL_FILES` option enabled)


