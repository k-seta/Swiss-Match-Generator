#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import random
import itertools
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
    for p1, p2 in match_table:
        tmp.append((members.index(p2), p1))
        tmp.append((members.index(p1), p2))
    tmp.sort()
    opponents = zip(*tmp)[1]
    logger.debug(str(opponents).decode("string-escape"))
    return opponents

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
        df = pd.read_csv(path_csv)
        print df
    except Exception as e:
        logger.error(type(e))
        logger.error(e.message)
        quit()

    num_match = (len(df.columns) - 1 ) / 2.0
    if num_match < 0:
        logger.error("Invalid format: {}".format(path_csv))
        quit()
    elif num_match == 0:
        members = list(df[df.columns[0]])
        members_shuffle = list(members)
        random.shuffle(members_shuffle)

        match_table = list(itertools.izip_longest(*[iter(members_shuffle)]*2))
        opponents = generate_list_opponents(members, match_table)
        df["opponent_1"] = opponents
    df.to_csv(path_csv,index=None)