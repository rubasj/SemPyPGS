import sys
from Workers import Worker
from xml.dom import minidom

# ******* DATA FOR STATS ****** #
# AB
# count of processed blocks
global count_processed_blocks

# CD
# average time for processing one block
global average_block_duration

# EF
# count of processed resources
global count_processed_resources

# GH
# average time for processing one resource
global total_time_mined_blocks

# IJ
# count of ferry paths
global ferry_count

# KL
# average waiting time for filling
global ferry_average_time

# YZ
# simulation duration
global end_of_simulation

# ************************************* #

# list (dictionary) of worker objects
worker_instances = {}

# ////// MESSAGES AND VARIABLES - lorry \\\\\\ #
is_full = "is full"
arrived_to_ferry = "arrived to ferry"
arrived_to_end = "arrived to END"

# -------------------------------------------- #
# list (dictionary) of lorry objects
lorry_instances = {}

# list of lorry data
lorry_data = []

# ////// MESSAGES AND VARIABLES - ferry \\\\\\ #
went_out = "went out"

# list of ferry data
ferry_data = []
# -------------------------------------------- #

# ////// MESSAGES AND VARIABLES - worker \\\\\\ #

block_mined = "block mined"
resource_mined = "resource mined"
# list of workers data
worker_data = []


# -------------------------------------------- #

# --------------------------------- WORKER - generating stats ------------------------------------ ##

# load worker instances
def generate_stats_worker():
    # GLOBALS
    global count_processed_blocks
    global count_processed_resources
    global total_time_mined_blocks
    global total_time_mined_resources
    global average_block_duration

    # temps for set globals
    count_processed_blocks = 0
    count_processed_resources = 0
    total_time_mined_blocks = 0.0
    total_time_mined_resources = 0.0

    #
    for data in worker_data:
        # split and find idx
        tmp1 = data[1].split('[')
        tmp2 = tmp1[1].split(']')
        idx = int(tmp2[0])

        # The item with ID does not exist => creating new instance
        if idx not in worker_instances:
            worker_instances[idx] = Worker(idx)

        if block_mined.__eq__(data[2]):

            # total time and count for worker instance
            worker_instances[idx].set_total_blocks()
            timeStr = data[3].replace(",", ".")
            time = float(timeStr)
            worker_instances[idx].set_total_worked_time(time)

            # total time and count for globals variables (temps)
            count_processed_blocks += 1
            total_time_mined_blocks += time

        # make record about processed resource
        elif resource_mined.__eq__(data[2]):
            count_processed_resources += 1
            timeStr = data[3].replace(",", ".")
            time = float(timeStr)
            total_time_mined_resources += time

    # storing values in global variables
    average_block_duration = total_time_mined_blocks / count_processed_blocks


# --------------------------------- ------------------------ ------------------------------------ ##

# --------------------------------- LORRY - generating stats ------------------------------------ ##
# class represented Lorry
class Lorry:
    def __init__(self, id):
        self._id = id
        self._load_time = 0.0
        self._transport_time = ferry_average_time

    def get_id(self):
        return self._id

    def set_load_time(self, time):
        self._load_time += time

    def set_transport_time(self, time):
        self._transport_time += time

    def get_load_time(self):
        return self._load_time

    def get_transport_time(self):
        return self._transport_time

def generate_stats_lorry():
    for data in lorry_data:
        tmp1 = data[1].split('[')
        tmp2 = tmp1[1].split(']')
        idx = int(tmp2[0])

        # The item with ID does not exist => creating new
        if idx not in lorry_instances:
            lorry_instances[idx] = Lorry(idx)

        if is_full.__eq__(data[2]):
            timeStr = data[3].replace(",", ".")
            time = float(timeStr)
            lorry_instances[idx].set_load_time(time)

        elif arrived_to_end.__eq__(data[2]) or arrived_to_ferry.__eq__(data[2]):
            timeStr = data[3].replace(",", ".")
            time = float(timeStr)
            lorry_instances[idx].set_transport_time(time)


# --------------------------------- ------------------------ ------------------------------------ ##

# --------------------------------- Ferry - generating stats ------------------------------------ ##
def generate_stats_ferry():
    # GLOBALS
    global ferry_count
    global ferry_average_time

    total_filling_time = 0.0
    ferry_count = len(ferry_data)

    for data in ferry_data:
        if went_out.__eq__(data[2]):
            timeStr = data[3].replace(",", ".")
            time = float(timeStr)
            total_filling_time += time

    ferry_average_time = total_filling_time / ferry_count


