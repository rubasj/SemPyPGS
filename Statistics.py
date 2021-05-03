import sys
from xml.dom import minidom

####### MESSAGES AND VARIABLES - worker ########

block_mined = "block mined"
resource_mined = "resource mined"

global count_of_mined_blocks
global average_block_duration

global count_of_mined_resources
global average_resource_duration

global end_of_simulation

# list (dictionary) of worker objects
worker_instances = {}

####### MESSAGES AND VARIABLES - lorry ########
is_full = "is full"
arrived_to_ferry = "arrived to ferry"
arrived_to_end = "arrived to END"

# list (dictionary) of lorry objects
lorry_objects = {}

# list of lorry data
lorry_data = []

####### MESSAGES AND VARIABLES - ferry ########
went_out = "went out"

# count of ferry paths
global ferry_count
# average waiting time for filling
global ferry_average_time

# list of workers data
worker_data = []

# list of ferry data
ferry_data = []


# class witch represented Worker
class Worker:
    def __init__(self, id):
        self.__id = id
        self.__total_worked_time = 0.0
        self.__total_blocks = 0

    @property
    def get_id(self):
        return self.__id

    def set_total_blocks(self):
        self.__total_blocks += 1

    def set_total_worked_time(self, time):
        self.__total_worked_time += time

    @property
    def get_total_worked_time(self):
        return self.__total_worked_time

    @property
    def get_total_blocks(self):
        return self.__total_blocks


def worker_add_record(idx, data):
    # GLOBALS
    global count_of_mined_blocks
    global average_block_duration

    # temps for set globals
    total_count_mined_blocks = 0
    total_count_mined_resources = 0
    total_time_mined_blocks = 0.0
    total_time_mined_resources = 0.0

    if block_mined.__eq__(data[2]):

        # total time and count for worker instance
        worker_instances[idx].set_total_blocks()
        timeStr = data[3].replace(",", ".")
        time = float(timeStr)
        worker_instances[idx].set_total_worked_time(time)

        # total time and count for globals variables (temps)
        total_count_mined_blocks = total_count_mined_blocks + 1
        total_time_mined_blocks += time

    # make record about processed resource
    elif resource_mined.__eq__(data[2]):
        total_count_mined_resources += 1
        timeStr = data[3].replace(",", ".")
        time = float(timeStr)
        total_time_mined_resources += time

    # storing values in global variables
    # count_of_mined_blocks = total_count_mined_blocks
    # average_block_duration = total_time_mined_blocks / count_of_mined_blocks


# load worker instances
def generate_stats_worker():
    for data in worker_data:
        # split and find idx
        tmp1 = data[1].split('[')
        tmp2 = tmp1[1].split(']')
        idx = int(tmp2[0])

        # the item with idx exist, add new record
        if idx in worker_instances:
            worker_add_record(idx, data)

        # The item with ID does not exist => creating new
        else:
            worker_instances[idx] = Worker(idx)
            worker_add_record(idx, data)

    # print(count_of_mined_blocks, average_time_one_block)


# class represented Lorry
class Lorry:
    def __init__(self, id):
        self.__id = id
        self.__time_filling = 0.0
        self.__duration_time = ferry_average_time

    @property
    def get_id(self):
        return self.__id

    def set_time_filling(self, time):
        self.__time_filling += time

    def set_duration_time(self, time):
        self.__time_filling += time


def generate_stats_lorry():
    for data in lorry_data:
        tmp1 = data[1].split('[')
        tmp2 = tmp1[1].split(']')
        idx = int(tmp2[0])

        if idx in lorry_objects:
            lorry_add_record(idx, data)

        # The item with ID does not exist => creating new
        else:
            lorry_objects[idx] = Lorry(idx)
            lorry_add_record(idx, data)


def lorry_add_record(idx, data):
    if is_full.__eq__(data[2]):
        timeStr = data[3].replace(",", ".")
        time = float(timeStr)
        lorry_objects[idx].set_time_filling(time)

    elif arrived_to_end.__eq__(data[2]) or arrived_to_ferry.__eq__(data[2]):  # todo zjistit jak je to s treti promennou
        timeStr = data[3].replace(",", ".")
        time = float(timeStr)
        lorry_objects[idx].set_duration_time(time)


def generate_stats_ferry():
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


def load_data():
    global inputFile
    # print(sys.argv)

    file = sys.argv[2]

    try:
        inputFile = open(file, "r")

        end_time_str= ""
        # first sorting row by object
        for line in inputFile.readlines():
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
        print(end_of_simulation)
        generate_stats_worker()
        generate_stats_ferry()
        generate_stats_lorry()

    except IOError:
        print("File not accessible")
    finally:
        inputFile.close()


# method evaluate data from load_data method
def generate_xml():
    global outputfile

    # simulation = minidom.Document()
    #
    # xml = simulation.createElement('Simulation')
    # simulation.setAttribute('duration', )
    #
    # try:
    #     outputfile = open(sys.argv[4], "w")
    #     print(sys.argv[4])
    #
    # except IOError:
    #     print("Problem with outputfile.")
    #
    # finally:
    #     outputfile.close()


#   Main program method
if __name__ == '__main__':
    # check if count of parameters is 5
    if len(sys.argv) != 5:
        print("Wrong parameters:", len(sys.argv), "expected: 5")

    else:
        load_data()  # load data from input file
        generate_xml()  # XML generator method
