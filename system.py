# --------------------------------------------------------------------------
# Libraries
# --------------------------------------------------------------------------
import m5
from m5.objects import *

from caches import *
from power import *
from processor import *

import argparse

from data_extraction import *

# --------------------------------------------------------------------------
# Add Options
# --------------------------------------------------------------------------
# create parser object
parser = argparse.ArgumentParser(
    description = 'A simple system with 2-level cache.'
)

# create empty list of CPU parameters for data extraction purposes
parameters = [[], []]

# add an argument for selecting the binary file.
parser.add_argument(
    '--binary',
    default = '', 
    nargs = '?', 
    type = str, 
    help = 'Path to the binary to execute.'
)

# add an argument for naming the .csv files
parser.add_argument(
    '--csv_file_suffix',
    default = '',
    type = str,
    help = 'String that is appended to the end of the .csv file names.'
)

# add an argument for a directory save loaction for the CSV files
parser.add_argument(
    '--csv_save_dir',
    default = '',
    type = str,
    help = 'Location to save the CSV files containing the extracted data.'
)

# add arguments for selecting cache sizes
parameters[0].append("L1 Instruction Cache Size")
parser.add_argument(
    '--l1i_size', 
    default = '16kB',
    help = 'L1 instruction cache size. Default: 16kB.'
)
parameters[0].append("L1 Data Cache Size")
parser.add_argument(
    '--l1d_size',
    default = '64kB',
    help = 'L1 data cache size. Default: 64kB.'
)
parameters[0].append("L2 Cache Size")
parser.add_argument(
    '--l2_size',
    default = '256kB',
    help = 'L2 cache size. Default: 256kB.'
)
parameters[0].append("L3 Cache Size")
parser.add_argument(
    '--l3_size',
    default = '1MB',
    help = 'L3 cache size. Default: 1MB.'
)

# add arguments for selecting cache associativity
parameters[0].append("L1 Instruction Cache Associativity")
parser.add_argument(
    '--l1i_assoc',
    default = 2,
    help = 'L1 data cache associativity. Default: 2.'
)
parameters[0].append("L1 Data Cache Associativity")
parser.add_argument(
    '--l1d_assoc',
    default = 2,
    help = 'L1 instruction cache associativity. Default: 2.'
)
parameters[0].append("L2 Cache Associativity")
parser.add_argument(
    '--l2_assoc',
    default = 8,
    help = 'L2 cache associativity. Default: 8.'
)
parameters[0].append("L3 Cache Associativity")
parser.add_argument(
    '--l3_assoc',
    default = 64,
    help = 'L3 cache associativity. Default: 64.'
)

# add arguments for selecting cache data latencies
parameters[0].append("L1 Instruction Cache Data Latency")
parser.add_argument(
    '--l1i_data_latency', 
    default = 2,
    help = 'L1 instruction cache data latency. Default: 2'
)

# add argument for selecting the CPU type
parameters[0].append("CPU Type")
parser.add_argument(
    '--cpu_type',
    default = 'MinorCPU',
    help = 'Selects the processor type.'
)

# add arguments for configuring the CPU
parser.add_argument(
    '--thread_policy', 
    help = 'Thread scheduling policy for the MinorCPU.'
)
parser.add_argument(
    '--decode_input_buffer_size', 
    help = 'Size of input buffer to decode in cycle-worth of instructions.'
)
parser.add_argument(
    '--fetch1_to_fetch2_forward_delay', 
    help = 'Forward cycle delay from Fetch1 to Fetch2.'
)

# add argument for including L3 Cache.
parser.add_argument(
    '--include_l3_cache',
    default = False,
    help = 'Determines whether the L3 cache should be included on not. Options: True | False. Default: False.'
)

