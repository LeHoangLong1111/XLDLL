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
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)
def reducer(key, list):
    for order in list:
      if order[0]=='order':
        for order1 in list:
          if order1[0] == 'line_item':
            mr.emit(order+order1)
if __name__ == '__main__':
    inputdata = open("./records.json")
    mr.execute(inputdata, mapper, reducer)