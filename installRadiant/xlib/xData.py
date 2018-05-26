#!/usr/bin/python  
# -*- coding: utf-8 -*-
import re
import sys
import collections

__author__ = 'Shawn Yan'
__date__ = '16:09 2018/5/25'

ON_WIN = sys.platform.startswith("win")

# Radiant Release Path
rel_path_win = "//192.168.48.104/home/rel"
rel_path_lin = "/home/rel"
REL_PATH = rel_path_win if ON_WIN else rel_path_lin

# Radiant Install Path
lscc_path_win = "d:/radiant_auto"
lscc_path_lin = "/lsh/sw/qa/qadata/radiant/lin"
LSCC_PATH = lscc_path_win if ON_WIN else lscc_path_lin

# install file package logo dictionary
PACKAGE_LOGOS = collections.OrderedDict([
    ("base", [re.compile("Radiant_x64")]),
    ("epic", [re.compile("Ctrl_Pack_EPIC")]),
    ("jedi", [re.compile("Ctrl_Pack_JEDI")]),
    ("power", [re.compile("PowerEstimator")]),
    ("program_security", [re.compile("Radiant_Programmer_Security")]),
    ("program", [re.compile("Radiant_Programmer")]),
    ("reveal", [re.compile("Radiant_Reveal")]),
    ("security", [re.compile("Radiant_Security")]),
])

EMAIL = "shawn.yan@latticesemi.com"