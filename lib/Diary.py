from collections import deque
from multiprocessing.managers import BaseManager


class Diary(object):

    def __init__(self):
        self.database = {}
        self.archive_max = {}
        self.archive_avg = {}

        self.f = 5
        self.x = 200

        self.t = {
            "30min": 1800,
            "1day": 84600,
            "1week": 604800,
            "1month": 2538000, # assuming month - 30 days
            }

        self.c = {}
        self.z = {}
        for i in self.t:
            self.c[i] = self.t[i] / self.f
            self.z[i] = self.c[i] / self.x

        self.live_queue_size = max(self.z.values()) + 16 # just in case
        for i in self.t:
            self.archive_max[i] = {}
            self.archive_avg[i] = {}

        self.counters = {}
            
        



    def write(self, probe_name, value):
        try:
            self.database[probe_name].append(value)
        except KeyError:
            self.database[probe_name] = deque([value], self.live_queue_size)

        if "Heavy" in probe_name or "Apache" in probe_name or "Nginx" in probe_name:
            return False

        try:
            self.counters[probe_name] += 1
        except KeyError:
            self.counters[probe_name] = 1

        for i in self.t:
            if self.counters[probe_name] % self.z[i] == 0:
                #self.archive_max[probe_name][i].append() 
                #which value in dictionary should we take as most important?
                sl = list(self.database[probe_name])[- self.z[i] - 1: -1]
                average_dict = self.getAvgDict(sl)
                try:
                    self.archive_avg[i][probe_name].append(average_dict)
                except KeyError:
                    self.archive_avg[i][probe_name] = deque([average_dict],self.c[i] + 16)

    def read(self, probe_name, how_many=50):
        try:
            series = list(self.database[probe_name])[-how_many:]
            return series

        except KeyError:
           return None

    def readArchiveAvg(self,probe_name,interval,how_many = 50):
        try:
            series = list(self.archive_avg[interval][probe_name])[-how_many:]
            return series

        except KeyError:
            return None

    def getAvgDict(self, a):
        # let's assume that a is a list of dictionaries
        avg = {}
        for one_dict in a:
            for value in one_dict:
                try:
                    avg[value] += one_dict[value]
                except KeyError:
                    avg[value] = one_dict[value]
        #print avg

        for v in avg:
            avg[v] /= len(a)

        return avg


class DiaryManager(BaseManager):
    pass

DiaryManager.register('Diary', Diary)
