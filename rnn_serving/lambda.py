import time
import psutil
import os
import pickle
import numpy as np
import torch
import string
import torch
import torch.nn as nn
from torch.autograd import Variable
from minio import Minio

def getMinioClient(access, secret):
    return Minio(
        '10.10.1.1:9000',
        access_key = access,
        secret_key = secret,
        secure = False
    )

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, all_categories, n_categories, all_letters, n_letters):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size

        self.all_categories = all_categories
        self.n_categories = n_categories
        self.all_letters = all_letters
        self.n_letters = n_letters

        self.i2h = nn.Linear(n_categories + input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(n_categories + input_size + hidden_size, output_size)
        self.o2o = nn.Linear(hidden_size + output_size, output_size)
        self.dropout = nn.Dropout(0.1)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, category, input_tensor, hidden):
        input_combined = torch.cat((category, input_tensor, hidden), 1)
        hidden = self.i2h(input_combined)
        output = self.i2o(input_combined)
        output_combined = torch.cat((hidden, output), 1)
        output = self.o2o(output_combined)
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden

    def init_hidden(self):
        return Variable(torch.zeros(1, self.hidden_size))

    @staticmethod
    def gen_input_tensor(all_letters, n_letters, line):
        tensor = torch.zeros(len(line), 1, n_letters)
        for li in range(len(line)):
            letter = line[li]
            tensor[li][0][all_letters.find(letter)] = 1
        return tensor

    @staticmethod
    def gen_category_tensor(all_categories, n_categories, category):
        li = all_categories.index(category)
        tensor = torch.zeros(1, n_categories)
        tensor[0][li] = 1
        return tensor

    # Sample from a category and starting letter
    def sample(self, category, start_letter='A'):
        category_tensor = Variable(self.gen_category_tensor(self.all_categories, self.n_categories, category))
        input_tensor = Variable(self.gen_input_tensor(self.all_letters, self.n_letters, start_letter))
        hidden = self.init_hidden()

        output_name = start_letter

        max_length = 20
        for i in range(max_length):
            output, hidden = self.forward(category_tensor, input_tensor[0], hidden)
            topv, topi = output.data.topk(1)
            topi = topi[0][0]

            if topi == self.n_letters - 1:
                break
            else:
                letter = self.all_letters[topi]
                output_name += letter

            input_tensor = Variable(self.gen_input_tensor(self.all_letters, self.n_letters, letter))

        return output_name

    # Get multiple samples from one category and multiple starting letters
    def samples(self, category, start_letters='ABC'):
        for start_letter in start_letters:
            yield self.sample(category, start_letter)



def main(params):
    pid = os.getpid()
    python_process = psutil.Process(pid)
    memoryUse_old = 0
    timeS1 = time.time()
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 1:', memoryUse-memoryUse_old)
    tmp = '/tmp/'
    pkl_name = 'rnn_params.pkl'
    pth_name = 'rnn_model.pth'
    minioClient = getMinioClient("minioadmin", "minioadmin")

    minioClient.fget_object('testbucket', 'model/' + pkl_name, tmp+pkl_name)
    minioClient.fget_object('testbucket', 'model/' + pth_name, tmp+pth_name)

    timeE1 = time.time()
    print(timeE1 - timeS1)

    torch.set_num_threads(1)
    language = 'Scottish'
    language2 = 'Russian'
    start_letters = 'ABCDEFGHIJKLMNOP'
    start_letters2 = 'QRSTUVWXYZABCDEF'
    
    with open(tmp+pkl_name, 'rb') as pkl:
        params = pickle.load(pkl)

    all_categories =['French', 'Czech', 'Dutch', 'Polish', 'Scottish', 'Chinese', 'English', 'Italian', 'Portuguese', 'Japanese', 'German', 'Russian', 'Korean', 'Arabic', 'Greek', 'Vietnamese', 'Spanish', 'Irish']
    n_categories = len(all_categories)
    all_letters = string.ascii_letters + " .,;'-"
    n_letters = len(all_letters) + 1

    rnn_model = RNN(n_letters, 128, n_letters, all_categories, n_categories, all_letters, n_letters)
    rnn_model.load_state_dict(torch.load(tmp+pth_name))
    rnn_model.eval()

    timeE2 = time.time()
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 2:', memoryUse-memoryUse_old)
    print(timeE2 - timeE1)
    startTime = time.time()
    output_names = list(rnn_model.samples(language, start_letters))
    memoryUse_old = memoryUse
    memoryUse = python_process.memory_info()[0]/2.**30  # memory use in GB...I think
    print('memory use 3:', memoryUse-memoryUse_old)
    print(time.time() - startTime)
    return {'output':output_names, 'time':time.time()-startTime}
    
