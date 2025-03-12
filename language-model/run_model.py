import transformers
import torch
import argparse
import time
import random
from transformers import AutoModelForCausalLM, AutoTokenizer
import math

prompts = [
        # For these prompts, the expected answer is the natural continuation of the prompt
        "I believe the meaning of life is",
        """Translate English to French:

        sea otter => loutre de mer
        peppermint => menthe poivrée
        plush girafe => girafe peluche
        cheese => fromage
        whale => baleine
        shark => requin
        octopus =>""",
        # Few shot prompt (providing a few examples before asking model to complete more);
        """Paris, the capital of France, is known for its stunning architecture, art museums, historical landmarks, and romantic atmosphere. Here are some of the top attractions to see in Paris:

        1. The Eiffel Tower: The iconic Eiffel Tower is one of the most recognizable landmarks in the world and offers breathtaking views of the city.
        2. The Louvre Museum: The Louvre is one of the world's largest and most famous museums, housing an impressive collection of art and artifacts, including the Mona Lisa.
        3. Notre-Dame Cathedral: This beautiful cathedral is one of the most famous landmarks in Paris and is known for its Gothic architecture and stunning stained glass windows.
        If I were to plan a three-day trip to Paris, my plan would be
        """,
        """Antibiotics are a type of medication used to treat bacterial infections. 
        They work by either killing the bacteria or preventing them from reproducing, 
        allowing the body’s immune system to fight off the infection. Antibiotics are usually 
        taken orally in the form of pills, capsules, or liquid solutions, or sometimes administered intravenously. 
        They are not effective against viral infections, and using them inappropriately can lead to antibiotic resistance.
        Explain the above in two sentences: """
    ]

configs = [
    {'prompt': prompts[0],
     'max_new_tokens' : 20

    },
    {'prompt': [prompts[1]]*8,
     'max_new_tokens' : 20
    },
    {'prompt': [prompts[2]]*16,
     'max_new_tokens' : 20
    },
]

new_tokens=10

if __name__ == "__main__":
    random.seed(17)
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

    args = parser.parse_args()
    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    model = AutoModelForCausalLM.from_pretrained(
	model_id, device_map="cpu", torch_dtype=torch.float32)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    csvlines = []
    csvlines.append("Curtime,Elapsed")
    if (not args.downloadonly):
        if args.workload == 'low':
            myprompt = prompts[1]
            bsize = 2
            new_tokens=20
            arrivals = [0.0, 88.35571434352617, 89.02003794489113,
                        132.5127269873638, 174.63380813188067, 321.55113336674253,
                        543.5219121929915, 564.961992132476]
        elif args.workload == 'high':
            myprompt = prompts[2]
            bsize = 8
            new_tokens=10
            arrivals = [0.0, 54.869902600932996, 233.14789809492828,
                        249.080560505403, 542.5364127881884]
        else:
            myprompt = prompts[1]
            bsize = 2
            new_tokens=20
            arrivals = [0.0, 88.35571434352617, 89.02003794489113,
                        132.5127269873638, 174.63380813188067, 321.55113336674253,
                        543.5219121929915, 564.961992132476]
        begintime = time.time()
        curtime = begintime
        endtime = curtime + args.duration
        '''
        while curtime < endtime:
            encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
            with torch.no_grad():
                output = model.generate(encodings['input_ids'], max_new_tokens=new_tokens)
            elapsed = time.time() - curtime
            csvlines.append(f"{curtime-begintime},{elapsed}")
            time.sleep(elapsed*args.idle)
            curtime = time.time()
        '''
        logsum = 0
        total = 0
        count = 0
        for t in arrivals:
            curtime = time.time() - begintime
            if t > args.duration:
                break
            if curtime < t:
                time.sleep(t-curtime)
            encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
            with torch.no_grad():
                output = model.generate(encodings['input_ids'], max_new_tokens=new_tokens)
            elapsed = time.time() - t - begintime
            logsum += math.log(elapsed)
            total += elapsed
            count += 1
            csvlines.append(f"{curtime},{elapsed}")
        gmean = math.exp(logsum/count)
        csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count}")
        with open(f"/mydata/workspace/jrapl/{args.tag}_llama-3.1-8b_{args.workload}.csv", "w") as f:
            f.write("\n".join(csvlines))