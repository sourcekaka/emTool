#!/usr/bin/env python3
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')

from chart_column import to_percent


def _line_chart_sheet_mat(sp1, data, mabid, ave_load,
                          min_load, max_load, variance):
    mab_name = mabid
    list_fn = data[0]
    list_load = data[1]
    list_max = len(data[0]) * [max_load]
    list_min = len(data[0]) * [min_load]

    text_str = 'average load:' + str("%.2f%%" % (ave_load * 100)) + '\n' \
        + 'maxload:' + str("%.2f%%" % (max_load * 100)) + '\n' \
        + 'miniload:' + str("%.2f%%" % (min_load * 100)) + '\n' \
        + 'variance:' + str("%.2f%%" % (variance * 100)) + '\n'
    sfn = np.min(list_fn)
    efn = np.max(list_fn)
    sp1.text(
        (sfn + efn) / 2,
        0.5,
        text_str,
        color='red',
        bbox=dict(
            boxstyle='round,pad=0.5',
            fc='white',
            ec='k',
            lw=1,
            alpha=0.4))
    sp1.grid(True)

    sp1.plot(list_fn, list_load, label='ave', color='green', alpha=0.8)
    sp1.plot(list_fn, list_max, label='max', color='red', alpha=0.8)
    sp1.plot(list_fn, list_min, label='min', color='blue', alpha=0.8)
    sp1.set_title('cpu utilization graph:' + mabid)
    sp1.yaxis.set_major_formatter(FuncFormatter(to_percent))
    sp1.set_xlabel('subframe (per subframe 1ms)')
    sp1.set_ylabel('cpu load(%)')
    sp1.legend()


def _line_chart_fig_mat(result_path, mab_dict, mab_str):
    key_idx = 0
    subplot_num_per_fig = 2
    fig_num = int((len(mab_dict) + 1) / subplot_num_per_fig)
    key_list = list(mab_dict.keys())
    for fig_idx in range(0, fig_num):
        fig_tmp = plt.figure(figsize=(12, 4))
        out_path = result_path + '/chart_line_' + \
            mab_str + str(fig_idx + 1) + '.png'
        subplot_idx = 1
        for mabid in key_list[key_idx:key_idx + subplot_num_per_fig]:
            key_idx = key_idx + 1
            ave_load = mab_dict[mabid].ave
            min_load = mab_dict[mabid].min
            max_load = mab_dict[mabid].max
            variance = mab_dict[mabid].vari
            list_fn = mab_dict[mabid].list_fn
            list_load = mab_dict[mabid].list_load
            data = [list_fn, list_load]

            sp1 = fig_tmp.add_subplot(1, subplot_num_per_fig, subplot_idx)
            subplot_idx = subplot_idx + 1
            _line_chart_sheet_mat(
                sp1,
                data,
                mabid,
                ave_load,
                min_load,
                max_load,
                variance)
        plt.savefig(out_path)


def line_chart_mat(result_path, mab_dict1, mab_dict2):
    _line_chart_fig_mat(result_path, mab_dict1, "mdab")
    _line_chart_fig_mat(result_path, mab_dict2, "mhab")
