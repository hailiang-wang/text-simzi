#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
#
# Copyright (c) 2017 <> All Rights Reserved
#
#
# File: /Users/hain/ai/text-simzi/app/preprocess.py
# Author: Hai Liang Wang
# Date: 2018-03-27:16:07:21
#
#===============================================================================

"""
   
"""
from __future__ import print_function
from __future__ import division

__copyright__ = "Copyright (c) 2017 . All Rights Reserved"
__author__    = "Hai Liang Wang"
__date__      = "2018-03-27:16:07:21"


import os
import sys
curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curdir)

if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    # raise "Must be using Python 3"

# Get ENV
ENVIRON = os.environ.copy()

from absl import flags   #absl-py
from absl import logging #absl-py

import unittest
from utils import is_zh, any2unicode
from pypinyin import pinyin, lazy_pinyin, Style
from tqdm import tqdm

FLAGS = flags.FLAGS


def get_char_py(s, heteronym=True):
    p = pinyin(s, heteronym=heteronym)
    if len(p) > 0 and len(p[0]) > 0:
        return p[0]
    raise BaseException("get_char_py(%s) Error: %s"  % (s, p))

# run testcase: python /Users/hain/ai/text-simzi/app/preprocess.py Test.testExample
class Test(unittest.TestCase):
    '''
    
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_pinyin(self):
        print("test_get_pinyin")
        s = "Python 3(Python 2 下把 '中心' 替换为 u'中心' 即可):"
        for x in any2unicode(s):
            if is_zh(x): print(x, " ".join(get_char_py(x)))

    def test_load_sim_pinyin(self):
        print("test_load_sim_pinyin")
        from_ = os.path.join(curdir, os.path.pardir, "tmp", "sim_pinyin.utf8.txt")
        ct = 0
        ct_i = 0
        with open(from_, "r") as fin:
            for x in fin.readlines():
                x = x.strip().split("\t")
                if len(x) > 1:
                    print("pinyin: %s| %s" % (x[0], " ".join(x[1::])))
                    ct += len(x[1::])
                ct_i += 1
        print("count total char:", ct, ", pinyin: ", ct_i)

    def test_sim_pinyin(self):
        logging.info("test_sim_pinyin")
        from_ = os.path.join(curdir, os.path.pardir, "data", "vocab.txt")
        to_ = os.path.join(curdir, os.path.pardir, "tmp", "sim_pinyin.utf8.txt")
        result = dict()

        with open(from_, "r") as fin:
            for x in tqdm(fin.readlines()):
                for y in any2unicode(x):
                    if not y: continue
                    if not is_zh(y): continue
                    for z in get_char_py(y): # 多音字
                        if not z in result:
                            result[z] = set()

                        result[z].add(y)

        print(len(result.keys()))
        with open(to_, "w") as fout:
            for (x,y) in result.items():
                fout.write("%s\t%s\n" % (x, "\t".join(list(y))))
                # print(x, " ".join(list(y)))
                # break

def test():
    unittest.main()

if __name__ == '__main__':
    FLAGS([__file__, '--verbosity', '1']) # DEBUG 1; INFO 0; WARNING -1
    test()
