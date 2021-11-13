# --------------------------------------------------------------------------
# Libraries
# --------------------------------------------------------------------------
import m5
from m5.objects import *

from caches import *
from power import *
from processor import *

import argparse

# --------------------------------------------------------------------------
# Add Options
# --------------------------------------------------------------------------
# create parser object
parser = argparse.ArgumentParser(
    description = 'A simple system with 2-level cache.'
)

# add an argument for selecting the binary file.
parser.add_argument(
    '--binary',
    default = '', 
    nargs = '?', 
    type = str, 
    help = 'Path to the binary to execute.'
)

# add arguments for selecting cache sizes
parser.add_argument(
    '--l1i_size', 
    help = 'L1 instruction cache size. Default: 16kB.'
)
parser.add_argument(
    '--l1d_size', 
    help = 'L1 data cache size. Default: 64kB.'
)
parser.add_argument(
    '--l2_size', 
    help = 'L2 cache size. Default: 256kB.'
)

# add arguments for selecting cache data latencies
parser.add_argument(
    '--l1i_data_latency', 
    help = 'L1 instruction cache data latency. Default: 2'
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

# create options object
options = parser.parse_args()

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

# create an L2 Cache bus
system.l2bus = L2XBar()

# connect the processor's cache ports to the L2 Cache Bus
system.processor.connectProcessor(system.l2bus)

# create L2 cache and connect it to the L2 Cache Bus and the memory bus
system.l2cache = L2Cache(options)
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

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
#adding power modeling for the CPU
for cpu in system.descendants():
    if not isinstance(cpu, m5.objects.BaseCPU):
        continue
    cpu.power_state.default_state = 'ON'
    cpu.power_model = CpuPowerModel(cpu.path())

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
m5.stats.periodicStatDump(m5.ticks.fromSeconds(0.1E-3))

# kick off simulation
print('Beginning simulation!')
exit_event = m5.simulate()

# inspect state of the simulation after completion
print('Exiting @ tick {} because {}'.format(m5.curTick(), exit_event.getCause()))