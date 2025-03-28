import transformers
import torch
import argparse
import time
import random
from transformers import VitsModel, AutoTokenizer
import scipy
import math

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
    args = parser.parse_args()


    model = VitsModel.from_pretrained("kakao-enterprise/vits-vctk")
    tokenizer = AutoTokenizer.from_pretrained("kakao-enterprise/vits-vctk")
    #tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    if args.workload == 'low':
        myprompt = prompts[1]
        bsize = 1
        arrivals = [7.624752770452206, 16.190036858722447, 17.00370428145268, 21.046930643697426, 32.7290542418688,
                    46.89003571139354, 50.806308226973954, 62.74582533005132, 65.07983098455777, 66.55366780211335,
                    67.62082959765667, 68.9412682453357, 78.07893956549961, 84.79160094701169, 97.45403525622741,
                    109.96499185998834, 116.44044291562132, 118.67437012597357, 120.1865710306716, 134.8816791216944,
                    140.08624164295816, 149.1901326927584, 149.92002837896368, 155.2121267841612, 162.71558597352492,
                    174.34769547468346, 176.1200175303397, 176.18430659685143, 184.38766900214037, 188.74852914758452,
                    196.709414310753, 202.75967382226187, 210.0804346694687, 218.25304046117023, 224.7095366944223,
                    228.50010410778563, 229.38898478230163, 230.580369668823, 237.1379091489234, 247.51333105683756,
                    251.945653456591, 255.25268454934698, 268.187589029482, 274.04407448383205, 278.4899386176682,
                    285.0112951871279, 285.32708767147193, 287.84715915453023, 301.33277393278877, 311.4109087691204,
                    312.322601233177, 318.04480700022697, 334.5126669417471, 351.71833783276537, 353.0834970767916,
                    353.08406743424354, 356.7293589514965, 373.58442783657586, 373.80422594889995, 374.7849658104915,
                    378.1093320143487, 384.8187152158549, 388.44399172284994, 389.1258944354256, 391.54935141974175,
                    396.6322155717727, 406.7535760541617, 416.37300736298073, 426.85343321673037, 427.83734246464365,
                    429.264663554099, 429.28922932172355, 431.1165263491252, 433.7242595373731, 435.04185001198476,
                    440.66368843883305, 446.0260397410169, 447.37937173436376, 448.06877677260815, 454.43657612113134,
                    457.0400678174948, 458.23158589840494, 460.62630306224537, 465.2115377197023, 467.1900164778615,
                    467.67811700164134, 467.7928497475567, 467.90044940389674, 468.9783796605125, 494.66257689968603,
                    497.2490146325136, 510.97314488955936, 514.6203265576905, 516.9868436729279, 517.6059160989514,
                    519.6988424623598, 525.1873736972385, 526.1280275769325, 527.0253952874666, 527.3729637933285,
                    527.5338735357536, 528.4838612171484, 528.5894488372452, 530.1666078327842, 534.4684708451556,
                    534.5116311113228, 539.935141967513, 541.1925330895065, 542.3561242357027, 542.963931785391,
                    543.7614214304699, 546.581142829592, 561.3432801779177, 567.8912586118951, 571.5717130504935,
                    571.8374364614037, 572.7045863056233, 582.3308834282814, 585.3059081459071, 588.9765679591112]
    elif args.workload == 'high':
        myprompt = prompts[3]
        bsize = 2
        arrivals = [105.1399, 299.3093, 311.5389, 347.7571, 368.8147, 412.6155, 448.3597]
    else:
        myprompt = prompts[random.randint(0,3)]
        bsize = random.randint(1,2)
        arrivals = [29.326290606546504, 214.21194210880896, 266.7356405120745, 331.53368036541065, 512.5682110586149]
    if (not args.downloadonly):
        begintime = time.time()
        curtime = begintime
        endtime = curtime + args.duration
        csvlines = []
        csvlines.append("Curtime,Elapsed")
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
                with torch.no_grad():
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
                with torch.no_grad():
                    output = model(**encodings).waveform
                elapsed = time.time() - t - begintime
                logsum += math.log(elapsed)
                total += elapsed
                count += 1
                csvlines.append(f"{curtime},{elapsed}")
        gmean = math.exp(logsum/count)
        csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count}")
        with open(f"/mydata/workspace/jrapl/{args.tag}_vits-ljs_{args.workload}.csv", "w") as f:
            f.write("\n".join(csvlines))