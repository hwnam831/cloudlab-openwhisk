import torch
from diffusers import DiffusionPipeline
import argparse
import time
import random

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

    args = parser.parse_args()
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", use_safetensors=True)
    if (not args.downloadonly):
        curtime = time.time()
        endtime = curtime + args.duration
        while curtime < endtime:
            myprompt = prompts[random.randint(0,2)]
            if args.workload == 'low':
                myres = res_low[2]
                steps = 5
            elif args.workload == 'high':
                myres = res_high[2]
                steps = 5
            else:
                myres = res_high[random.randint(0,2)]
                steps = 5
            image = pipeline(myprompt,
                            width=myres,
                            height=myres,
                            num_inference_steps=steps)
            elapsed = time.time() - curtime
            time.sleep(elapsed*0.1)
            curtime = time.time()
    