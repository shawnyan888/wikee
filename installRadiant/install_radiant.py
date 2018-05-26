#!/usr/bin/python  
# -*- coding: utf-8 -*-
import os
import time
from xlib import xOptions
from xlib import xTools
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
                self.flow_remove_radiant()
                self.flow_install_radiant()
                time.sleep(self.gap_time)
        return sts

    def write_first_history(self):
        green_builds = xTools.get_green_builds(self.rel)
        return yose.write_file(self.history_file, ["{},{}".format(item, time.ctime()) for item in green_builds], append=False)

    def _install_radiant(self, radiant):
        yose.say_it("Will install Radiant {} <{}>".format(radiant, time.ctime()))
        _recov = yose.ChangeDir(self.lscc)
        radiant_path = "%s/%s" % (self.lscc, radiant)

        _recov.comeback()

    def flow_remove_radiant(self):
        pass

    def flow_install_radiant(self):
        pass

if __name__ == "__main__":
    my_ins = InstallRadiant()
    my_ins.process()
