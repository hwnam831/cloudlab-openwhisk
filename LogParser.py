import re
import sys

class ShortRecord():
    def __init__(self, input):
        pattern = re.compile(r"(\d+\-\d+\-\d+)\s+(\d+\:\d+\:\d+)\s+(.+)\s+(.+)\s+(cold|warm)\s+(.+s)\s+(success|developer error)\s+(.+)")
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
            else:
                dm = re.match(r"(\d+)m(\d+\.\d+)s",duration)
                self.duration = float(dm.group(2)) + 60*int(dm.group(1))
            #print(duration + ' is ' + str(self.duration))
            self.status = m.group(7)
            self.funcname = m.group(8)

if __name__=='__main__':
    fname = sys.argv[1]
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
    for r in records:
        if r.start != 'cold' and r.status != 'developer error':
            validcount += 1
            totalduration += r.duration
    print('Valid invocations : ' + str(validcount))
    print('Avg response time : {}'.format(totalduration/validcount))
