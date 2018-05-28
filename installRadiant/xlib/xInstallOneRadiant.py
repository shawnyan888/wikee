#!/usr/bin/python  
# -*- coding: utf-8 -*-
"""Install a Radiant
1) try to create a folder for new Radiant for future use
2) check all install files in icd path and get logo for them
3) copy files to local path
4) try to install them
5) if no errors found, write success.ini file
"""
import os
import time
from groot import yose
import xTools
import xData

__author__ = 'Shawn Yan'
__date__ = '14:46 2018/5/26/026'


class InstallOneRadiant(object):
    def __init__(self, rel_path, lscc_path, radiant, packages):
        self.rel_path = rel_path
        self.lscc_path = lscc_path
        self.radiant = radiant
        self.packages = packages
        self.msg = ""

    def get_msg(self):
        return self.msg

    def process(self):
        yose.say_it(" Will install Radiant {} <{}>".format(self.radiant, time.ctime()))
        for func in (self.create_radiant_path,
                     self.get_package_files,
                     self.install_package_files,
                     self.create_successful_file):
            if func():
                break
        yose.say_it(" Exit for installing Radiant {} <{}>\n\n".format(self.radiant, time.ctime()))
        return self.msg

    def create_radiant_path(self):
        self.radiant_path = "{}/{}".format(self.lscc_path, self.radiant)
        if yose.wrap_md(self.radiant_path, "Radiant Path"):
            self.msg = "Failed to create folder %s" % self.radiant_path
            return 1

    def get_package_files(self):
        radiant_icd_path = "{0}/{1}/icd/{2}".format(self.rel_path, self.radiant,
                                                    "pc" if xData.ON_WIN else "lin")
        logo_file_dict = xTools.get_logo_file_dict(radiant_icd_path)
        self.package_files = [logo_file_dict.get(logo) for logo in self.packages]
        if None in self.package_files:
            self.msg = "Failed to find base/package files for %s" % self.packages
            return 1

    def install_package_files(self):
        pac_src_dst_files = [(pf, "{}/{}".format(self.radiant_path, os.path.basename(pf))) for pf in self.package_files]
        # Copy
        for (src, dst) in pac_src_dst_files:
            if yose.wrap_cp_file(src, dst):
                self.msg = "Failed to copy %s" % src
                return 1
        # Install
        for (src, dst) in pac_src_dst_files:
            cmd = "{} --console --prefix {}".format(dst, self.radiant_path)
            if yose.run_command(cmd, "{}/auto_install.log" % self.radiant_path):
                self.msg = "Failed to install %s" % dst
                return 1

    def create_successful_file(self):
        _file = "%s/success.ini" % self.radiant_path
        _lines = xData.SUCCESS_INI.format(self.radiant_path)
        if yose.write_file(_file, _lines):
            self.msg = "Failed to write success.ini file"