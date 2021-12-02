
# --------------------------------------------------------------------------
# Import Libraries
# --------------------------------------------------------------------------
import m5
from m5.objects import MathExprPowerModel
from m5.objects import PowerModel

# --------------------------------------------------------------------------
# CPU Power On Class
# --------------------------------------------------------------------------
class CpuPowerOn(MathExprPowerModel):

    def __init__(self, cpu_path, options, **kwargs):

        super(CpuPowerOn, self).__init__(**kwargs)

        # select the equation to use to model the processor's power consumption
        if options.cpu_pwr_eq == 0:
            # 2A per IPC and 3pA per cache miss. Then convert to Watts.
            # dynamic power
            self.dyn = 'voltage*(2*{}.ipc + 3*0.000000001*{}.dcache.overallMisses/simSeconds)'.format(cpu_path, cpu_path)
            # static power
            self.st = '4*temp'
        elif options.cpu_pwr_eq == 1:
            # TODO: remove 'pass' and place a different power modeling 
            # equation here. If needed, create other if cases with different 
            # equations in them.
            pass

# --------------------------------------------------------------------------
# CPU Clock Gated Class
# --------------------------------------------------------------------------
class CpuClkGated(MathExprPowerModel):

    dyn = '0'
    st ='0'

# --------------------------------------------------------------------------
# CPU SRAM Retention Class
# --------------------------------------------------------------------------
class CpuSramRetention(MathExprPowerModel):

    dyn = '0'
    st ='0'

# --------------------------------------------------------------------------
# CPU Power Off Class
# --------------------------------------------------------------------------
class CpuPowerOff(MathExprPowerModel):
    
    # CPU is off therefore no power is being used
    dyn = '0'
    st = '0'

# --------------------------------------------------------------------------
# CPU Power Model Class
# --------------------------------------------------------------------------
class CpuPowerModel(PowerModel):

    def __init__(self, cpu_path, options, **kwargs):

        super(CpuPowerModel, self).__init__(**kwargs)

        self.pm = [
            CpuPowerOn(cpu_path, options), # ON
            CpuClkGated(),                 # CLK_GATED
            CpuSramRetention(),            # SRAM_RETENTION
            CpuPowerOff()                  # OFF
        ]

# --------------------------------------------------------------------------
# L2 Cache Power On Class
# --------------------------------------------------------------------------
class L2PowerOn(MathExprPowerModel):

    def __init__(self, l2_path, options, **kwargs):

        super(L2PowerOn, self).__init__(**kwargs)

        # select the equation to use to model the L2 cache's power consumption
        if options.l2_pwr_eq == 0:
            # Report L2 Cache overall accesses. The estimated power is converted
            # to Watts and will vary based on the size of the cache.
            self.dyn = '{}.overallAccesses*0.000018000'.format(l2_path)
            self.st = '(voltage*3)/10'
        elif options.l2_pwr_eq == 1:
            # TODO: remove 'pass' and place a different power modeling 
            # equation here. If needed, create other if cases with different 
            # equations in them.
            pass

# --------------------------------------------------------------------------
# L2 Cache Clock Gated Class
# --------------------------------------------------------------------------
class L2ClockGated(MathExprPowerModel):

    dyn = '0'
    st = '0'

# --------------------------------------------------------------------------
# L2 Cache SRAM Retention Class
# --------------------------------------------------------------------------
class L2SramRetention(MathExprPowerModel):

    dyn = '0'
    st = '0'

# --------------------------------------------------------------------------
# L2 Cache SRAM Retention Class
# --------------------------------------------------------------------------
class L2PowerOff(MathExprPowerModel):

    # L2 Cache is off therefore no power is being used
    dyn = '0'
    st = '0'

# --------------------------------------------------------------------------
# L2 Cache Power Model
# --------------------------------------------------------------------------
class L2PowerModel(PowerModel):

    def __init__(self, l2_path, options, **kwargs):

        super(L2PowerModel, self).__init__(**kwargs)

        # choose a power model for each power state
        self.pm = [
            L2PowerOn(l2_path, options), # ON
            L2ClockGated(),              # CLK_GATED
            L2SramRetention(),           # SRAM_RETENTION
            L2PowerOff()                 # OFF
        ]

# --------------------------------------------------------------------------
# L3 Cache Power On Class
# --------------------------------------------------------------------------
class L3PowerOn(MathExprPowerModel):

    def __init__(self, l3_path, options, **kwargs):

        super(L3PowerOn, self).__init__(**kwargs)

        # select the equation to use to model the L3 cache's power consumption
        if options.l3_pwr_eq == 0:
            # Report L3 Cache overall accesses. The estimated power is converted
            # to Watts and will vary based on the size of the cache.
            self.dyn = '{}.overallAccesses*0.000018000'.format(l3_path)
            self.st = '(voltage*3)/10'
        elif options.l3_pwr_eq == 1:
            # TODO: remove 'pass' and place a different power modeling 
            # equation here. If needed, create other if cases with different 
            # equations in them.
            pass

# --------------------------------------------------------------------------
# L3 Cache Clock Gated Class
# --------------------------------------------------------------------------
class L3ClockGated(MathExprPowerModel):

    dyn = '0'
    st = '0'

# --------------------------------------------------------------------------
# L3 Cache SRAM Retention Class
# --------------------------------------------------------------------------
class L3SramRetention(MathExprPowerModel):

    dyn = '0'
    st = '0'

# --------------------------------------------------------------------------
# L3 Cache SRAM Retention Class
# --------------------------------------------------------------------------
class L3PowerOff(MathExprPowerModel):

    # L3 Cache is off therefore no power is being used
    dyn = '0'
    st = '0'

# --------------------------------------------------------------------------
# L3 Cache Power Model
# --------------------------------------------------------------------------
class L3PowerModel(PowerModel):

    def __init__(self, l3_path, options, **kwargs):

        super(L3PowerModel, self).__init__(**kwargs)

        # choose a power model for each power state
        self.pm = [
            L3PowerOn(l3_path, options), # ON
            L3ClockGated(),              # CLK_GATED
            L3SramRetention(),           # SRAM_RETENTION
            L3PowerOff()                 # OFF
        ]