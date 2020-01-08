#!/usr/bin/env python3
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.use('Agg')


def to_percent(data, position):
    return "%1.0f" % (100 * data) + "%"


def _column_chart_sheet_mat(sp1, mab_dict, min_time,
                            max_time, mab_name, color):
    list_mabid = []
    list_ave = []
    for mabid in mab_dict:
        list_mabid.append(mabid)
    list_mabid.sort()
    for mabid in list_mabid:
        list_ave.append(mab_dict[mabid].ave)
    sp1.bar(list_mabid, list_ave, label='LOAD', color=color, alpha=0.8)
    sp1.set_title(
        mab_name +
        " load summary\n  subframe:" +
        str(min_time) +
        " --- " +
        str(max_time))
    sp1.yaxis.set_major_formatter(FuncFormatter(to_percent))
    for x, y in enumerate(list_ave):
        sp1.text(x, y + 0.01, "%1.1f" % (100 * y) + "%", ha='center')

    sp1.set_xlabel(mab_name + " ID")
    sp1.set_ylabel("AVERAGE_CPULOAD(%)")
    sp1.grid(True)
    sp1.legend()


def column_chart_mat(result_path, mab_dict1, mab_dict2, min_time, max_time):
    out_path = result_path + '/chart_column.png'

    fig = plt.figure(figsize=(12, 5))
    plt.suptitle("load summary")
    sp1 = fig.add_subplot(121)
    _column_chart_sheet_mat(
        sp1,
        mab_dict1,
        min_time,
        max_time,
        'MDAB',
        'green')
    sp2 = fig.add_subplot(122)
    _cloumn_chart_sheet_mat(sp2, mab_dict2, min_time, max_time, 'MHAB', 'blue')

    plt.savefig(out_path)
    plt.close()
