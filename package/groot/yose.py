#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import time
import stat
import shutil
import ConfigParser
import fnmatch
import platform
import traceback

__author__ = 'Shawn Yan'
__date__ = '10:09 2018/5/16'


# /****************************
# General wrapper functions
def say_it(msg, comments="", show=1, log_key="Y_O_S_E_L_O_G"):
    """Wrapper of print
    """
    if not show:
        return
    try:
        log = open(os.getenv(log_key), "a")
    except (TypeError, IOError):
        log = ""

    def _dump_it(notes):
        notes = str(notes)
        if log:
            print >> log, notes
        print(notes)

    if comments:
        _dump_it(comments)
    if isinstance(msg, str):
        _dump_it(msg)
    elif isinstance(msg, list) or isinstance(msg, tuple):
        for item in msg:
            _dump_it("  - %s" % str(item))
    elif isinstance(msg, dict):
        msg_keys = msg.keys()
        try:
            msg_keys.sort(key=str.lower)
        except (AttributeError, TypeError):
            msg_keys.sort()
        for key in msg_keys:
            value = msg.get(key)
            _dump_it("  - %-20s: %s" % (str(key), str(value)))
    else:
        _dump_it(msg)
    if log:
        log.close()


def say_tb(comments=""):
    """Print out traceback message
    """
    say_it(traceback.format_exc(), comments)


def get_machine_name():
    """Get machine name
    """
    machine_name = platform.uname()[1]
    machine_name = re.split("\.", machine_name)
    return machine_name[0]


def pause(log=""):
    """ wrapper of pause by raw_input
    """
    if not log:
        log = time.ctime() + ">>"
    raw_input(log)


def split_list_with_window(a_list, window=5):
    """Split a list with window
    """
    return [a_list[x:x+window] for x in range(0, len(a_list), window)]


class GetFiles(object):
    """Get files from a folder
    """
    def __init__(self, file_patterns, func=None, skip_folder_patterns=(".svn", "rev_1", "*.dir")):
        self.file_patterns = file_patterns
        self.func = func
        self.skip_folder_patterns = skip_folder_patterns
        self.files = list()

    def search_folder(self, root):
        for foo in os.listdir(root):
            abs_foo = os.path.join(root, foo)
            if os.path.isdir(abs_foo):
                if _fn_match(foo, self.skip_folder_patterns):
                    pass
                else:
                    self.search_folder(abs_foo)
            else:
                if _fn_match(foo, self.file_patterns):
                    self.files.append(abs_foo)
                    if self.func:
                        self.func(abs_foo)

    def get_files(self):
        return self.files


class ChangeDir:
    """Change the current working directory to a new path.
    and can come back to the original current working directory
    """
    def __init__(self, new_path):
        self.cur_dir = os.getcwd()
        os.chdir(new_path)

    def comeback(self):
        os.chdir(self.cur_dir)


class ElapsedTime:
    """
    get elapsed time and timestamp
    """
    def __init__(self):
        self.etime = 0
        self.play()

    def play(self):
        self.start_time = time.time()

    def stop(self):
        self.etime = time.time() - self.start_time
        self.start_time = time.time()

    def get_etime(self):
        return self.etime

    def __str__(self):
        self.etime = time.time() - self.start_time
        return "Elapsed Time: %.2f seconds" % self.etime


class AppConfig(ConfigParser.ConfigParser):
    def __init__(self):
        ConfigParser.ConfigParser.__init__(self)

    def optionxform(self, optionstr):
        """
        re-define optionxform, in the release version, return optionstr.lower()
        """
        return optionstr


def get_conf_options(conf_files, key_lower=True):
    """
    get configuration from conf_files, conf_files can be a file or a file list
    all option will not change the case when key_lower is False
    """
    # use <xx> <yy> ... to specify a list string for an option.
    conf_options = dict()
    if key_lower:
        conf_parser = ConfigParser.ConfigParser()
    else:
        conf_parser = AppConfig()
    try:
        conf_parser.read(conf_files)
        for section in conf_parser.sections():
            t_section = dict()
            for option in conf_parser.options(section):
                value = conf_parser.get(section, option)
                t_section[option] = value
            conf_options[section] = t_section
    except:
        say_tb("Failed to parse file(s): %s" % conf_files)
    return conf_options


def write_file(a_file, lines, append=False):
    """
    append a file or create a new file if append=False
    """
    try_times = 1
    a_file = os.path.abspath(a_file)
    while True:
        try:
            aw = "a" if append else "w"
            with open(a_file, aw) as a_ob:
                if type(lines) is str:
                    print >> a_ob, lines
                else:
                    for item in lines:
                        print >> a_ob, item
            break
        except IOError:
            try_times += 1
            if try_times > 10:
                say_it("-- Error: can not open %s" % a_file)
                return 1
            time.sleep(5)
            say_it("-- Note: try to open %s %d times." % (a_file, try_times))


def get_status_output(cmd):
    """
    return (status, output) of executing cmd in a shell.
    source from commands.py <def getstatusoutput(cmd)>.
    """
    on_win = (sys.platform[:3] == "win")
    if not on_win:
        cmd = "{ " + cmd + "; }"
    pipe = os.popen(cmd + " 2>&1", "r")
    text = pipe.read()
    sts = pipe.close()
    if sts is None:
        sts = 0
    if text[-1:] == '\n':
        text = text[:-1]
    return sts, text


