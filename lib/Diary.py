class Diary(object):

    def __init__(self):
        self.load_record = []

    def start(self):
        pass

    def stop(self):
        print "[!] Closing the diary."

    def write_load(self, load_report):
        self.load_record.append(load_report)
