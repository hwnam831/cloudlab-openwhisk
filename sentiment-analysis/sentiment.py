# Copyright (c) 2019 Princeton University
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import sys
import json
import time
from textblob import TextBlob

def main(params):
    starttime = time.time()
    try:
        analyse = TextBlob(params['analyse'])
    except:
        return {'Error' : 'Input parameters should include a string to sentiment analyse.'}

    sentences = len(analyse.sentences)

    retVal = {}

    retVal["subjectivity"] = sum([sentence.sentiment.subjectivity for sentence in analyse.sentences]) / sentences
    retVal["polarity"] = sum([sentence.sentiment.polarity for sentence in analyse.sentences]) / sentences
    retVal["sentences"] = sentences
    endtime = time.time()
    retVal["time":endtime-starttime]


    return retVal
