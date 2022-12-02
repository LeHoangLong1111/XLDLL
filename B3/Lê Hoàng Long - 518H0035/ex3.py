import json
from operator import itemgetter

class MapReduce:
    def __init__(self):
        self.intermediate = {}
        self.result = []
    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)
    def emit(self, value):
        self.result.append(value)
    def execute(self, data, mapper, reducer):
        for line in data:
            record = json.loads(line)
            mapper(record)
        for key in self.intermediate:
            reducer(key, self.intermediate[key])
        #jenc = json.JSONEncoder(encoding='utf-8')
        jenc = json.JSONEncoder()
        for item in self.result:
            print(jenc.encode(item))

mr =MapReduce()

def mapper(record):
    key = record[0]
    mr.emit_intermediate(key, 1)
def reducer(key, list):
    count = len(list)
    mr.emit((key, count))
if __name__ == '__main__':
    inputdata = open("./friends.json")
    mr.execute(inputdata, mapper, reducer)