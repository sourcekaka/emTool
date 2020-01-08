#!/usr/bin/env python3
import csv
import sys

import numpy as np

mhab_set0 = 0
mhab_set2 = 2
mdab_set = 1
column_mab_id = 0
column_fr_sf_tick = 3
column_cmd = 4
frame_num_per_superframe = 1024

def _filter_rsp(log_entrys):
    lines_with_rsp = []
    for log_entry in log_entrys:
        if log_entry[column_cmd] == 'RSP':
            lines_with_rsp.append(log_entry)
    return lines_with_rsp


def _store_data_in_dict(lines_list):
    field_sub_frame = 1
    sub_frame_per_frame = 10
    column_elapsed_ticks = 12
    mab_subframe_ticks_dict = {}
    prev_frame_num = 0
    super_frame_num = 0

    for line_no in range(len(lines_list)):
        if lines_list[line_no][column_mab_id] not in mab_subframe_ticks_dict:
            mab_subframe_ticks_dict.setdefault(
                lines_list[line_no][column_mab_id], {})
        frame = lines_list[line_no][column_fr_sf_tick].split(
            '-')[column_mab_id]
        frame_num = int(frame, 16)
        if frame_num < prev_frame_num:
            super_frame_num = super_frame_num + 1
            if 2 <= super_frame_num:
                raise Exception('super_frame_num can not be larger than 2.')
        prev_frame_num = frame_num
        sub_frame = lines_list[line_no][column_fr_sf_tick].split(
            '-')[field_sub_frame]
        abs_sub_frame = ((super_frame_num * frame_num_per_superframe) + frame_num) * \
            sub_frame_per_frame + int(sub_frame, 16)
        elapsed_ticks_dec = int(lines_list[line_no][column_elapsed_ticks], 16)

        if abs_sub_frame not in mab_subframe_ticks_dict[lines_list[line_no]
                                                        [column_mab_id]]:
            mab_subframe_ticks_dict[lines_list[line_no]
                                    [column_mab_id]][abs_sub_frame] = elapsed_ticks_dec
        else:
            mab_subframe_ticks_dict[lines_list[line_no]
                                    [column_mab_id]][abs_sub_frame] += elapsed_ticks_dec

    return mab_subframe_ticks_dict


def _extract_job_resp_from_csv(csv_file_name):
    with open(csv_file_name, "r") as csvfile:
        read = csv.reader(csvfile)
        lines_with_rsp = _filter_rsp(read)
        mab_subframe_ticks_dict = _store_data_in_dict(lines_with_rsp)
    return mab_subframe_ticks_dict


def _get_name_of_mab(id):
    mhab_name1 = {
        '0x0': 'PRCH',
        '0x1': 'ULFE',
        '0x2': 'RDEC',
        '0x3': 'DLFE',
        '0x4': 'FDEQ0',
        '0x5': 'PENC',
        '0x6': 'LENC0',
        '0x7': 'RMAP0',
        '0x8': 'EDEC',
        '0x9': 'DENC',
        '0xa': 'RMAP1',
        '0xb': 'PDEC',
        '0xc': 'TDEC',
        '0xd': 'LDEC0',
        '0xe': 'VDEC',
        '0x10': 'ECMP',
        '0x11': 'LENC1',
        '0x12': 'PNBD0',
        '0x13': 'PNBD1',
        '0x14': 'FDEQ1',
        '0x15': 'DMAP0',
        '0x16': 'DMAP1',
        '0x17': 'LDEC1'
    }

    mhab_name2 = {
        '0x0': 'RFOE0',
        '0x1': 'RFOE1',
        '0x2': 'RFOE2',
        '0x3': 'CPRI0',
        '0x4': 'CPRI1',
        '0x5': 'CPRI2'
    }
    set_idx_mask = 0xC0
    name_idx_mask = 0x3F
    set_idx_shift_bits = 6

    mab_id = int(id, 16)
    set_idx = (mab_id & set_idx_mask) >> set_idx_shift_bits
    name_idx = mab_id & name_idx_mask
    name_key = hex(name_idx)
    mab_name = ''
    if mhab_set0 == set_idx:
        mab_name = mhab_name1[name_key]
    elif mdab_set == set_idx:
        mab_name = 'CBP' + str(name_idx)
    elif mhab_set2 == set_idx:
        mab_name = mhab_name2[name_key]
    else:
        print("ERROR: Invalid MAB_ID!")
    return set_idx, mab_name


def get_max_tick(mab_idx):
    max_mdab_ticks = 1100000
    max_mhab_ticks = 1000000
    return max_mdab_ticks if mdab_set == mab_idx else max_mhab_ticks


def make_excel_dict(csv_file_name):
    mab_subframe_ticks_dict = _extract_job_resp_from_csv(csv_file_name)
    mdab_sheet = {}
    mhab_sheet = {}
    subframe_list = []
    for mab_id in mab_subframe_ticks_dict:
        set_idx, mab_name = _get_name_of_mab(mab_id)
        subframe_ticks_dict = mab_subframe_ticks_dict[mab_id]
        peak_clip_subframe_ticks_dict = {}
        for sub_frame in subframe_ticks_dict:
            peak_clip_subframe_ticks_dict[sub_frame] = subframe_ticks_dict[sub_frame]
            max_tick = get_max_tick(set_idx)
            if peak_clip_subframe_ticks_dict[sub_frame] > max_tick:
                peak_clip_subframe_ticks_dict[sub_frame] = max_tick
            subframe_list.append(sub_frame)

        if mdab_set == set_idx:
            mdab_sheet[mab_name] = peak_clip_subframe_ticks_dict
        else:
            mhab_sheet[mab_name] = peak_clip_subframe_ticks_dict

    min_subframe = np.min(subframe_list)
    max_subframe = np.max(subframe_list)
    return mdab_sheet, mhab_sheet, min_subframe, max_subframe
