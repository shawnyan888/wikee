#!/usr/bin/python  
# -*- coding: utf-8 -*-
"""
check builds recorded in history file  -- history_builds
check builds specified by customer     -- cc_builds
check builds for local lscc installed  -- cur_builds

will remove:
   a) not in cc_builds
   b) if total cur_builds number is larger than $max_build

remove the oldest build one by one.

"""
import os

__author__ = 'Shawn Yan'
__date__ = '14:53 2018/5/26/026'