import torch
from diffusers import DiffusionPipeline
import argparse
import time
import random

configs = [
    {'prompt': 'realistic medieval castle downtown with soldiers and knights',
     'width' : 96,
     'height' : 96,
     'steps' : 50
    },
    {'prompt': 'higly detailed, majestic royal tall ship on a calm sea,realistic painting, \
    by Charles Gregory Artstation and Antonio Jacobsen and Edward Moran, (long shot), clear blue sky, \
    intricated details, 4k',
     'width' : 256,
     'height' : 256,
     'steps' : 40
    },
    {'prompt': 'I want to generate a group avatar for a Feishu group chat.\
    The role of this group is daily software technical communication. \
    Now the subject technology stacks that members of this group discuss daily include: \
    algorithms, data structures, optimization, functional programming, and the programming \
    languages often discussed are: TypeScript, Java, python, etc. \
    I hope this avatar has a simple aesthetic, this avatar is a single person avatar',
     'width' : 512,
     'height' : 512,
     'steps' : 20
    },
]

if __name__ == "__main__":
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
            if args.workload == 'low':
                myconfig = configs[0]
            elif args.workload == 'med':
                myconfig = configs[1]
            elif args.workload == 'high':
                myconfig = configs[2]
            else:
                myconfig = configs[random.randint(0,2)]
            image = pipeline(myconfig['prompt'],
                            width=myconfig['width'],
                            height=myconfig['height'],
                            num_inference_steps=myconfig['steps'])
            curtime = time.time()
    