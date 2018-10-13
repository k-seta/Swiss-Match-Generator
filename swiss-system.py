#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import shutil
import random
import itertools
import numpy as np
import pandas as pd
from logging import getLogger, DEBUG, Formatter
from rainbow_logging_handler import RainbowLoggingHandler

#setting logger
logger = getLogger(__name__)
logger.setLevel(DEBUG)

handler = RainbowLoggingHandler(sys.stderr)
handler_format = Formatter('[%(asctime)s] %(pathname)s (%(module)s) - %(funcName)s:L%(lineno)d : %(message)s')
handler.setFormatter(handler_format)

logger.addHandler(handler)
logger.propagate = False

def generate_list_opponents(members, match_table):
    tmp = []
    table = list(itertools.izip_longest(*[iter(match_table)]*2))
    for p1, p2 in table:
        tmp.append((members.index(p2), p1))
        tmp.append((members.index(p1), p2))
    tmp.sort()
    opponents = zip(*tmp)[1]
    # logger.debug(str(opponents).decode("string-escape"))
    return opponents

def calc_match_score(win, lose):
    tmp = zip(win, lose)
    score = []
    for x in tmp:
        if x[0] > x[1]:
            score.append(3)
        elif x[0] == x[1]:
            score.append(1)
        else:
            score.append(0)
    return np.array(score)

if __name__ == "__main__":
    argv = sys.argv
    argc = len(sys.argv)

    if argc != 2:
        logger.error("Wrong number of launch arguments: requires 1, but got {}".format(argc-1))
        logger.warning("Usage: python swiss-system.py [path of tables.csv]")
        quit()

    path_csv = argv[1]
    if not os.path.isfile(path_csv):
        logger.error("Could not find file: {}".format(path_csv))
        quit()

    try:
        df = pd.read_csv(path_csv, index_col=0)
    except Exception as e:
        logger.error(type(e))
        logger.error(e.message)
        quit()

    if df.isnull().any().any():
        logger.error("Missing Values: {}".format(path_csv))
        quit()

    print len(df.columns)
    num_match = (len(df.columns) - 1 ) / 4.0
    if num_match < 0:
        logger.error("Invalid format: {}".format(path_csv))
        quit()
    elif num_match == 0:
        members = list(df["Name"])
        match_table = list(members)
        random.shuffle(match_table)
    else:
        members = list(df["Name"])
        rand = list(np.random.rand(len(members)))
        score = np.zeros(len(members))
        for i in range(int(num_match)):
            win = list(df["win_{}".format(int(num_match))])
            lose = list(df["lose_{}".format(int(num_match))])
            score += calc_match_score(win, lose)
        list_score_member = zip(score, rand, members)
        list_score_member.sort()
        sorted_score, sorted_rand, match_table = zip(*list_score_member)
        
    opponents = generate_list_opponents(members, match_table)
    df["opponent_{}".format(int(num_match)+1)] = opponents
    df["win_{}".format(int(num_match)+1)] = pd.np.nan
    df["lose_{}".format(int(num_match)+1)] = pd.np.nan
    df["draw_{}".format(int(num_match)+1)] = pd.np.nan
    print df
    df.to_csv(path_csv)
    shutil.copyfile(path_csv, "./docs/src/majerrabaine_cup.csv")