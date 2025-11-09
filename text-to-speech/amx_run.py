import transformers
import torch
import argparse
import time
import random
from transformers import VitsModel, AutoTokenizer
import scipy
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

prompts = [
        "VITS is an end-to-end speech synthesis model that predicts a speech waveform conditional on an input text sequence.",
        "Advancements in technology continue to make our lives easier, transforming the way we communicate, work, and learn every day.",
        """A set of spectrogram-based acoustic features are predicted by the flow-based module, 
        which is formed of a Transformer-based text encoder and multiple coupling layers. 
        The spectrogram is decoded using a stack of transposed convolutional layers, 
        much in the same style as the HiFi-GAN vocoder. Motivated by the one-to-many nature of the TTS problem, 
        where the same text input can be spoken in multiple ways, the model also includes a stochastic duration predictor, 
        which allows the model to synthesise speech with different rhythms from the same input text.""",
        """I have a dream that one day, we will live in a world where equality and justice are not just ideals 
        but realities that we practice in our everyday lives. I dream of a time when people are no longer judged 
        by the color of their skin, their gender, or their socioeconomic status, but by the content of their character, 
        the strength of their convictions, and the depth of their compassion.
        In my dream, children from all walks of life grow up in a society that nurtures
        their potential and celebrates their uniqueness. They are not confined by the limits of prejudice or discrimination, 
        but are encouraged to explore their talents and pursue their passions. 
        Schools are safe havens of learning where curiosity is cultivated, critical thinking is encouraged, 
        and diversity is celebrated. Every child, regardless of their background, has access to quality education, 
        healthcare, and opportunities that allow them to flourish.
        I dream of a world where our differences are not just tolerated but embraced, where cultural diversity 
        is seen as a strength rather than a threat. In this world, people from different cultures, religions, 
        and ethnicities come together to learn from one another, to share their stories, and to build bridges of 
        understanding. There is a collective commitment to peace and nonviolence, to resolving conflicts through 
        dialogue rather than division, and to lifting each other up rather than tearing each other down.
        """,
        """In my dream, children from all walks of life grow up in a society that nurtures their potential and celebrates their uniqueness. They are not confined by the limits of prejudice or discrimination, but are encouraged to explore their talents and pursue their passions. Schools are safe havens of learning where curiosity is cultivated, critical thinking is encouraged, and diversity is celebrated. Every child, regardless of their background, has access to quality education, healthcare, and opportunities that allow them to flourish.
        I dream of a world where our differences are not just tolerated but embraced, where cultural diversity is seen as a strength rather than a threat. In this world, people from different cultures, religions, and ethnicities come together to learn from one another, to share their stories, and to build bridges of understanding. There is a collective commitment to peace and nonviolence, to resolving conflicts through dialogue rather than division, and to lifting each other up rather than tearing each other down.
        And yet, this is not a dream that we can simply wait for. It is a dream that demands our action, our courage, and our unwavering commitment. I dream of a day when we become the architects of this better world, when we work tirelessly to dismantle the systems of oppression and inequality that hold us back. I dream that we will have leaders who are guided by wisdom and integrity, who understand that their power is a sacred trust to serve the people, not to control them.
        My dream is for a world where every voice matters, where the meek have a platform, and where the marginalized are brought to the center of our shared humanity. Let us not be satisfied with the status quo. Let us not allow the cynics to extinguish the flame of our hope. Let us move forward with a fierce and unrelenting faith in our ability to create a future that is not just possible, but inevitable. A future where this dream is no longer a distant vision, but the tangible, beautiful reality we all live in.
        """
    ]

configs = [
    {'prompt': [prompts[0]],
     'max_new_tokens' : 30

    },
    {'prompt': [prompts[1]]*2,
     'max_new_tokens' : 30
    },
    {'prompt': [prompts[2]]*4,
     'max_new_tokens' : 30
    },
]

patterns = {
    'high' : [[105.1399, 299.3093, 311.5389, 368.8147, 412.6155, 448.3597],
              [6.4885, 80.2350, 198.5696, 224.2007, 389.9425, 533.4843],
              [0.0, 70.6441, 79.4753, 397.9972, 447.3245, 551.7109],
              [42.4098, 254.8486, 326.1932, 329.0888, 528.4175, 564.6664]],       
}

if __name__ == "__main__":
    random.seed(16)
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
    parser.add_argument(
        "--config", type=int, default=1,choices=[1,2,3,4], help="Arrival trace choice"
    )
    args = parser.parse_args()


    model = VitsModel.from_pretrained("kakao-enterprise/vits-vctk")
    tokenizer = AutoTokenizer.from_pretrained("kakao-enterprise/vits-vctk")
    #tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    if args.workload == 'high':
        myprompt = prompts[3]
        bsize = 2
        arrivals = PoissonGen(0.04, args.duration, args.config+7)
    elif args.workload == 'low':
        myprompt = prompts[2]
        bsize = 1
        arrivals = PoissonGen(0.1, args.duration, args.config+31)
    elif args.workload == 'med':
        myprompt = prompts[2]
        bsize = 1
        arrivals = PoissonGen(0.03, args.duration, args.config+13)
    else:
        myprompt = prompts[random.randint(0,3)]
        bsize = random.randint(1,2)
        arrivals = [29.326290606546504, 214.21194210880896, 266.7356405120745, 331.53368036541065, 512.5682110586149]
    if (not args.downloadonly):
        begintime = time.time()
        curtime = begintime
        endtime = curtime + args.duration
        csvlines = []
        csvlines.append("Curtime,Elapsed,Batchsize")
        '''
        while curtime < endtime:
            encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
            with torch.no_grad():
                output = model(**encodings).waveform
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
                encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
                with torch.autocast(device_type="cpu", dtype=torch.bfloat16):
                    output = model(**encodings).waveform
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
                encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
                with torch.autocast(device_type="cpu", dtype=torch.bfloat16):
                    output = model(**encodings).waveform
                elapsed = time.time() - t - begintime
                logsum += math.log(elapsed)
                total += elapsed
                count += 1
                csvlines.append(f"{curtime},{elapsed},{bsize}")
        gmean = math.exp(logsum/count)
        #csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count},{bsize}")
        with open(f"/mydata/workspace/jrapl/{args.tag}_vits-ljs_{args.workload}.csv", "w") as f:
            f.write("\n".join(csvlines))