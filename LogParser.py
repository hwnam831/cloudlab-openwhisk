import re
import sys
import json

class ShortRecord():
    def __init__(self, input):
        pattern = re.compile(r"(\d+\-\d+\-\d+)\s+(\d+\:\d+\:\d+)\s+(.+)\s+(.+)\s+(cold|warm)\s+(.+s)\s+(success|developer error)\s+guest\/(.+)\:\d\.\d\.\d")
        m = pattern.match(input)
        if not m:
            print('error parsing :' + input)
        else:
            self.date = m.group(1)
            self.time = m.group(2)
            self.id = m.group(3)
            self.start = m.group(5)
            duration = m.group(6)
            if re.match(r"\d+ms", duration):
                self.duration = int(duration[:-2])/1000
            elif re.match(r"\d+\.\d+s",duration):
                self.duration = float(duration[:-1])
            elif re.match(r"\d+s",duration):
                self.duration = float(duration[:-1])
            else:
                dm = re.match(r"(\d+)m(\d+\.\d+|\d+)s",duration)
                self.duration = float(dm.group(2)) + 60*int(dm.group(1))
            #print(duration + ' is ' + str(self.duration))
            self.status = m.group(7)
            self.funcname = m.group(8)

if __name__=='__main__':
    fname = sys.argv[1]
    m = re.match(r".+\_(.+\_.+)\_\d+\.log", fname)
    assert not m is None
    slist = []
    with open(fname,'r') as f:
        for l in f:
            slist.append(l)
        slist = slist[1:]
    pattern = re.compile(r"(\d+\-\d+\-\d+)\s+(\d+\:\d+\:\d+)\s+(.+)\s+(.+)\s+(cold|warm)\s+(.+s)\s+(success|developer error)\s+(.+)")
    records = []
    for l in slist:
        s = ShortRecord(l)
        records.append(s)
    totalduration = 0.0
    validcount = 0
    perfunction = {}
    for r in records:
        if r.start != 'cold' and r.status != 'developer error':
            if not r.funcname in perfunction:
                perfunction[r.funcname] = [1, r.duration]
            else:
                perfunction[r.funcname][0] += 1
                perfunction[r.funcname][1] += r.duration
    configjson = json.load(open("mxcontainerconfigs/"+m.group(1) + '.json','r'))
    ratios = {}
    ratiosum = 0.0
    for instance in configjson['instances']:
        funcname = configjson['instances'][instance]['application']
        ratios[funcname] = configjson['instances'][instance]['rate']
        ratiosum += ratios[funcname]
    print(ratios)
    weightedsum = 0.0
    perfuncsum = 0.0
    for funcname in perfunction:
        print("{}, {}".format(funcname,perfunction[funcname][1]/perfunction[funcname][0]))
        weightedsum += perfunction[funcname][1]/perfunction[funcname][0] * ratios[funcname]/ratiosum
        perfuncsum += perfunction[funcname][1]/perfunction[funcname][0]/len(perfunction)
    
    
    print("Avg invocation time: {}".format(weightedsum))
    print("Per function time: {}".format(perfuncsum))
    #print('Valid invocations : ' + str(validcount))
    #print('Avg response time : {}'.format(totalduration/validcount))