# --------------------------------- ------------------------ ------------------------------------ ##

# ----- Loading data from text file and sort records ----- ##

# load data from input file and sorted records
def load_data():
    global end_of_simulation, input_file

    file = sys.argv[2]

    try:
        input_file = open(file, "r")

        end_time_str = ""
        # first sorting row by object
        for line in input_file.readlines():
            x = line.split(";")
            end_time_str = x[0]
            if line.__contains__("#") or not line.__contains__(";"):
                continue

            elif x[1].__contains__("Worker"):
                worker_data.append(x)

            elif x[1].__contains__("Lorry"):
                lorry_data.append(x)

            elif x[1].__contains__("Ferry"):
                ferry_data.append(x)

        end_of_simulation = float(end_time_str.replace(",", "."))
        generate_stats_worker()
        generate_stats_ferry()
        generate_stats_lorry()

    except IOError:
        print("File not accessible")
    finally:
        input_file.close()


# ----- Create xml file based on stats ----- ##
def generate_xml():
    # root node
    root = minidom.Document()

    # simulation -> is root child
    simulation = root.createElement('Simulation')
    simulation.setAttribute('duration', str("{:.2f}".format(end_of_simulation)))
    root.appendChild(simulation)

    # add empty line
    simulation.appendChild(root.createTextNode(""))

    # blockAverageDuration -> is simulation child
    blockAverageDuration = root.createElement('blockAverageDuration')
    textAverage = root.createTextNode(str("{:.2f}".format(average_block_duration)))
    blockAverageDuration.appendChild(textAverage)
    blockAverageDuration.setAttribute('totalCount', str(count_processed_blocks))
    simulation.appendChild(blockAverageDuration)

    # resourceAverageDuration -> is simulation child
    resourceAverageDuration = root.createElement('resourceAverageDuration')
    resourceAverageDuration.setAttribute('totalCount', str(count_processed_resources))
    resourceAverageDuration.appendChild(root.createTextNode(str("{:.2f}".format(count_processed_resources))))
    # TODO osetrit chybu (resources)

    # ferryAverageWait -> is simulation child
    ferryAverageWait = root.createElement('ferryAverageWait')
    ferryAverageWait.setAttribute('trips', str(ferry_count))
    ferryAverageWait.appendChild(root.createTextNode(str("{:.2f}".format(ferry_average_time))))
    simulation.appendChild(ferryAverageWait)

    # workers
    workers = root.createElement("Workers")
    simulation.appendChild(root.createTextNode(""))

    for n in range(0, len(worker_instances)):
        w = worker_instances[n+1]

        workers.appendChild(root.createTextNode(""))
        wo = root.createElement("Worker")
        idx = w.get_id()
        wo.setAttribute('id', str(idx))
        resources = root.createElement('resources')
        resources.appendChild(root.createTextNode(str(w.get_total_blocks())))

        wo.appendChild(resources)
        workDuration = root.createElement('workDuration')
        workDuration.appendChild(root.createTextNode(str("{:.2f}".format(w.get_total_worked_time()))))
        wo.appendChild(workDuration)
        workers.appendChild(wo)

    workers.appendChild(root.createTextNode(""))
    simulation.appendChild(workers)
    simulation.appendChild(root.createTextNode(""))

    # vehicles
    vehicles = root.createElement('Vehicles')
    for n in range(len(lorry_instances)):
        lor = lorry_instances[n+1]
        vehicles.appendChild(root.createTextNode(""))
        lorry = root.createElement('Vehicle')
        lorry.setAttribute('vehicle', str(lor.get_id()))

        loadTime = root.createElement('loadTime')
        loadTime.appendChild(root.createTextNode(str(lor.get_load_time())))
        lorry.appendChild(loadTime)

        transportTime = root.createElement('transportTime')
        transportTime.appendChild(root.createTextNode(str(lor.get_transport_time())))
        lorry.appendChild(transportTime)
        vehicles.appendChild(lorry)



    vehicles.appendChild(root.createTextNode(""))
    simulation.appendChild(vehicles)
    simulation.appendChild(root.createTextNode(""))
    xml_str = root.toprettyxml(indent="\t")

    with open(sys.argv[4], "w") as f:
        f.write(xml_str)

    f.close()


# ------------------------------------------ ##

#   Main program method
if __name__ == '__main__':
    # check if count of parameters is 5
    if len(sys.argv) != 5:
        print("Wrong parameters:", len(sys.argv), "expected: 5")

    else:
        load_data()  # load data from input file
        generate_xml()  # XML generator method