# add arguments for selecting the pwer modeling equations for the CPU and
# L2 and L3 caches.
parser.add_argument(
    '--cpu_pwr_eq',
    default = 0,
    help = 'Selects the equation to use for modeling the processor\'s power consumption. Input is a positive integer.'
)
parser.add_argument(
    '--l2_pwr_eq',
    default = 0,
    help = 'Selects the equation to use for modeling the L2 cache\'s power consumption. Input is a positive integer.'
)
parser.add_argument(
    '--l3_pwr_eq',
    default = 0,
    help = 'Selects the equation to use for modeling the L3 cache\'s power consumption. Input is a positive integer.'
)

# create options object
options = parser.parse_args()

# place options in the parameter list
parameters[1] = [
    options.l1i_size,
    options.l1d_size,
    options.l2_size,
    options.l3_size,
    options.l1i_assoc,
    options.l1d_assoc,
    options.l2_assoc,
    options.l3_assoc,
    options.l1i_data_latency,
    options.cpu_type
]

# --------------------------------------------------------------------------
# Create Architecture
# --------------------------------------------------------------------------
# create the system
system = System()

# create a clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain(voltage = '1.0V')

# create the processor
system.processor = Processor(options)

# set up the memory
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('8GB')]

# create the memory bus
system.membus = SystemXBar()

# connect the processor's cache ports to memory
system.processor.connectProcessor(system.membus)

# For x86 only, make sure the interrupts are connected to the memory
# Note: these are directly connected to the memory bus and are not cached
if m5.defines.buildEnv['TARGET_ISA'] == 'x86':
    system.processor.connectInterruptsToMem(system.membus)

# connect the system to the memory bus
system.system_port = system.membus.cpu_side_ports

# create a memory controller and add it to the memory bus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# ---------------------------------------------------------------------------------
# Add Power Modeling
# ---------------------------------------------------------------------------------
# adding power modeling for the CPU
system.processor.cpu.power_state.default_state = 'ON'
system.processor.cpu.power_model = CpuPowerModel('system.processor.cpu', options)

# add power modeling for the L2 Cache
system.processor.l2cache.power_state.default_state = "ON"
system.processor.l2cache.power_model = L2PowerModel('system.processor.l2cache', options)

# add power modeling for the L3 Cache
if options.include_l3_cache:
    system.processor.l3cache.power_state.default_state = "ON"
    system.processor.l3cache.power_model = L3PowerModel('system.processor.l3cache', options)

# ---------------------------------------------------------------------------------
# Run Binary File
# ---------------------------------------------------------------------------------
# grab finename and path of the binary file to run
system.workload = SEWorkload.init_compatible(options.binary)

# create the process, set the process command, then tell the CPU to use the process
process = Process()
process.cmd = [options.binary]
system.processor.addWorkload(process)

# instantiate the system
root = Root(full_system = False, system = system)
m5.instantiate()

# dump stats periodically
stats_dump_period = 0.1E-3
m5.stats.periodicStatDump(m5.ticks.fromSeconds(stats_dump_period))

# kick off simulation
print('Beginning simulation!')
exit_event = m5.simulate()

# inspect state of the simulation after completion
exiting_tick = m5.curTick()
print('Exiting @ tick {} because {}'.format(exiting_tick, exit_event.getCause()))

# ---------------------------------------------------------------------------------
# Extract Statistics
# ---------------------------------------------------------------------------------
# read statistics file
print('Extracting statistics...')
statistics = DataExtraction(exiting_tick, stats_dump_period)

# create .csv file names
cpu_power_filename = '{}/cpu_power_data_{}.csv'.format(options.csv_save_dir, options.csv_file_suffix)
l2_cache_power_filename = '{}/l2_cache_power_data_{}.csv'.format(options.csv_save_dir, options.csv_file_suffix)
if options.include_l3_cache:
    l3_cache_power_filename = '{}/l3_cache_power_data_{}.csv'.format(options.csv_save_dir, options.csv_file_suffix)

# extract power modeling data
statistics.ExtractCpuPowerData(parameters, cpu_power_filename)
statistics.ExtractL2CachePowerData(parameters, l2_cache_power_filename)
if options.include_l3_cache:
    statistics.ExtractL3CachePowerData(parameters, l3_cache_power_filename)