
# --------------------------------------------------------------------------------
# Import Libraries
# --------------------------------------------------------------------------------
from m5.objects import Cache
from m5.objects import CoherentXBar
from m5.objects import SnoopFilter
from m5.objects import SubSystem

# --------------------------------------------------------------------------------
# L1 Cache
# extend the BaseCache object to create an L1 cache by setting some of the
# parameters of BaseCache that do not have default values. 
# --------------------------------------------------------------------------------
class L1Cache(Cache):

    # parameters
    tag_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20

    # constructor
    def __init__(self, options = None):
        super(L1Cache, self).__init__()
        pass

    # raise a not implemented error if this function is not deined in a child
    # class.
    def connectCPU(self, cpu):
        raise NotImplementedError
    
    # connects a bus to the cache
    def connectBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# --------------------------------------------------------------------------------
# L1 Instruction Cache
# extend the L1Cache class to create an L1 Instruction Cache
# --------------------------------------------------------------------------------
class L1ICache(L1Cache):

    # paramters
    size = '16kB'
    assoc = 2
    data_latency = 2

    # constructor - sets cache size and data latency
    def __init__(self, options = None):

        super(L1ICache, self).__init__(options)

        if options:
            if options.l1i_size:
                self.size = options.l1i_size
            if options.l1i_data_latency:
                self.data_latency = options.l1i_data_latency
            if options.l1i_assoc:
                self.assoc = options.l1i_assoc

    # connects the CPU to the L1 instruction cache
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port

# --------------------------------------------------------------------------------
# L1 Data Cache
# extend the L1Cache class to create an L1 Data Cache
# --------------------------------------------------------------------------------
class L1DCache(L1Cache):

    # paramters
    size = '64kB'
    assoc = 2
    data_latency = 2

    # constructor - sets cache size
    def __init__(self, options = None):

        super(L1DCache, self).__init__(options)

        if options:
            if options.l1d_size:
                self.size = options.l1d_size
            if options.l1d_assoc:
                self.assoc = options.l1d_assoc

    # connects a CPU to the L1 data cache
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port

# --------------------------------------------------------------------------------
# L2 Cache
# create an L2 Cache by extending the BaseCache class
# --------------------------------------------------------------------------------
class L2Cache(Cache):

    # parameters
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12

    # constructor - sets cache size
    def __init__(self, options = None):

        super(L2Cache, self).__init__()

        if options:
            if options.l2_size:
                self.size = options.l2_size
            if options.l2_assoc:
                self.assoc = options.l2_assoc

    # connects the CPU side bus
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    # connects the memory side bus
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# --------------------------------------------------------------------------------
# L3 Cache
# create an L3 Cache by extending the BaseCache class
# --------------------------------------------------------------------------------
class L3Cache(Cache):

    # parameters
    size = '1MB'
    assoc = 64
    tag_latency = 32
    data_latency = 32
    response_latency = 32
    mshrs = 32
    tgts_per_mshr = 24
    write_buffers = 16

    # constructor - sets the cache size
    def __init__(self, options = None):
        
        super(L3Cache, self).__init__()
        
        if options:
            if options.l3_size:
                self.size = options.l3_size
            if options.l3_assoc:
                self.assoc = assoc.l3_assoc

    # connects the CPU side bus
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports

    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

# --------------------------------------------------------------------------------
# L3 Cache Bus
# --------------------------------------------------------------------------------
class L3XBar(CoherentXBar):

    # parameters
    # 256-bit crossbar by default
    width = 32
    frontend_latency = 1
    forward_latency = 0
    response_latency = 1
    snoop_response_latency = 1
    snoop_filter = SnoopFilter(lookup_latency = 0)
