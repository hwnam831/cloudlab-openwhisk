import torch
from diffusers import DiffusionPipeline
import argparse
import time
import random
import math

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
res_high = [256, 384, 512]



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
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", use_safetensors=True)
    if args.workload == 'low':
        myprompt = prompts[0]
        myres = res_low[0]
        steps = 10
        arrivals = [0.0, 14.079019926956557, 20.21188621509486, 32.73587849403652,
                    41.91358630783891, 99.21233244629681, 162.5987408251167, 196.06716880038928,
                    210.89409933305262, 227.98369242544203, 237.35931849642836, 244.40616795859367,
                    255.69254566908424, 268.19301239076356, 280.1921241532026, 291.29750439343707,
                    320.8850211761088, 335.81933862987455, 353.9010340535836, 371.6544130462701,
                    374.1089278203828, 387.03256750204366, 387.53430820156825, 393.8648542868814,
                    401.151599459538, 407.29729689513937, 415.70429737935484, 431.47368326373044,
                    432.5365363402964, 437.42021755167525, 466.23249052883085, 488.1839171516043,
                    491.25963972227913, 508.1832846249064, 510.30833267986054, 560.019955813888, 575.3665743896685]
    elif args.workload == 'high':
        myprompt = prompts[2]
        myres = res_high[2]
        steps = 5
        arrivals = [24.1822, 58.5168, 61.9939, 
                    147.3740, 293.9903, 328.7430, 
                    338.8403, 546.3436, 592.0992]
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
        csvlines.append("Curtime,Elapsed")
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
            for t in arrivals:
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
                csvlines.append(f"{curtime},{elapsed}")
        gmean = math.exp(logsum/count)
        csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count}")
        with open(f"/mydata/workspace/jrapl/{args.tag}_stable-diffusion_{args.workload}.csv", "w") as f:
            f.write("\n".join(csvlines))