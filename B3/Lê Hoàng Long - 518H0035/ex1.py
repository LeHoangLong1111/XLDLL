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
    value = record[1]
    words = value.split()
    for word in words:
        mr.emit_intermediate(word, 1)
def reducer(key, list):
    total = 0
    for v in list:
        total += v
    mr.emit((key, total))
if __name__ == '__main__':
    inputdata = open("./data.json")
    mr.execute(inputdata, mapper, reducer)