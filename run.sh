#!bin/bash

# --------------------------------------------------------------------------
# This script runs all of the tests for the power modeling project
# Assumes the following:
#   The project is stored in the directory configs/project within the gem5 directory
#   This script is ran from within the gem5/configs/project directory
# --------------------------------------------------------------------------

project_dir="configs/project"

# --------------------------------------------------------------------------
# Build C program
# --------------------------------------------------------------------------
echo "Building C Program for ARM Architecture..."
aarch64-linux-gnu-gcc -O0 -ggdb3 -std=c99 -static -o stress_test_ARM stress_test/stress_test.c
echo "Building C Program for X86 Architecture..."
gcc -O0 -ggdb3 -std=c99 -static -o stress_test_X86 stress_test/stress_test.c

# --------------------------------------------------------------------------
# Change Directory to gem5
# --------------------------------------------------------------------------
cd ../..

# --------------------------------------------------------------------------
# First Test
# --------------------------------------------------------------------------
echo "Running test 1 of 6"

test1_dir="$project_dir/test1"

if [ ! -d "$test1_dir" ]
then
    echo "Creating directory for test 1"
    mkdir "$test1_dir"
fi

build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l2_size=512kB --csv_file_suffix=without_l3_cache --csv_save_dir=$test1_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l2_size=256kB --include_l3_cache=True --csv_file_suffix=with_l3_cache --csv_save_dir=$test1_dir

echo "Test 1 of 6 complete"
echo ""

# --------------------------------------------------------------------------
# Second Test
# --------------------------------------------------------------------------
echo "Running test 2 of 6"

test2_dir="$project_dir/test2"

if [ ! -d "$test2_dir" ]
then
    echo "Creating directory for test 2"
    mkdir "$test2_dir"
fi

build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --csv_file_suffix=ARM --csv_save_dir=$test2_dir
build/X86/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_X86 --csv_file_suffix=X86 --csv_save_dir=$test2_dir

echo "Test 2 of 6 complete"
echo ""

# --------------------------------------------------------------------------
# Third Test
# --------------------------------------------------------------------------
echo "Running test 3 of 6"

test3_dir="$project_dir/test3"

if [ ! -d "$test3_dir" ]
then
    echo "Creating directory for test 3"
    mkdir "$test3_dir"
fi

build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=4kB  --l1d_size=16kB  --l2_size=256kB --csv_file_suffix=L1_16kB  --csv_save_dir=$test3_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=8kB  --l1d_size=32kB  --l2_size=256kB --csv_file_suffix=L1_32kB  --csv_save_dir=$test3_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=16kB --l1d_size=64kB  --l2_size=256kB --csv_file_suffix=L1_64kB  --csv_save_dir=$test3_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=32kB --l1d_size=128kB --l2_size=256kB --csv_file_suffix=L1_128kB --csv_save_dir=$test3_dir

build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=16kB --l1d_size=32kB  --l2_size=64kB  --csv_file_suffix=L2_64kB  --csv_save_dir=$test3_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=16kB --l1d_size=32kB  --l2_size=128kB --csv_file_suffix=L2_128kB --csv_save_dir=$test3_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=16kB --l1d_size=32kB  --l2_size=256kB --csv_file_suffix=L2_256kB --csv_save_dir=$test3_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_size=16kB --l1d_size=32kB  --l2_size=512kB --csv_file_suffix=L2_512kB --csv_save_dir=$test3_dir

echo "Test 3 of 6 complete"
echo ""

# --------------------------------------------------------------------------
# Fourth Test
# --------------------------------------------------------------------------
echo "Running test 4 of 6"

test4_dir="$project_dir/test4"

if [ ! -d "$test4_dir" ]
then
    echo "Creating directory for test 4"
    mkdir "$test4_dir"
fi

build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --cpu_type=MinorCPU --csv_file_suffix=MinorCPU --csv_save_dir=$test4_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --cpu_type=O3CPU    --csv_file_suffix=03CPU --csv_save_dir=$test4_dir

echo "Test 4 of 6 complete"
echo ""

# --------------------------------------------------------------------------
# Fifth Test
# --------------------------------------------------------------------------
echo "Running test 5 of 6"

test5_dir="$project_dir/test5"

if [ ! -d "$test5_dir" ]
then
    echo "Creating directory for test 5"
    mkdir "$test5_dir"
fi

echo "Test 5 is currently unimplemented. Skipping for now."

echo "Test 5 of 6 complete"
echo ""

# --------------------------------------------------------------------------
# Sixth Test
# --------------------------------------------------------------------------
echo "Running test 6 of 6"

test6_dir="$project_dir/test6"

if [ ! -d "$test6_dir" ]
then
    echo "Creating directory for test 6"
    mkdir "$test6_dir"
fi

build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=1 --l1d_assoc=4 --csv_file_suffix=L1i_assoc_1 --csv_save_dir=$test6_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=2 --l1d_assoc=4 --csv_file_suffix=L1i_assoc_2 --csv_save_dir=$test6_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=3 --l1d_assoc=4 --csv_file_suffix=L1i_assoc_3 --csv_save_dir=$test6_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=4 --l1d_assoc=4 --csv_file_suffix=L1i_assoc_4 --csv_save_dir=$test6_dir

build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=2 --l1d_assoc=2  --csv_file_suffix=L1d_assoc_2  --csv_save_dir=$test6_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=2 --l1d_assoc=4  --csv_file_suffix=L1d_assoc_4  --csv_save_dir=$test6_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=2 --l1d_assoc=8  --csv_file_suffix=L1d_assoc_8  --csv_save_dir=$test6_dir
build/ARM/gem5.opt $project_dir/system.py --binary=$project_dir/stress_test_ARM --l1i_assoc=2 --l1d_assoc=16 --csv_file_suffix=L1d_assoc_16 --csv_save_dir=$test6_dir

echo "Test 6 of 6 complete"
echo ""
