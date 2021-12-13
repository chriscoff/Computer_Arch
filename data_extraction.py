
# --------------------------------------------------------------------------
# Data Extraction Class
# --------------------------------------------------------------------------
class DataExtraction:
    """This class extracts relevant data from the gem5 output text file and
    places the data in a .csv file.
    """

    # ----------------------------------------------------------------------
    # Constructor
    # ----------------------------------------------------------------------
    def __init__(self, exiting_tick, stats_period, stats_filename = "m5out/stats.txt"):
        """Constructor function. Reads the gem5 output test file.
        """

        self.exiting_tick = exiting_tick
        self.stats_period = stats_period

        with open(stats_filename, "r") as stats_file:
            self.stats_lines = stats_file.readlines()

    # ----------------------------------------------------------------------
    # Create CSV File
    # ----------------------------------------------------------------------
    def CreateCsv(self, parameters, csv_filename, static_power, dynamic_power):
        """This creates a .csv file and writes the static and dynamic power 
        data to the .csv file. This function also writes the exiting tick
        value and the stats dump period.
        """

        csv_file = open(csv_filename, "w")

        # writing parameters
        for i in range(len(parameters[0])):
            csv_file.write("{}\n".format(parameters[0][i]))
            csv_file.write("{}\n\n".format(parameters[1][i]))

        # writing power data
        csv_file.write("Dynamic Power (Watts), Static Power (Watts)\n")
        for i in range(len(static_power)):
            csv_file.write("{}, {}\n".format(dynamic_power[i], static_power[i]))

        # writing exiting tick and stats dump period
        csv_file.write("\n")
        csv_file.write("Exiting Tick, Stats Dump Period (seconds)\n")
        csv_file.write("{}, {}\n".format(self.exiting_tick, self.stats_period))

        csv_file.close()

    # ----------------------------------------------------------------------
    # Extract CPU Power Data
    # ----------------------------------------------------------------------
    def ExtractCpuPowerData(self, parameters, csv_filename = "configs/project/cpu_power_data.csv"):
        """This function extracts the CPU's power modeling data and places
        it into a .csv file.
        """

        dynamic_power = []
        static_power = []

        for line in self.stats_lines:
            line_split = line.split()
            if line_split:
                if line_split[0] == "system.processor.cpu.power_model.pm0.dynamicPower":
                    dynamic_power.append(float(line_split[1]))
                elif line_split[0] == "system.processor.cpu.power_model.pm0.staticPower":
                    static_power.append(float(line_split[1]))
        
        self.CreateCsv(parameters, csv_filename, static_power, dynamic_power)

    # ----------------------------------------------------------------------
    # Extract L2 Cache Power Data
    # ----------------------------------------------------------------------
    def ExtractL2CachePowerData(self, parameters, csv_filename = "configs/project/l2_cache_power_data.csv"):
        """This function extracts the L2 Cache's power modeling data and
        places it into a .csv file.
        """

        dynamic_power = []
        static_power = []

        for line in self.stats_lines:
            line_split = line.split()
            if line_split:
                if line_split[0] == "system.processor.l2cache.power_model.pm0.dynamicPower":
                    dynamic_power.append(float(line_split[1]))
                elif line_split[0] == "system.processor.l2cache.power_model.pm0.staticPower":
                    static_power.append(float(line_split[1]))

        self.CreateCsv(parameters, csv_filename, static_power, dynamic_power)

    # ----------------------------------------------------------------------
    # Extract L3 Cache Power Data
    # ----------------------------------------------------------------------
    def ExtractL3CachePowerData(self, parameters, csv_filename = "configs/project/l3_cache_power_data.csv"):
        """This function extracts the L3 cache's power modeling data and
        places it into a .csv file.
        """

        dynamic_power = []
        static_power = []

        for line in self.stats_lines:
            line_split = line.split()
            if line_split:
                if line_split[0] == "system.processor.l3cache.power_model.pm0.dynamicPower":
                    dynamic_power.append(float(line_split[1]))
                elif line_split[0] == "system.processor.l3cache.power_model.pm0.staticPower":
                    static_power.append(float(line_split[1]))
        
        self.CreateCsv(parameters, csv_filename, static_power, dynamic_power)
