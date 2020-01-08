#!/usr/bin/env python3
import os
import time
import shutil
import subprocess
from subprocess import Popen, PIPE

from psm_post_analyser import psm_post_analyse_main

status, repo_path = subprocess.getstatusoutput('git rev-parse --show-toplevel')


def _psm_log_parser(cmd, bin_file, csv_file):
    if not os.path.isfile(cmd):
        print("ERROR:psmLogParser:{} doesn't exist.".format(cmd))
        return 1
    if not os.path.isfile(bin_file):
        print("ERROR:psmLog bin:{} file doesn't exist.".format(bin_file))
        return 1

    if os.path.isfile(csv_file):
        os.remove(csv_file)
    p = Popen(
        cmd +
        " " +
        bin_file +
        " " +
        csv_file,
        shell=True,
        stdout=PIPE,
        stderr=PIPE)
    p.communicate()
    p.wait()
    if p.returncode != 0:
        print("psmLogParser Error returncode = {:d}.".format(p.returncode))
        return 1
    else:
        print("psmLogParser return OK, result file is at : {}.".format(csv_file))
        return 0


if __name__ == "__main__":
    result_path = os.path.abspath(
        os.path.join(
            os.path.expanduser('~'),
            "psm_log_result/"))
    cmd = os.path.abspath(
        os.path.join(
            repo_path,
            "out/build-clang64/tools/psmLogParser/PsmLogParser"))
    bin_file = os.path.abspath(
        os.path.join(
            repo_path,
            "tools/asim/docker/ffs/run/logs/PSMLog_entries.bin"))
    csv_file = os.path.abspath(
        os.path.join(
            result_path,
            "PSMLog_entries.csv"))

    if os.path.exists(result_path):
        shutil.rmtree(result_path)
        time.sleep(1)
    os.mkdir(result_path)

    if 0 == _psm_log_parser(cmd, bin_file, csv_file):
        psm_post_analyse_main(result_path, csv_file)
        print("PSM parse successfully, parse result at: {}".format(result_path))
    else:
        print("psmLogParser failed.")
