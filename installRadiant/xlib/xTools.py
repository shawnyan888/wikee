#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import glob
import xData

from groot import yose

__author__ = 'Shawn Yan'
__date__ = '8:24 2018/5/26/026'


def _map_logo(abs_file):
    for logo, logo_patterns in xData.PACKAGE_LOGOS.items():
        for p in logo_patterns:
            if p.search(os.path.basename(abs_file)):
                return logo
    yose.say_it("Warning. Unknown install file: %s" % abs_file)


def get_logo_file_dict(radiant_icd_path):
    """ find each file's logo name and return a dict
    """
    try:
        fds = os.listdir(radiant_icd_path)
    except OSError:
        fds = list()
    abs_fds = [os.path.join(radiant_icd_path, item) for item in fds]
    return dict(zip(map(_map_logo, abs_fds), map(yose.win2unix, abs_fds)))


def get_green_builds(rel_path):
    eb_str = "eit/BuildGREEN"
    p_build = re.compile("/(ng.+?)/%s" % eb_str)
    green_files = glob.glob("{}/ng*/{}".format(rel_path, eb_str))
    green_files.sort()
    return [p_build.search(item).group(1) for item in green_files]

