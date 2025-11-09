import torch
from diffusers import DiffusionPipeline
import argparse
import time
import random
import math
import numpy as np

def PoissonGen(rate, interval, seed=1):
    n = int(rate*interval)
    random.seed(seed)
    arr = [-np.log(random.random())/rate for _ in range(2*n)]
    acc = 0
    times = []
    for t in arr:
        acc += t
        if acc > interval:
            break
        times.append(acc)
    return times

prompts = ['realistic medieval castle downtown with soldiers and knights',
            'higly detailed, majestic royal tall ship on a calm sea,realistic painting, \
    by Charles Gregory Artstation and Antonio Jacobsen and Edward Moran, (long shot), clear blue sky, \
    intricated details, 4k',
            'I want to generate a group avatar for a Feishu group chat.\
    The role of this group is daily software technical communication. \
    Now the subject technology stacks that members of this group discuss daily include: \
    algorithms, data structures, optimization, functional programming, and the programming \
    languages often discussed are: TypeScript, Java, python, etc. \
    I hope this avatar has a simple aesthetic, this avatar is a single person avatar']

res_low = [64, 96, 128]
res_high = [256, 384, 512, 1024]

patterns = {
    'high' : [[0.0, 24.1822, 58.5168, 61.9939, 147.3740, 293.9903, 328.7430, 338.8403, 546.3436, 592.0992],
              [1.5996, 40.1941, 272.3170, 301.6533, 317.9071, 353.9856, 446.4671, 460.7184, 487.1172, 533.4843],
              [27.0417, 60.0327, 90.4605, 153.9525, 355.9670, 398.3473, 419.6466, 440.7745, 560.7427, 590.3304],
              [29.4346, 66.0883, 95.4533, 105.0176, 154.9749, 251.4679, 380.0509, 382.5629, 472.0273, 516.0084, 584.4252]],       
}

if __name__ == "__main__":
    random.seed(74)
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
    parser.add_argument(
        "--downloadonly",
        action="store_true"
    )
    parser.add_argument(
        "--config", type=int, default=1,choices=[1,2,3,4], help="Arrival trace choice"
    )
    parser.add_argument(
        "--idle", type=float, default=0.3, help="idle percentage"
    )
    parser.add_argument(
        "--tag", type=str, default='default', help="exp tag"
    )
    parser.add_argument(
        "--continuous",
        action="store_true"
    )
    args = parser.parse_args()
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", use_safetensors=True, torch_dtype=torch.bfloat16)
    if args.workload == 'low':
        myprompt = prompts[1]
        myres = res_high[2]
        steps = 15
        arrivals = PoissonGen(0.05, args.duration, args.config+17)
    elif args.workload == 'high':
        myprompt = prompts[2]
        myres = res_high[3]
        steps = 5
        arrivals = PoissonGen(0.04, args.duration, args.config+13)
    elif args.workload == 'med':
        myprompt = prompts[1]
        myres = res_high[0]
        steps = 5
        arrivals = PoissonGen(0.04, args.duration, args.config+17)
    else:
        myprompt = prompts[random.randint(0,2)]
        myres = res_high[random.randint(0,2)]
        steps = 5
        arrivals = [28.774393103543197, 55.77128263960971, 162.15597087662746,
                    353.6182113235427, 547.7951661534263]
    if (not args.downloadonly):
        begintime = time.time()
        curtime = begintime
        endtime = curtime + args.duration
        csvlines = []
        csvlines.append("Curtime,Elapsed,Batchsize")
        '''
        while curtime < endtime:
            image = pipeline(myprompt,
                            width=myres,
                            height=myres,
                            num_inference_steps=steps)
            elapsed = time.time() - curtime
            csvlines.append(f"{curtime-begintime},{elapsed}")
            time.sleep(elapsed*args.idle)
            curtime = time.time()
        '''
        logsum = 0
        total = 0
        count = 0
        if args.continuous:
            while curtime < endtime:
                image = pipeline(myprompt,
                            width=myres,
                            height=myres,
                            num_inference_steps=steps)
                elapsed = time.time() - curtime
                logsum += math.log(elapsed)
                total += elapsed
                count += 1
                csvlines.append(f"{curtime-begintime},{elapsed}")
                curtime = time.time()
        else:
            for cnt,t in enumerate(arrivals):
                if args.workload == 'med':
                    myprompt = prompts[cnt%3]
                    myres = res_high[cnt%2]
                curtime = time.time() - begintime
                if t > args.duration:
                    break
                if curtime < t:
                    time.sleep(t-curtime)
                image = pipeline(myprompt,
                                width=myres,
                                height=myres,
                                num_inference_steps=steps)
                elapsed = time.time() - t - begintime
                logsum += math.log(elapsed)
                total += elapsed
                count += 1
                csvlines.append(f"{curtime},{elapsed},1")
        gmean = math.exp(logsum/count)
        #csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count},1")
        with open(f"/mydata/workspace/jrapl/{args.tag}_stable-diffusion_{args.workload}.csv", "w") as f:
            f.write("\n".join(csvlines))