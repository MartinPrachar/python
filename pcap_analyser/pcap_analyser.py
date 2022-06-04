""" open, parse and close a pcap file
"""
import sys
import re
import socket
import os
import dpkt
from graph import packet_count, plot_graph
from geolocation import get_locations, create_kml_file
from print_lib import content_summary, ip_addr_summary, urls_and_files


def main() -> list:
    """parsing pcap file, storing packets information in suitable objects"""
    try:
        open_file = open(sys.argv[1], "rb")
    except FileNotFoundError as err:
        print("[-]", err.__class__.__name__, err)
        return []
    except IndexError as err:
        print("[-]", err.__class__.__name__, err)
        return []
    pcap = dpkt.pcap.Reader(open_file)
    packets = []
    # pacekt_type:[number_of_packets, length, fitrst_timestamp, last_timestamp]
    packets_summary = {}
    list_of_emails = []
    list_of_urls = []
    list_of_images = []
    ip_summary = {}  # ip_addr:[sent from, sent to]
    interval = 15
    ts_list = []
    dst_ips = []

    for tim_s, buf in pcap:
        # loop over pcap file
        eth = dpkt.ethernet.Ethernet(buf)
        ip_ad = eth.data

        # TASK 2 - Collecting packets information
        packet_type = str(type(eth.data.data)).split(".")[1].upper()
        if packet_type not in packets_summary:
            packets_summary[packet_type] = [0, 0, tim_s, tim_s]
        packets_summary[packet_type][0] += 1          # counting packets
        packets_summary[packet_type][1] += len(eth)   # packets length
        packets_summary[packet_type][3] = tim_s       # update last timestamp

        # TASK 3 - Extracting email addresses, urls and image file names
        email = re.compile(r"TO+\W\s<[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]"
                           r"+\.[A-Za-z]{2,4}>|FROM+\W\s<[A-Za-z0-9._%+-]"
                           r"+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}>")
        output = email.findall(repr(eth))
        if output:
            email_addr = str(output[0]).split("<")[1][:-1]
            if email_addr not in list_of_emails:
                list_of_emails.append(email_addr)
        try:
            http = dpkt.http.Request(ip_ad.data.data)
            http_extension = os.path.splitext(http.uri)[1]
            if http_extension.lower() in [".jpg", ".gif", ".png"]:
                file_name = os.path.basename(http.uri)
                if http.uri not in list_of_urls:
                    list_of_urls.append(http.uri)
                list_of_images.append(file_name)
        except Exception:
            # print("[-]", err.__class__.__name__, err)
            pass

        # TASK 4 - Extracting IP addresses and counting packets
        src = socket.inet_ntoa(ip_ad.src)
        dst = socket.inet_ntoa(ip_ad.dst)
        if src not in ip_summary:
            ip_summary[src] = [0, 0]
        if dst not in ip_summary:
            ip_summary[dst] = [0, 0]
        ip_summary[src][0] += 1
        ip_summary[dst][1] += 1

        if dst not in dst_ips:
            dst_ips.append(dst)
        ts_list.append(tim_s)
        packets.append(eth.data)

    open_file.close()

    # TASK 2
    content_summary(packets_summary)

    # TASK 3
    urls_and_files(list_of_emails, list_of_urls, list_of_images)

    # TASK 4
    ip_addr_summary(ip_summary)

    # TASK 5
    locations = get_locations(dst_ips, ip_summary)
    create_kml_file(locations)

    # TASK 6
    packet_count_dict = packet_count(ts_list, interval)
    plot_graph(packet_count_dict)

    return packets


if __name__ == "__main__":
    main()
