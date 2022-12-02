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
    if record[0]=='a':
        for m in range(5):
            key = (record[1],m)
            value = (0, record[2], record[3]) 
            mr.emit_intermediate(key, value)
    else:
        for n in range(5):
            key = (n,record[2])
            value = (1, record[1], record[3])
            mr.emit_intermediate(key,value)
def reducer(key, list_values):
    hash_A = {}
    hash_B = {}

    for item in list_values:
      if item[0]==0:
        hash_A[item[1]] = item[2]
      else:
        hash_B[item[1]] = item[2]
    # print("B: ",hash_B)
    # print("A: ",hash_A)
    result = 0
    for j in range(5):
      try:
        result += hash_A[j]*hash_B[j]
      except:
        pass
    mr.emit(tuple(list(key)+[result]))

if __name__ == '__main__':
    inputdata = open("./matrix.json")
    mr.execute(inputdata, mapper, reducer)