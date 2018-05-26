#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os
import data

from groot import yose

__author__ = 'Shawn Yan'
__date__ = '8:24 2018/5/26/026'


def get_file_logo(top_dir):
    """ find each file's logo name and return a dict
    """
    logo_file_dict = dict()
    try:
        fds = os.listdir(top_dir)
    except OSError:
        fds = list()
    for fd in fds:
        abs_fd = os.path.join(top_dir, fd)
        for logo, logo_pattern in data.PACKAGE_LOGOS.items():
            for p in logo_pattern:
                if p.search(fd):
                    logo_file_dict[logo] = abs_fd
                    break
            else:
                yose.say_it("Warning. Unknown file %s" % fd)
    return logo_file_dict





