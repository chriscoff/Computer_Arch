
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

    def __init__(self, cpu_path, **kwargs):

        super(CpuPowerOn, self).__init__(**kwargs)

        # 2A per IPC and 3pA per cache miss. Then convert to Watts.
        # dynamic power
        self.dyn = 'voltage*(2*{}.ipc + 3*0.000000001*{}.dcache.overallMisses/simSeconds)'.format(cpu_path, cpu_path)
        # static power
        self.st = '4*temp'

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

    def __init__(self, cpu_path, **kwargs):

        super(CpuPowerModel, self).__init__(**kwargs)

        self.pm = [
            CpuPowerOn(cpu_path), # ON
            CpuClkGated(),        # CLK_GATED
            CpuSramRetention(),   # SRAM_RETENTION
            CpuPowerOff()         # OFF
        ]