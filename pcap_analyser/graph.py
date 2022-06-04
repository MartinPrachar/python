"""library to create a graph
"""
import statistics
import matplotlib.pyplot as plt


def packet_count(ts_list, interval) -> dict:
    """count number of packets per interval"""
    ts0 = ts_list[0]
    packet_count_dict = {ts0: 0}
    for time_stamp in ts_list:
        if (time_stamp-ts0) > interval:
            ts0 = ts0+interval
            packet_count_dict[ts0] = 0
        packet_count_dict[ts0] += 1
    return packet_count_dict


def plot_graph(data_dict):
    """create a graph"""
    plt.plot(data_dict.keys(), data_dict.values(), linestyle='-',
             marker='o', color='b', label="# packets")

    mean = statistics.mean(data_dict.values())
    std_dev = statistics.stdev(data_dict.values())

    plt.axhline(y=(mean+2*std_dev), color='r', linestyle='--',
                label="high traffic warning")

    plt.xlabel("value")
    plt.ylabel("frequency")
    plt.title("Packet count")
    plt.legend()
    plt.savefig('packet_count_graph.png')
    plt.show()
