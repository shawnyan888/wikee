#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os
import time
from xlib import xOptions
from xlib import xTools
from xlib import xInstallOneRadiant
from groot import yose

__author__ = 'Shawn Yan'
__date__ = '8:25 2018/5/26/026'


class InstallRadiant(xOptions.Options):
    def __init__(self):
        super(InstallRadiant, self).__init__()
        self.gap_time = 180
        self.idle_time_range = range(120, 1200)

    def process(self):
        self.run_option_parser()
        sts = 0
        if self.first or not os.path.isfile(self.history_file):
            sts = self.write_first_history()
        if self.radiant:
            sts = self._install_radiant(self.radiant)
        if self.standalone:
            while True:
                try:
                    self.flow_remove_radiant()
                    self.flow_install_radiant()
                except:
                    yose.say_tb()
                time.sleep(self.gap_time)
        return sts

    def write_first_history(self):
        gbs = xTools.get_green_builds(self.rel)
        return yose.write_file(self.history_file, ["{},{},Initial".format(item, time.ctime()) for item in gbs])

    def _install_radiant(self, radiant):
        my_install = xInstallOneRadiant.InstallOneRadiant(self.rel, self.lscc, radiant, self.packages)
        my_install.process()
        msg = my_install.get_msg()
        msg_str = msg if msg else "OK"
        yose.write_file(self.history_file, "{},{},{}".format(radiant, time.ctime(), msg_str), append=True)
        return msg

    def flow_remove_radiant(self):
        pass

    def flow_install_radiant(self):
        pass

if __name__ == "__main__":
    my_ins = InstallRadiant()
    my_ins.process()
