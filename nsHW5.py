#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 14:23:20 2021

@author: nidhisinha
"""

import sys, re
from nltk.stem.porter import PorterStemmer 
stemmer = PorterStemmer()

capitalpat = re.compile("[A-Z](\w)*")

def sentenceProcessor(sent, mode):
    ans = []
    for i, feature in enumerate(sent):
        nextfeat = feature 
        if i >= 1:
            nextfeat['PREV_POS'] = sent[i - 1]['POS']
            nextfeat['PREV_TOKEN'] = sent[i-1]['TOKEN']
            nextfeat['PREV_CAPITAL'] = sent[i-1]['IS_CAPITAL']
            if mode == 1:
                nextfeat['PREV_BIO'] = "@@"
        nextfeat['IS_FIRST'] = True if i == 0 else False 
        if i >= 2: 
            nextfeat['PREV_POS2'] = sent[i-2]['POS']
            nextfeat['PREV_CAPITAL2'] = sent[i-2]['IS_CAPITAL']
        if i <= len(sent) - 2: 
            nextfeat['NEXT_POS'] = sent[i+1]['POS']
            nextfeat['NEXT_TOKEN'] = sent[i+1]['TOKEN']
            nextfeat['NEXT_CAPITAL'] = sent[i+1]['IS_CAPITAL']
        if i <= len(sent) - 3: 
            nextfeat['NEXT_POS2'] = sent[i+2]['POS']
            nextfeat['NEXT_CAPITAL2'] = sent[i+2]['IS_CAPITAL']
        ans.append(nextfeat) 
    return ans 

def read(filename, mode):
    data = [] 
    sent = []
    currfeat = {} 
    with open(f'./{filename}', 'r') as inputfile:
        for i, line in enumerate(inputfile):
            tokens = line.strip("\n").split("\t")
            if (len(tokens) == 1):
                currfeat = {}
                sent = sentenceProcessor(sent, mode)
                data.append(sent)
                sent = []
                continue 
            token = tokens[0]
            stem = stemmer.stem(token)
            ext = token[len(stem):]
            currfeat = {"TOKEN": token, "POS": tokens[1], "STEM" : stem, "EXT" : ext} 
            if mode == 1:
                currfeat["BIO_TAG"] = tokens[2]
            currfeat["IS_CAPITAL"] = True if capitalpat.match(token) else False
            currfeat["TOKEN_LENGTH"] = len(token)
            sent.append(currfeat)
    return data 

def write(data, filename, mode):
    #print(len(data))
    sep = '\t'
    with open(f'./{filename}', 'w') as outputfile:
        d = data[1:]
        for sent in d:
            outputfile.write('\n')
            for feat in sent:
                s = []
                s.append(feat['TOKEN'])
                for key, value in feat.items():
                    if key == "TOKEN" or key == "BIO_TAG":
                        continue
                    s.append(f'{key}={value}')
                if mode == 1:
                    s.append(feat["BIO_TAG"])
                ans = sep.join(s)
                ans += '\n'
                outputfile.write(ans)
        outputfile.write('\n')
    return 

def main():
    mode = 1
    inputfiles = ["WSJ_02-21.pos-chunk", "WSJ_23.pos"]
    outputfiles = ["training.feature", "test.feature"]
    #inputfiles = ["WSJ_23.pos"]
    #outputfiles = ["test.feature"]
    for inputfile, outputfile in zip(inputfiles, outputfiles):
        #mode = 0
        print(inputfile, outputfile)
        data = read(inputfile, mode)
        write(data, outputfile, mode)
        mode = 0
    return 
main() 
