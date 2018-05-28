#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os
import xData
import argparse

__author__ = 'Shawn Yan'
__date__ = '8:59 2018/5/26/026'


class Options(object):
    def __init__(self):
        self.default_packages = xData.DEFAULT_PACKS
        self.history_file = os.path.abspath("history_radiant.txt")

    def run_option_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--debug", action="store_true", help="print debug message and run flow 1 time")
        parser.add_argument("--rel", help="specify release path")
        parser.add_argument("--lscc", help="specify local Radiant install path")
        parser.add_argument("--packages", choices=xData.PACKAGE_LOGOS.keys(), nargs="+", help="specify package list")
        parser.add_argument("--email", help="specify notification Email address")
        parser.add_argument("--cc", help="specify central control configuration file")
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--standalone", action="store_true", help="install Radiant standalone")
        group.add_argument("--radiant", help="specify Radiant version to install")
        group.add_argument("--first", action="store_true", help="First run!")
        parser.set_defaults(rel=xData.REL_PATH,
                            lscc=xData.LSCC_PATH,
                            package=self.default_packages,
                            email=xData.EMAIL)
        opts = parser.parse_args()
        self.debug = opts.debug
        self.rel = opts.rel
        self.lscc = opts.lscc
        # Radiant should be installed with proper order
        self.packages = filter(lambda x: x in opts.packages, xData.PACKAGE_LOGOS.keys())
        self.email = opts.email
        self.cc = opts.cc
        self.standalone = opts.standalone
        self.radiant = opts.radian
        self.first = opts.first


if __name__ == "__main__":
    tst = Options()
    tst.run_option_parser()
    print tst.packages
