
# --------------------------------------------------------------------------
# Import Libraries
# --------------------------------------------------------------------------
import m5
from m5.objects import *

from caches import *

# --------------------------------------------------------------------------
# Processor Class
# --------------------------------------------------------------------------
class Processor(SubSystem):
    
    # Constructor
    def __init__(self, options):

        super(Processor, self).__init__()
        
        # Instatntiate CPU
        self.cpu = MinorCPU()

        # configure the CPU
        if options.thread_policy:
            system.cpu.threadPolicy = options.thread_policy

        if options.decode_input_buffer_size:
            system.cpu.decodeInputBufferSize = options.decode_input_buffer_size

        if options.fetch1_to_fetch2_forward_delay:
            system.cpu.fetch1ToFetch2ForwardDelay = options.fetch1_to_fetch2_forward_delay
    
        # create the L1 caches
        self.cpu.icache = L1ICache(options)
        self.cpu.dcache = L1DCache(options)

        # connect the L1 Caches to the CPU
        self.cpu.icache.connectCPU(self.cpu)
        self.cpu.dcache.connectCPU(self.cpu)

        # create interrupt controller
        self.cpu.createInterruptController()

    # Connect processor to a bus
    def connectProcessor(self, bus):

        self.cpu.icache.connectBus(bus)
        self.cpu.dcache.connectBus(bus)
    
    # Connect interrupts to memory (x86 only)
    def connectInterruptsToMem(self, membus):

        self.cpu.interrupts[0].pio = membus.mem_side_ports
        self.cpu.interrupts[0].int_requestor = membus.cpu_side_ports
        self.cpu.interrupts[0].int_responder = membus.mem_side_ports
    
    # add a workload to the Processor
    def addWorkload(self, process):

        self.cpu.workload = process
        self.cpu.createThreads()