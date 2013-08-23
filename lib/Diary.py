from multiprocessing.managers import BaseManager

class Diary(object):
    def __init__(self):
        self.load = []
        self.mem_info = []

    def write_load(self, load_values):
        self.load.append(load_values)

    def read_load(self, how_many=50):
        # Return how_many elements, counting from the end.
        return self.load[-how_many:]

    def write_mem_info(self, mem_info):
        self.mem_info.append(mem_info)

    def read_mem_info(self):
        return self.mem_info

class DiaryManager(BaseManager):
    pass

DiaryManager.register('Diary', Diary)
