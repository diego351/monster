from collections import deque
from multiprocessing.managers import BaseManager

class Diary(object):
    def __init__(self):
        self.database = {}

    def write(self, probe_name, value):
        try:
            self.database[probe_name].append(value)
        except KeyError:
            self.database[probe_name] = deque([value], 100)

    def read(self, probe_name, how_many=50):
        try:
            series = list(self.database[probe_name])[-how_many:]
            return series

        except KeyError:
            return None


class DiaryManager(BaseManager):
    pass

DiaryManager.register('Diary', Diary)
