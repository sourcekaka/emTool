#!/usr/bin/env python3
import xlsxwriter
import numpy as np

from psm_log_pre_analyse import get_max_tick

def _write_head(work_book, work_sheet, min_time, max_time):
    # Increase the cell size of the merged cells to highlight the formatting.
    work_sheet.set_column("B:E", 18)
    work_sheet.set_row(0, 25)

    # Create a format to use in the merged range.
    merge_format = work_book.add_format(
        {
            "bold": 1,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
            "bg_color": "yellow",
        }
    )

    merge_format.set_text_wrap()

    # Merge 3 cells.
    work_sheet.merge_range(
        "B1:E1",
        "GENERAL STATICS\n(load value in the form of percentage x 100)",
        merge_format,
    )
    work_sheet.merge_range("F1:G1", "TIME STATICS..", merge_format)
    work_sheet.merge_range("A1:A2", "MAB_ID", merge_format)

    work_sheet.write(1, 1, "MIN", merge_format)
    work_sheet.write(1, 2, "MAX", merge_format)
    work_sheet.write(1, 3, "AVERAGE", merge_format)
    work_sheet.write(1, 4, "VARIANCE", merge_format)

    for x in range(min_time, max_time + 1):
        work_sheet.write(1, 5 + x - min_time, x)


class mabData:
    def __init__(self):
        self.row = 0
        self.min = 0
        self.max = 0
        self.ave = 0
        self.vari = 0
        self.list_fn = []
        self.list_load = []


def calc_data(list_load):
    mab_data_min = np.min(list_load)
    mab_data_max = np.max(list_load)
    mab_data_ave = np.mean(list_load)
    mab_data_vari = np.var(list_load)
    return mab_data_min, mab_data_max, mab_data_ave, mab_data_vari


def _calc_cpu_time_percentage(value, mab_idx):
    max_tick = get_max_tick(mab_idx)
    return value / max_tick
    
    
def _write_data(work_book, work_sheet, min_time, max_time, mab_src_dict, mab_idx):
    mabdict = {}
    row_pos = 2

    format2 = work_book.add_format({"num_format": "##0.00%"})

    for mab_name in mab_src_dict:
        fn_and_tick_tmp = mab_src_dict[mab_name]
        mab_data_tmp = mabData()
        if mab_name in mabdict:
            mab_data_tmp.row = mabdict[mab_name].row
        else:
            mab_data_tmp.row = row_pos
            work_sheet.write(mab_data_tmp.row, 0, mab_name)
            # append the new data at new line
            row_pos = row_pos + 1

        for fn in range(min_time, max_time + 1):
            if fn in fn_and_tick_tmp.keys():
                # write the frame data
                value = fn_and_tick_tmp[fn]
                core_cpu_time_percentage = _calc_cpu_time_percentage(value, mab_idx)
                work_sheet.write(
                    mab_data_tmp.row,
                    5 + fn - min_time,
                    core_cpu_time_percentage,
                    format2,
                )
            else:
                core_cpu_time_percentage = 0
                work_sheet.write(
                    mab_data_tmp.row,
                    5 + fn - min_time,
                    core_cpu_time_percentage,
                    format2,
                )
            mab_data_tmp.list_fn.append(fn)
            mab_data_tmp.list_load.append(core_cpu_time_percentage)

        # refresh the calculate value
        (
            mab_data_tmp.min,
            mab_data_tmp.max,
            mab_data_tmp.ave,
            mab_data_tmp.vari,
        ) = calc_data(mab_data_tmp.list_load)
        work_sheet.write(mab_data_tmp.row, 1, mab_data_tmp.min, format2)
        work_sheet.write(mab_data_tmp.row, 2, mab_data_tmp.max, format2)
        work_sheet.write(mab_data_tmp.row, 3, mab_data_tmp.ave, format2)
        work_sheet.write(mab_data_tmp.row, 4, mab_data_tmp.vari, format2)
        mabdict[mab_name] = mab_data_tmp

    return mabdict


def bphy_utilization_excel(result_path, dict1, dict2, min_time, max_time):
    xlsx_path = result_path + "/psmlog PSM Log tool.xlsx"
    work_book = xlsxwriter.Workbook(xlsx_path)
    work_sheet1 = work_book.add_worksheet("MDAB")
    _write_head(work_book, work_sheet1, min_time, max_time)
    work_sheet2 = work_book.add_worksheet("MHAB")
    _write_head(work_book, work_sheet2, min_time, max_time)
    mab_dict1 = _write_data(work_book, work_sheet1, min_time, max_time, dict1 , 1)
    mab_dict2 = _write_data(work_book, work_sheet2, min_time, max_time, dict2 , 0)

    work_book.close()
    return mab_dict1, mab_dict2