def run_command(cmd, log_file=None, time_file=None):
    etime = ElapsedTime()
    say_it(" Running %s <%s>" % (cmd, time.ctime()))
    sts, text = get_status_output(cmd)
    if log_file or time_file:
        timestamp_lines = [">> {} <{}>".format(cmd, time.ctime()), etime]
        if log_file:
            write_file(log_file, timestamp_lines + [text], append=True)
        if time_file:
            write_file(time_file, timestamp_lines, append=True)


def get_file_line_count(a_file):
    """Get the line number of a file
    """
    count = -1
    try:
        for count, line in enumerate(open(a_file, "rU")):
            pass
    except IOError:
        pass
    count += 1
    return count


def win2unix(a_path, use_abs=0):
    """
    transfer a path to unix format
    """
    if use_abs:
        a_path = os.path.abspath(a_path)
    return re.sub(r"\\", "/", a_path)


def to_abs_list(a_value, root_path):
    """
    get the absolute path for value(s) in root_path
    """
    t = ChangeDir(root_path)
    if type(a_value) is str:
        _value = [a_value]
    else:
        _value = a_value[:]
    _value = [win2unix(item) for item in _value]
    t.comeback()
    return _value


def not_exists(a_path, comments):
    """
    return 1 if a_path not exists
    """
    if not a_path:
        say_it("-- Error. No value specified for %s" % comments)
        return 1
    if not os.path.exists(a_path):
        say_it("-- Warning. Not found %s <%s> in %s" % (a_path, comments, os.getcwd()))
        return 1


def wrap_md(a_path, comments):
    """
    return 1 if failed to make a new folder if it doesn't exist
    """
    if not a_path:
        say_it("-- Error. No value specified for %s" % comments)
        return 1
    if not os.path.isdir(a_path):
        try:
            os.makedirs(a_path)
        except Exception, e:
            say_it("-- Error. can not makedir %s <%s>" % (a_path, comments))
            say_it(e)
            say_it("")
            return 1


def wrap_cp_file(src, dst, force=True):
    """
    copy a file
    """
    abs_src = os.path.abspath(src)
    abs_dst = os.path.abspath(dst)
    if abs_src == abs_dst:
        return

    try:
        if os.path.isfile(abs_dst):
            if not force:
                return
            os.chmod(abs_dst, stat.S_IRWXU)
            os.remove(abs_dst)
        shutil.copy2(abs_src, abs_dst)
    except Exception, e:
        say_it("- Error. Not copy %s to %s" % (src, dst))
        say_it("- %s" % e)
        return 1


def encrypt(s, key=365):
    """ Encrypt a string, add _ to escape spelling check
    """
    b = bytearray(str(s).encode("gbk"))
    n = len(b)
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        key -= 1
        b1 = b[i]
        b2 = b1 ^ key
        c1 = b2 % 16 + 65
        c2 = b2 // 16 + 65
        c[j] = c1
        c[j+1] = c2
        j += 2
    my_code = c.decode("gbk")
    return "_".join(my_code)


def decrypt(s, key=365):
    """ Decrypt a string
    """
    s = re.sub("_", "", s)
    c = bytearray(str(s).encode("gbk"))
    n = len(c)
    if n % 2 != 0:
        say_it("Error. Cannot decrypt code: %s" % s)
        return ""
    n //= 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        key -= 1
        c1 = c[j] - 65
        c2 = c[j+1] - 65
        j += 2
        b2 = c2 * 16 + c1
        b1 = b2 ^ key
        b[i] = b1
    return b.decode("gbk")


def _get_column_letter(col_idx):
    """Convert a column number into a column letter (3 -> 'C')

    Right shift the column col_idx by 26 to find column letters in reverse
    order.  These numbers are 1-based, and can be converted to ASCII
    ordinals by adding 64.

    """
    if not 1 <= col_idx <= 18278:
        raise ValueError("Invalid column index {0}".format(col_idx))
    letters = []
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx, 26)
        if remainder == 0:
            remainder = 26
            col_idx -= 1
        letters.append(chr(remainder+64))
    return ''.join(reversed(letters))


_COL_STRING_CACHE = {}
_STRING_COL_CACHE = {}
for mm in range(1, 18279):
    col = _get_column_letter(mm)
    _STRING_COL_CACHE[mm] = col
    _COL_STRING_CACHE[col] = mm


def get_column_letter(idx,):
    """Convert a column index into a column letter
    (3 -> 'C')
    """
    try:
        return _STRING_COL_CACHE[idx]
    except KeyError:
        raise ValueError("Invalid column index {0}".format(idx))


# / **********************************
# INNER TINY FUNCTIONS
def _fn_match(name, patterns):
    """Filename matching
        *       matches everything
        ?       matches any single character
        [seq]   matches any character in seq
        [!seq]  matches any char not in seq
    """
    if isinstance(patterns, str):
        patterns = [patterns]
    for p in patterns:
        if fnmatch.fnmatch(name, p):
            return 1