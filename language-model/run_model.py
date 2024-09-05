import transformers
import torch
import argparse
import time
import random
from transformers import AutoModelForCausalLM, AutoTokenizer

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

    args = parser.parse_args()
    model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"

    model = AutoModelForCausalLM.from_pretrained(
	model_id, device_map="cpu", torch_dtype=torch.float32)
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    if (not args.downloadonly):
        curtime = time.time()
        endtime = curtime + args.duration
        while curtime < endtime:
            if args.workload == 'low':
                myprompt = prompts[random.randint(0,1)]
                bsize = 4
            elif args.workload == 'high':
                myprompt = prompts[random.randint(2,3)]
                bsize = 16
            else:
                myprompt = configs[random.randint(0,3)]
                bsize = random.randint(4,16)
            encodings = tokenizer([myprompt]*bsize, return_tensors="pt")
            with torch.no_grad():
                output = model.generate(encodings['input_ids'], max_new_tokens=20)
            curtime = time.time()
    