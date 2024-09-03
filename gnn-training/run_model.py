import subprocess
import argparse
import time
import os

parser = argparse.ArgumentParser()
parser.add_argument(
    "--workload",
    type=str,
    default="low",
    choices=['low','med','high','random','sinusoidal'],
    help="workload heaviness",
)
parser.add_argument(
    "--duration", type=int, default=60, help="Benchmark duration in seconds"
)

args = parser.parse_args()

configs = ['CSL-gcn.json','collab-graphsage.json','superpixels_gat_cifar10.json']
scripts = [
    'main_CSL_graph_classification.py ',
    'main_COLLAB_edge_classification.py',
    'main_superpixels_graph_classification.py'
]

curtime = time.time()
endtime = curtime + args.duration

while curtime < endtime:
    if args.workload == 'low':
        myconfig = configs[0]
        myscript = scripts[0]
    elif args.workload == 'med':
        myconfig = configs[1]
        myscript = scripts[1]
    elif args.workload == 'high':
        myconfig = configs[2]
        myscript = scripts[2]
    else:
        idx = random.randint(0,2)
        myconfig = configs[idx]
        myscript = scripts[idx]
    os.system('python ' + myscript + ' --config ' + myconfig)
    curtime = time.time()
