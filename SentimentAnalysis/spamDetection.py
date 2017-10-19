#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 21:02:47 2017

@author: korda
"""

import pandas as pd
import numpy as np

dataset1 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube01-Psy.csv', sep=',')
dataset2 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube02-KatyPerry.csv', sep=',')
dataset3 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube03-LMFAO.csv', sep=',')
dataset4 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube04-Eminem.csv', sep=',')
dataset5 = pd.read_csv('./YouTube-Spam-Collection-v1/Youtube05-Shakira.csv', sep=',')

dataset1 = dataset1.iloc[:,3:]
dataset2 = dataset2.iloc[:,3:]
dataset3 = dataset3.iloc[:,3:]
dataset4 = dataset4.iloc[:,3:]
dataset5 = dataset5.iloc[:,3:]


