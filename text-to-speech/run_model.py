import transformers
import torch
import argparse
import time
import random
from transformers import VitsModel, AutoTokenizer
import scipy

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

    args = parser.parse_args()


    model = VitsModel.from_pretrained("kakao-enterprise/vits-vctk")
    tokenizer = AutoTokenizer.from_pretrained("kakao-enterprise/vits-vctk")
    #tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    if (not args.downloadonly):
        curtime = time.time()
        endtime = curtime + args.duration
        while curtime < endtime:
            if args.workload == 'low':
                myprompt = prompts[1]
                bsize = 1
            elif args.workload == 'high':
                myprompt = prompts[3]
                bsize = 2
            else:
                myprompt = prompts[random.randint(0,3)]
                bsize = random.randint(1,2)
            encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
            with torch.no_grad():
                output = model(**encodings).waveform
            elapsed = time.time() - curtime
            #time.sleep(elapsed*0.1)
            curtime = time.time()
