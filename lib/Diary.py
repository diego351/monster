from multiprocessing.managers import BaseManager

class Diary(object):
    def __init__(self):
        self.database = {}

    def write(self, probe_name, value):
        try:
            self.database[probe_name].append(value)
        except KeyError:
            self.database[probe_name] = [value]

    def read(self, probe_name, how_many=50):
        try:
            series = self.database[probe_name][-how_many:]
            if len(series) < how_many:
                return [{} for i in xrange(how_many - len(series))] + (series)
            else:
                return series

        except KeyError:
            return None


class DiaryManager(BaseManager):
    pass

DiaryManager.register('Diary', Diary)
