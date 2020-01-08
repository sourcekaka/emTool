#!/usr/bin/env python3
import os
import time
import shutil

from chart_line import line_chart_mat
from chart_column import column_chart_mat
from psm_log_to_excel import bphy_utilization_excel
from psm_log_pre_analyse import make_excel_dict


def _psm_post_analyser(result_path, dict1, dict2, min_time, max_time):
    mab_dict1, mab_dict2 = bphy_utilization_excel(
        result_path, dict1, dict2, min_time, max_time)
    column_chart_mat(result_path, mab_dict1, mab_dict2, min_time, max_time)
    line_chart_mat(result_path, mab_dict1, mab_dict2)


def psm_post_analyse_main(result_path, csv_file):
    sheet_mdab, sheet_mhab, min_time, max_time = make_excel_dict(csv_file)
    _psm_post_analyser(result_path, sheet_mdab, sheet_mhab, min_time, max_time)
    return 0
