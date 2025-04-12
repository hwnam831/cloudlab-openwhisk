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

patterns = {
    'high' : [[8.0313, 192.5857, 354.1262, 385.5167, 464.6160, 565.5796],
              [23.2249, 65.8364, 100.2305, 417.1087, 436.6336, 542.9643, 574.1780],
              [89.4954, 197.1510, 279.1672, 295.2953, 308.3088, 405.6035, 524.0012],
              [20.1468, 59.9922, 83.3614, 129.3731, 428.1551, 520.7822, 585.8331]],
    'low' : [[0.0, 88.35571434352617, 89.02003794489113,132.5127269873638, 
              174.63380813188067, 321.55113336674253,543.5219121929915, 564.961992132476],
              [15.8339, 141.1562, 147.5333, 242.5866, 339.0783, 464.7911, 495.2243, 504.9494],
              [33.9019, 181.5147, 194.2174, 227.4718, 335.7596, 395.4141, 435.7351, 454.0246],
              [18.4423, 41.7540, 88.1744, 125.8823, 177.1112, 227.2783, 389.7754, 401.6363, 531.8213]]         
}

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
        "--config", type=int, default=1,choices=[1,2,3,4], help="Arrival trace choice"
    )
    parser.add_argument(
        "--downloadonly",
        action="store_true"
    )

    parser.add_argument(
        "--continuous",
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
    csvlines.append("Curtime,Elapsed,Batchsize")
    if (not args.downloadonly):
        if args.workload == 'low':
            myprompt = prompts[1]
            bsize = 2
            new_tokens=20
            arrivals = patterns['low'][args.config-1]
        elif args.workload == 'high':
            myprompt = prompts[2]
            bsize = 8
            new_tokens=10
            arrivals = patterns['high'][args.config-1]
        elif args.workload == 'med':
            myprompt = prompts[1]
            bsize = 2
            new_tokens=15
            arrivals = patterns['low'][args.config%4]
        else:
            myprompt = prompts[1]
            bsize = 2
            new_tokens=20
            arrivals = patterns['low'][args.config-1]
        begintime = time.time()
        curtime = begintime
        endtime = curtime + args.duration
        logsum = 0
        total = 0
        count = 0
        if args.continuous:
            while curtime < endtime:
                encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
                with torch.no_grad():
                    output = model.generate(encodings['input_ids'], max_new_tokens=new_tokens)
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
                    bsize = 3 + (cnt%2)*3
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
                csvlines.append(f"{curtime},{elapsed},{bsize}")
        gmean = math.exp(logsum/count)
        #csvlines.append(f"Geometric Mean,{gmean}")
        csvlines.append(f"Average,{total/count},{bsize}")
        with open(f"/mydata/workspace/jrapl/{args.tag}_llama-3.1-8b_{args.workload}.csv", "w") as f:
            f.write("\n".join(csvlines))