
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

        # grab relevant options
        self._include_l3_cache = options.include_l3_cache
        
        # Instantiate CPU
        if options.cpu_type == 'MinorCPU':
            self.cpu = MinorCPU()
        elif options.cpu_type == 'O3CPU':
            self.cpu = O3CPU()

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

        # create L2 and L3 Cache Buses
        self.l2bus = L2XBar()
        if self._include_l3_cache:
            self.l3bus = L3XBar()

        # connect L2 Cache to the processor
        self.cpu.icache.connectBus(self.l2bus)
        self.cpu.dcache.connectBus(self.l2bus)

        # create L2 and L3 caches
        self.l2cache = L2Cache(options)
        if self._include_l3_cache:
            self.l3cache = L3Cache(options)

        # hook up L2 and L3 buses
        self.l2cache.connectCPUSideBus(self.l2bus)
        if self._include_l3_cache:
            self.l2cache.connectMemSideBus(self.l3bus)
            self.l3cache.connectCPUSideBus(self.l3bus)

    # Connect processor to a bus
    def connectProcessor(self, bus):

        if self._include_l3_cache:
            self.l3cache.connectMemSideBus(bus)
        else:
            self.l2cache.connectMemSideBus(bus)
    
    # Connect interrupts to memory (x86 only)
    def connectInterruptsToMem(self, membus):

        self.cpu.interrupts[0].pio = membus.mem_side_ports
        self.cpu.interrupts[0].int_requestor = membus.cpu_side_ports
        self.cpu.interrupts[0].int_responder = membus.mem_side_ports
    
    # add a workload to the Processor
    def addWorkload(self, process):

        self.cpu.workload = process
        self.cpu.createThreads()