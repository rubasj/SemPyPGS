import sys


####### MESSAGES AND VARIABLES - worker ########
block_mined = "block mined"
resource_mined = "resource mined"

total_count_mined_blocks = 0
total_count_mined_resources = 0
total_time_mined_blocks = 0.00
total_time_mined_resources = 0.00

# list (dictionary) of worker instances
worker_instances = {}


####### MESSAGES AND VARIABLES - lorry ########
is_full = "is full"
arrived_to_ferry = "arrived to ferry"
arrived_to_end = "arrived to END"
travel_time = 0.0
# list of lorry instances
lorry_instances = {}

# list of lorry data
lorry_data = []


####### MESSAGES AND VARIABLES - ferry ########
went_out = "went out"
ferry_count = 0

# list of workers data
worker_data = []



# list of ferry data
ferry_data = []


# class represented Lorry
class Lorry:
    def __init__(self, id):
        self.__id = id
        self.__time_filling = 0.0


# class witch represented Worker
class Worker:
    def __init__(self, id):
        self.__id = id
        self.__total_worked_time = 0.0
        self.__total_blocks = 0

    def getID(self):
        return self.__id

    def setBlocks(self):
        self.__total_blocks += 1

    def setTotalWorkedTime(self, time):
        self.__total_worked_time += time


# load data from file
def generate_stats_worker():
    for w in worker_data:
        tmp1 = w[1].split('[')
        tmp2 = tmp1[1].split(']')
        number = int(tmp2[0])

        if number in worker_instances:
            pass

        else:
            worker_instances[number] = Worker(number)


def load_data():
    global inputFile

    # print(sys.argv)

    file = sys.argv[2]

    try:
        inputFile = open(file, "r")
        print()
        # first sorting row by object
        for line in inputFile.readlines():
            x = line.split(";")
            if line.__contains__("#") or not line.__contains__(";"):
                continue

            elif x[1].__contains__("Worker"):
                worker_data.append(x)

            elif x[1].__contains__("Lorry"):
                lorry_data.append(x)

            elif x[1].__contains__("Ferry"):
                ferry_data.append(x)

        generate_stats_worker()

    except IOError:
        print("File not accessible")
    finally:
        inputFile.close()


# method evaluate data from load_data method
def generate_xml():
    pass


#   Main program method
if __name__ == '__main__':
    # check if count of parameters is 5
    if len(sys.argv) != 5:
        print("Wrong parameters:", len(sys.argv), "expected: 5")

    else:
        load_data()  # load data from input file
        generate_xml()  # XML generator method
