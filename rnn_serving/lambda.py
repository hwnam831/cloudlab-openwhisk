import time
import psutil
import os
pid = os.getpid()
python_process = psutil.Process(pid)
memoryUse_old = 0
timeS1 = time.time()
import pickle
import numpy as np
import torch
import rnn
import string
memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
print('memory use 1:', memoryUse-memoryUse_old)

timeE1 = time.time()
print(timeE1 - timeS1)

torch.set_num_threads(1)
language = 'Scottish'
language2 = 'Russian'
start_letters = 'ABCDEFGHIJKLMNOP'
start_letters2 = 'QRSTUVWXYZABCDEF'

with open('/home/jovans2/apps/rnn_serving/rnn_params.pkl', 'rb') as pkl:
    params = pickle.load(pkl)

all_categories =['French', 'Czech', 'Dutch', 'Polish', 'Scottish', 'Chinese', 'English', 'Italian', 'Portuguese', 'Japanese', 'German', 'Russian', 'Korean', 'Arabic', 'Greek', 'Vietnamese', 'Spanish', 'Irish']
n_categories = len(all_categories)
all_letters = string.ascii_letters + " .,;'-"
n_letters = len(all_letters) + 1

rnn_model = rnn.RNN(n_letters, 128, n_letters, all_categories, n_categories, all_letters, n_letters)
rnn_model.load_state_dict(torch.load('/home/jovans2/apps/rnn_serving/rnn_model.pth'))
rnn_model.eval()

timeE2 = time.time()
memoryUse_old = memoryUse
memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
print('memory use 2:', memoryUse-memoryUse_old)
print(timeE2 - timeE1)

def main(params):
    startTime = time.time()
    output_names = list(rnn_model.samples(language, start_letters))
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 3:', memoryUse-memoryUse_old)
    print(time.time() - startTime)
    return output_names
    
