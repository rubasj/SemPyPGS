# class witch represented Worker
class Worker:
    # class constructor
    def __init__(self, id):
        # index worker
        self._id = id
        # worker's total worked time
        self._total_worked_time = 0.0
        # worker's total processed blocks
        self._total_blocks = 0

    # getter method for ID
    def get_id(self):
        return self._id

    # setter total blocks
    def set_total_blocks(self):
        self._total_blocks += 1

    # setter total worked time
    def set_total_worked_time(self, time):
        self._total_worked_time += time

    # getter total worked time
    def get_total_worked_time(self):
        return self._total_worked_time

    # getter total blocks
    def get_total_blocks(self):
        return self._total_blocks

