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
            return self.database[probe_name][-how_many:]
        except KeyError:
            return None


class DiaryManager(BaseManager):
    pass

DiaryManager.register('Diary', Diary)
